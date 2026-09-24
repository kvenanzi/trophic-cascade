"""Part B plumbing on toy models, CPU only, a few seconds each."""

import numpy as np
import torch

from trophic.model import add_drophead, build, gpt2_config, to_hooked
from trophic.selfrepair import measure

TINY = dict(n_layer=2, n_head=4, d_model=32, d_mlp=64, ctx=16)


def test_arms_configure_dropout():
    assert gpt2_config("none").resid_pdrop == 0 and gpt2_config("drophead").attn_pdrop == 0
    s = gpt2_config("standard")
    assert s.resid_pdrop == s.embd_pdrop == s.attn_pdrop == 0.1


def test_drophead_masks_whole_heads_in_training_only():
    m = build("none", 0, **TINY)
    add_drophead(m, 0.5)
    proj = m.transformer.h[0].attn.c_proj
    seen = {}
    proj.register_forward_pre_hook(lambda mod, args: seen.__setitem__("x", args[0]))
    x = torch.randint(0, 50257, (8, 16))
    m.train()
    m(x)
    heads = seen["x"].view(8, 16, 4, 8)
    zero = (heads == 0).all(dim=(1, 3))                  # [B, H]: head silenced for a whole sequence
    assert zero.any() and not zero.all()
    live = heads[~zero[:, None, :, None].expand_as(heads)]
    assert live.abs().sum() > 0
    m.eval()
    m(x)
    assert not (seen["x"].view(8, 16, 4, 8) == 0).all(dim=(1, 3)).any()


def test_hooked_conversion_matches_hf():
    m = build("standard", 1, **TINY).eval()
    x = torch.randint(0, 50257, (2, 16))
    hf = torch.log_softmax(m(x).logits, -1)
    tl = torch.log_softmax(to_hooked(m, "cpu")(x), -1)
    assert torch.allclose(hf, tl, atol=1e-4)


def test_selfrepair_runs():
    m = to_hooked(build("none", 2, **TINY).eval(), "cpu")
    toks = torch.randint(0, 50257, (6, 17))
    r = measure(m, toks, top_frac=0.1, batch_size=3)
    assert np.isfinite(r["pooled"]) and r["per_head"].shape == (2, 4)
    assert len(r["per_layer"]) == 2


def test_train_smoke(tmp_path, monkeypatch):
    """End to end on a synthetic token file: train, measure at every point, save."""
    monkeypatch.setenv("WANDB_MODE", "disabled")
    from trophic.train import TrainConfig, train
    rng = np.random.default_rng(0)
    for split, n in (("train", 40_000), ("validation", 4_000)):
        rng.integers(0, 50257, n).astype(np.uint16).tofile(tmp_path / f"{split}.bin")
    for arm in ("none", "drophead"):
        cfg = TrainConfig(arm=arm, seed=0, tokens=8 * 16 * 20, batch_size=8, ctx=16, n_layer=2,
                          n_head=4, d_model=32, d_mlp=64, measure_points=2, measure_seqs=8,
                          val_seqs=16, data_dir=str(tmp_path), output_dir=str(tmp_path / "models"),
                          log_model=False, run_name=f"t-{arm}")
        out = train(cfg)
        assert [h["step"] for h in out["history"]] == [0, 10, 20]
        assert all(np.isfinite(h["val_loss"]) for h in out["history"])
