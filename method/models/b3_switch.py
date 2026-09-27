"""Pinning B-3's switch.  Prediction (paper): flow runs up the gradient when P = s*kappa*L*theta > 1.

Test 1, the formula itself: a UNIFORM dense state above threshold (rho0 = 3 > theta = 2), with c at its steady value
c0 = kappa*L*(rho0 - theta), plus a small ripple. Linear theory: the ripple grows iff P > 1, whatever rho0.
Measured: the ripple's size (std of rho) at t = 0, 1000, 3000, 6000, 10000.
Test 2, the drop (the practical switch): same start as b3_card.py, P from 1.2 to 3.0 in steps of 0.1, three hbar.
Measured: committed fraction and clump count at t = 8000.
"""
import json, sys
import numpy as np
import b3_card as m

out = {"uniform": [], "drop": []}

print("TEST 1 - uniform dense state, ripple growth (std of rho)")
for L in (10, 100):
    for P in (0.8, 0.9, 0.95, 1.05, 1.1, 1.2):
        s = P / (m.KAPPA * L * m.THETA)
        rng = np.random.default_rng(1)
        rho0 = 3.0
        rho = rho0 * (1 + 1e-3 * rng.standard_normal((m.N,) * 3))
        c = np.full_like(rho, m.KAPPA * L * (rho0 - m.THETA))
        stds = {}
        for t in range(10001):
            if t in (0, 1000, 3000, 6000, 10000):
                stds[t] = float(rho.std())
            if t < 10000:
                rho, c = m.step(rho, c, s, L)
        verdict = "GROWS" if stds[10000] > stds[0] else "decays"
        out["uniform"].append(dict(L=L, P=P, s=s, stds=stds, verdict=verdict))
        print(f"L={L:3d} P={P:4.2f}  " + "  ".join(f"t{t}:{v:.1e}" for t, v in stds.items()) + f"  -> {verdict}", flush=True)

print("\nTEST 2 - the drop, fine sweep (committed fraction, clumps at t=8000)")
for L in (10, 30, 100):
    for P in [round(1.2 + 0.1 * i, 1) for i in range(19)]:
        s = P / (m.KAPPA * L * m.THETA)
        rows, drift, rho, c = m.run(s, L, 1, T=8000, every=8000)
        r = rows[-1]
        out["drop"].append(dict(L=L, P=P, s=s, cfrac=r["cfrac"], ncl=r["ncl"]))
        print(f"L={L:3d} P={P:3.1f}  cfrac={r['cfrac']:.3f}  clumps={r['ncl']}", flush=True)

json.dump(out, open("b3_switch.json", "w"), indent=1)
