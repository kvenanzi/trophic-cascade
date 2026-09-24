import numpy as np

from trophic.effects import abundance, bootstrap, community_importance, compensation


def test_measures():
    de = np.zeros((4, 2, 2)); de[:, 0, 0] = 3; de[:, 1, 1] = -1
    p = abundance(de)
    assert np.isclose(p[0, 0], 0.75) and np.isclose(p[1, 1], 0.25)
    ld = np.full(4, 4.0)
    # removing a head that holds 25% of abundance and costs 25% of the trait: CI = 1
    assert np.isclose(community_importance(ld, np.full(4, 3.0), 0.25), 1.0)
    # full compensation, none, and overcompensation
    assert np.isclose(compensation(ld, ld, np.full(4, 2.0)), 1.0)
    assert np.isclose(compensation(ld, ld - 2, np.full(4, 2.0)), 0.0)
    assert compensation(ld, ld + 1, np.full(4, 2.0)) > 1
    pt, lo, hi = bootstrap(lambda a: a.mean(), [np.arange(100.0)], n_boot=200)
    assert lo < pt < hi
