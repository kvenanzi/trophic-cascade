"""Ecological measures computed from removal experiments (trophic/ablate.py).

Terms, with the ecological source of each:

- abundance p_i: head i's share of the summed absolute direct effect of all heads on
  the unablated prompts. The analogue of proportional biomass (Power et al 1996).
- community importance CI_i = [(t_N - t_D) / t_N] / p_i, where t is the mean logit
  difference, N the intact model, D the model with head i removed (Power et al 1996).
  CI_i = 1 is an effect in proportion to abundance.
- compensation c = 1 - TE / DE for a removed set: TE is the fall in logit difference,
  DE the removed heads' summed direct effect. c = 0 is no compensation, c = 1 full
  compensation, c > 1 overcompensation (the "hydra effect" of population ecology,
  Abrams 2009). Rushing & Nanda (2024) call DE - TE "self-repair".
- interaction strength of i on j: the change in j's direct effect when i is removed,
  Delta_ij = DE_j(-i) - DE_j (Paine 1992; Berlow et al 1999).
- log response ratio of j's activity to the removal of i: ln(mean A_j(-i) / mean A_j)
  (Hedges et al 1999; Shurin et al 2002).
"""

from __future__ import annotations

import numpy as np

# Head classes of the GPT-2 small IOI circuit, Wang et al (2022) Figure 2.
CLASSES = {
    "previous_token": [(2, 2), (4, 11)],
    "duplicate_token": [(0, 1), (3, 0), (0, 10)],
    "induction": [(5, 5), (6, 9), (5, 8), (5, 9)],
    "s_inhibition": [(7, 3), (7, 9), (8, 6), (8, 10)],
    "name_mover": [(9, 9), (9, 6), (10, 0)],
    "backup_name_mover": [(9, 0), (9, 7), (10, 1), (10, 2), (10, 6), (10, 10), (11, 2), (11, 9)],
    "negative_name_mover": [(10, 7), (11, 10)],
}

# Trophic levels for H3, in the order information flows through the circuit, and the
# position (index into ablate.POSITIONS) at which each level's activity is read.
# Backup name movers are left out: they sit beside the name movers, not below them.
LEVELS = [
    ("L1 previous-token", CLASSES["previous_token"], 0),
    ("L2 duplicate + induction", CLASSES["duplicate_token"] + CLASSES["induction"], 1),
    ("L3 S-inhibition", CLASSES["s_inhibition"], 2),
    ("L4 name mover", CLASSES["name_mover"], 2),
    ("L5 negative name mover", CLASSES["negative_name_mover"], 2),
]


def abundance(de: np.ndarray) -> np.ndarray:
    """p_i from per-prompt direct effects [n, L, H]: |mean DE_i| / sum_j |mean DE_j|."""
    m = np.abs(de.mean(0))
    return m / m.sum()


def community_importance(ld_intact: np.ndarray, ld_removed: np.ndarray, p: float) -> float:
    t_n, t_d = ld_intact.mean(), ld_removed.mean()
    return float((t_n - t_d) / t_n / p)


def compensation(ld_intact: np.ndarray, ld_removed: np.ndarray, de_removed_sum: np.ndarray
                 ) -> float:
    """1 - TE/DE, as a ratio of means over prompts. `de_removed_sum` is the per-prompt
    summed direct effect of the removed heads in the intact run."""
    te = (ld_intact - ld_removed).mean()
    return float(1 - te / de_removed_sum.mean())


def log_response_ratio(a_removed: np.ndarray, a_intact: np.ndarray) -> float:
    return float(np.log(a_removed.mean() / a_intact.mean()))


def bootstrap(stat, arrays: list[np.ndarray], n_boot: int = 2000, seed: int = 0,
              ) -> tuple[float, float, float]:
    """Point estimate and percentile 95% interval of stat(*arrays), resampling prompts
    (the first axis, shared by every array) with replacement."""
    rng = np.random.default_rng(seed)
    n = len(arrays[0])
    point = stat(*arrays)
    boots = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        boots.append(stat(*[a[idx] for a in arrays]))
    lo, hi = np.percentile(boots, [2.5, 97.5])
    return float(point), float(lo), float(hi)


def heads_str(heads) -> str:
    return ", ".join(f"{l}.{h}" for l, h in heads)
