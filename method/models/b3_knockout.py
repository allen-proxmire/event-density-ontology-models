"""Knock-a-clump-out test for B-3 (the other session's challenge: memory, or just stability?).

Grow clumps (s=1, L=10, product 4), pick the largest clump, then continue 3000 steps under three conditions:
  control : no change
  A       : its committed stuff is turned back into free stuff, in place (the pile of free becoming stays)
  B       : everything in the clump (free and committed) is spread evenly over the whole grid (nothing local left)
Measure: fraction of the old clump's cells that hold committed stuff again, against the chance level
(fraction of all cells holding committed stuff).
Expectations, written before running: control ~ stays; A re-forms in the SAME place, because the local pile of
free becoming is still there (that pile is the only 'memory' - a present-state trace, not a stored record);
B re-forms only at chance level.
"""
import numpy as np
from scipy import ndimage
import b3_card as m

S, L, T0, T1 = 1.0, 10, 8000, 3000


def grow(seed):
    rng = np.random.default_rng(seed)
    rho, c = m.drop(rng, 1e-3)
    for _ in range(T0):
        rho, c = m.step(rho, c, S, L)
    return rho, c


def cont(rho, c):
    for _ in range(T1):
        rho, c = m.step(rho, c, S, L)
    return rho, c


for seed in (1, 2, 3):
    rho, c = grow(seed)
    lab, n = ndimage.label(c > 0.1)
    sizes = np.bincount(lab.ravel()); sizes[0] = 0
    region = lab == sizes.argmax()
    grown = ndimage.binary_dilation(region, iterations=1)       # the clump plus a one-cell margin
    res = {}
    for cond in ("control", "A", "B"):
        r, cc = rho.copy(), c.copy()
        if cond == "A":
            r[grown] += cc[grown]; cc[grown] = 0
        if cond == "B":
            amt = (r[grown] + cc[grown]).sum(); r[grown] = 0; cc[grown] = 0; r += amt / r.size
        tot0 = (rho + c).sum()
        r, cc = cont(r, cc)
        assert abs((r + cc).sum() - tot0) / tot0 < 1e-10
        occ = cc > 0.1
        res[cond] = (float(occ[region].mean()), float(occ.mean()))
    print(f"seed {seed}: clump {int(region.sum())} cells | " +
          " | ".join(f"{k}: back {v[0]:.2f} (chance {v[1]:.2f})" for k, v in res.items()), flush=True)
