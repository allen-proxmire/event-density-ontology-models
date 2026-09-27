"""Step 1: firm up the anchor. Rerun all four expansion cases (h = 3e-5) with NO cap on the search for the
clumps' peak density: track the densest clump's committed density and stop only once it has clearly fallen
(below 80% of its peak) or the clumps have died. Save the full state at the peak for the leak derivation."""
import json, sys, numpy as np
import b3_card as m
h = 3e-5
out = []
for (L, s) in ((10, 1.0), (10, 10.0), (100, 1.0), (100, 10.0)):
    rng = np.random.default_rng(1)
    rho, c = m.drop(rng, 1e-3)
    best, t0, state = 0.0, 0, None
    for t in range(400000):
        rho, c = m.step(rho, c, s, L)
        rho = rho - 3 * h * rho
        if t % 200 == 0:
            cm = float(c.max())
            if cm > best:
                best, t0, state = cm, t, (rho.copy(), c.copy())
            elif cm < 0.8 * best or cm < 1e-6:
                break
    np.savez(f"peak_L{L}_s{int(s)}.npz", rho=state[0], c=state[1], t0=t0)
    d = dict(L=L, s=s, t0=t0, c0_max=best, stopped=t)
    out.append(d); print(d, flush=True)
json.dump(out, open("b3_peak.json", "w"), indent=1)
