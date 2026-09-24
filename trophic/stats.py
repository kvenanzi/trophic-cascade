"""Paired statistics over seeds for Part B (§4.6), following rxnorm_vandf/stats.py."""

from __future__ import annotations

import math

T_975 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447, 7: 2.365, 8: 2.306,
         9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179}


def sign_test_p(n_pos: int, n: int) -> float:
    """Two-sided exact sign test."""
    k = min(n_pos, n - n_pos)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def paired(diffs: dict) -> dict:
    """Mean, sd, 95% t interval, and sign count of within-unit differences."""
    vals = list(diffs.values())
    k = len(vals)
    mean = sum(vals) / k
    sd = math.sqrt(sum((v - mean) ** 2 for v in vals) / (k - 1)) if k > 1 else 0.0
    se = sd / math.sqrt(k) if k > 1 else None
    t = T_975.get(k - 1)
    n_pos = sum(v > 0 for v in vals)
    return {"n": k, "mean": mean, "sd": sd,
            "ci95": [mean - t * se, mean + t * se] if se and t else None,
            "n_pos": n_pos, "sign_p": sign_test_p(n_pos, k), "diffs": diffs}
