"""TinyStories (Eldan & Li 2023) as flat token files for Part B.

Each split is tokenized with the GPT-2 tokenizer, stories are joined with the
end-of-text token, and the result is written as one uint16 array per split
(`train.bin`, `validation.bin`), the layout nanoGPT uses. Training reads fixed
windows of CTX + 1 tokens (input and next-token target) at stride CTX.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

DATASET = "roneneldan/TinyStories"


def prepare(out_dir: str | Path = "data/tinystories", num_proc: int = 8) -> dict[str, int]:
    """Tokenize both splits into out_dir. Returns the token count per split; skips a
    split whose file already exists."""
    from datasets import load_dataset
    from transformers import AutoTokenizer

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    tok = AutoTokenizer.from_pretrained("gpt2")
    eos = tok.eos_token_id
    counts = {}
    for split in ("train", "validation"):
        path = out_dir / f"{split}.bin"
        if path.exists():
            counts[split] = len(np.memmap(path, dtype=np.uint16, mode="r"))
            continue
        ds = load_dataset(DATASET, split=split)
        ds = ds.map(lambda b: {"ids": [x + [eos] for x in tok(b["text"])["input_ids"]]},
                    batched=True, remove_columns=ds.column_names, num_proc=num_proc,
                    desc=f"tokenize {split}")
        lens = np.fromiter((len(x) for x in ds["ids"]), dtype=np.int64, count=len(ds))
        total = int(lens.sum())
        arr = np.memmap(path.with_suffix(".tmp"), dtype=np.uint16, mode="w+", shape=(total,))
        pos = 0
        for start in range(0, len(ds), 100_000):
            chunk = ds[start:start + 100_000]["ids"]
            flat = np.fromiter((t for ids in chunk for t in ids), dtype=np.uint16)
            arr[pos:pos + len(flat)] = flat
            pos += len(flat)
        arr.flush()
        del arr
        path.with_suffix(".tmp").rename(path)
        counts[split] = total
    return counts


class Windows:
    """Non-overlapping windows of ctx + 1 tokens from one split file."""

    def __init__(self, path: str | Path, ctx: int):
        self.data = np.memmap(path, dtype=np.uint16, mode="r")
        self.ctx = ctx
        self.n = (len(self.data) - 1) // ctx

    def get(self, idx: np.ndarray) -> np.ndarray:
        """[len(idx), ctx + 1] int64 array of windows."""
        starts = np.asarray(idx) * self.ctx
        return np.stack([self.data[s:s + self.ctx + 1] for s in starts]).astype(np.int64)
