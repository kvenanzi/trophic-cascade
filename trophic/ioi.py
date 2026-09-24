"""Indirect-object-identification (IOI) prompts.

A prompt such as "When Mary and John went to the store, John gave a drink to" has
two names in its first clause; one of them (the subject, S) is repeated, and the
correct continuation is the other (the indirect object, IO). The metric is the
logit difference logit(IO) - logit(S) at the last position.

The fifteen templates follow the BABA templates of Wang et al (2022); each is used
in both name orders (ABBA and BABA). The ABC set uses the same templates with
three fresh, distinct names in place of the IO and both occurrences of S, as in
Wang et al's p_ABC, so it carries the sentence structure without the repetition the
circuit keys on; its activations are the reference for mean ablation.

Names, places, and objects are restricted to strings that are a single token, with a
leading space, under every tokenizer in TOKENIZERS, so one prompt set serves every
model and every prompt of a template has the same token length.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, asdict

TEMPLATES = [
    "Then, [B] and [A] went to the [PLACE]. [B] gave a [OBJECT] to [A]",
    "Then, [B] and [A] had a lot of fun at the [PLACE]. [B] gave a [OBJECT] to [A]",
    "Then, [B] and [A] were working at the [PLACE]. [B] decided to give a [OBJECT] to [A]",
    "Then, [B] and [A] were thinking about going to the [PLACE]. [B] wanted to give a [OBJECT] to [A]",
    "Then, [B] and [A] had a long argument, and afterwards [B] said to [A]",
    "After [B] and [A] went to the [PLACE], [B] gave a [OBJECT] to [A]",
    "When [B] and [A] got a [OBJECT] at the [PLACE], [B] decided to give it to [A]",
    "When [B] and [A] got a [OBJECT] at the [PLACE], [B] decided to give the [OBJECT] to [A]",
    "While [B] and [A] were working at the [PLACE], [B] gave a [OBJECT] to [A]",
    "While [B] and [A] were commuting to the [PLACE], [B] gave a [OBJECT] to [A]",
    "After the lunch, [B] and [A] went to the [PLACE]. [B] gave a [OBJECT] to [A]",
    "Afterwards, [B] and [A] went to the [PLACE]. [B] gave a [OBJECT] to [A]",
    "Then, [B] and [A] had a long argument. Afterwards [B] said to [A]",
    "The [PLACE] [B] and [A] went to had a [OBJECT]. [B] gave it to [A]",
    "Friends [B] and [A] found a [OBJECT] at the [PLACE]. [B] gave it to [A]",
]

NAMES = [
    "Mary", "John", "Tom", "James", "Dan", "Sid", "Martin", "Amy", "Lisa", "Michael", "Sarah",
    "Paul", "David", "Kevin", "Jennifer", "Laura", "Andrew", "Mark", "Emily", "Jessica", "Anna",
    "Richard", "Steven", "Brian", "Robert", "Peter", "Susan", "Karen", "Nancy", "Linda", "George",
    "Edward", "Charles", "Thomas", "Joseph", "Daniel", "Matthew", "Anthony", "Rachel", "Kate",
    "Alice", "Grace", "Ruth", "Jack", "Henry", "Sam", "Alex", "Chris", "Jane", "Ben", "Max",
    "Adam", "Eric", "Frank", "Gary", "Jeff", "Joe", "Justin", "Ryan", "Scott", "Simon", "Victoria",
    "Helen", "Diana", "Julia", "Maria", "Patrick", "Tim", "Luke", "Carl", "Jason", "Philip",
]
PLACES = ["store", "garden", "restaurant", "school", "hospital", "office", "house", "station",
          "park", "beach", "library", "church", "market", "bar", "hotel", "kitchen", "museum"]
OBJECTS = ["ring", "kiss", "bone", "basketball", "computer", "necklace", "drink", "snack",
           "book", "letter", "pen", "bag", "ball", "gift", "card", "phone", "key", "cake"]

# Every model in the study; the vocabulary filter keeps only strings that are single
# tokens under all of them. GPT-2 small and medium share a tokenizer, as do the Pythias.
TOKENIZERS = ["gpt2", "EleutherAI/pythia-160m"]


@dataclass
class Prompt:
    template: int
    order: str        # "ABBA" (IO first in the first clause) or "BABA" (S first) or "ABC"
    text: str         # prompt without the answer
    io: str           # correct answer, with leading space
    s: str            # repeated subject, with leading space; for ABC, the second-clause subject
    names: tuple      # (first-clause name 1, first-clause name 2, second-clause subject)
    place: str
    obj: str

    def to_dict(self):
        return asdict(self)


def single_token_vocab(tokenizer_names: list[str] = TOKENIZERS) -> dict[str, list[str]]:
    """NAMES, PLACES, OBJECTS filtered to single tokens (with a leading space) under
    every tokenizer."""
    from transformers import AutoTokenizer

    toks = [AutoTokenizer.from_pretrained(n) for n in tokenizer_names]

    def ok(word: str) -> bool:
        return all(len(t.encode(" " + word, add_special_tokens=False)) == 1 for t in toks)

    return {"names": [w for w in NAMES if ok(w)],
            "places": [w for w in PLACES if ok(w)],
            "objects": [w for w in OBJECTS if ok(w)]}


def _fill(template: str, a: str, b: str, place: str, obj: str) -> str:
    return (template.replace("[A]", a).replace("[B]", b)
            .replace("[PLACE]", place).replace("[OBJECT]", obj))


def make_prompts(n_per_template: int, vocab: dict[str, list[str]], seed: int = 0,
                 ) -> tuple[list[Prompt], list[Prompt]]:
    """IOI prompts and their ABC counterparts.

    For each template, n_per_template prompts, half ABBA and half BABA. Each IOI prompt
    has an ABC twin with the same template, name order, place, and object, and three
    other distinct names A, B, C (first clause A and B, second-clause subject C).
    Returns (ioi, abc), aligned by index.
    """
    rng = random.Random(seed)
    ioi, abc = [], []
    for ti, tpl in enumerate(TEMPLATES):
        head, tail = tpl.rsplit(" [A]", 1)   # the final [A] is the answer, not part of the prompt
        assert tail == "", tpl
        for k in range(n_per_template):
            io, s = rng.sample(vocab["names"], 2)
            place, obj = rng.choice(vocab["places"]), rng.choice(vocab["objects"])
            order = "BABA" if k % 2 == 0 else "ABBA"
            # BABA: "[B] and [A] ... [B] gave ... to" ; ABBA swaps the first clause.
            first = head.replace("[B] and [A]", "[S1] and [IO]") if order == "BABA" \
                else head.replace("[B] and [A]", "[IO] and [S1]")
            text = first.replace("[S1]", s).replace("[IO]", io)
            text = _fill(text, io, s, place, obj)   # remaining [B] (second clause) -> S
            ioi.append(Prompt(ti, order, text, " " + io, " " + s,
                              (s, io, s) if order == "BABA" else (io, s, s), place, obj))
            a2, b2, c2 = rng.sample([n for n in vocab["names"] if n not in (io, s)], 3)
            text_abc = first.replace("[S1]", b2).replace("[IO]", a2)
            text_abc = _fill(text_abc, a2, c2, place, obj)
            abc.append(Prompt(ti, "ABC", text_abc, " " + a2, " " + c2,
                              (b2, a2, c2) if order == "BABA" else (a2, b2, c2), place, obj))
    return ioi, abc


N_PER_TEMPLATE = 40
SEED = 0


def standard_prompts() -> tuple[list[Prompt], list[Prompt]]:
    """The 600 IOI prompts and their ABC twins used throughout the write-up (§3.1)."""
    return make_prompts(N_PER_TEMPLATE, single_token_vocab(), seed=SEED)
