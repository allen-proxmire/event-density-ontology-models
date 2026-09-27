"""B-5b: tightened measurement for the square-root law (other session's three fixes): deaths read every 100 steps,
three seeds per cell, and the missing cell (hbar 30, eps 0.01). Also records committed and spent totals every
500 steps, so the derivation can be checked against the trajectory, not just the death time.
Usage: python b5b.py L EPS SEED"""
import sys, json, numpy as np
import b3_card as m
L, EPS, seed = int(sys.argv[1]), float(sys.argv[2]), int(sys.argv[3]); P = 5.0; s = P / (m.KAPPA * L * m.THETA)
rng = np.random.default_rng(seed); rho, c = m.drop(rng, 1e-3); total0 = (rho + c).sum(); spent = 0.0
traj = []; peak = 0.0; death = None; t = 0
while t < 400000:
    if t % 100 == 0:
        cf = float(c.sum() / total0); peak = max(peak, cf)
        if t % 500 == 0: traj.append((t, round(cf, 5), round(spent / total0, 5)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None and t > death + 2000: break
    rho, c = m.step(rho, c, s, L); lost = EPS * c / L; rho = rho - lost; spent += lost.sum(); t += 1
json.dump(dict(L=L, EPS=EPS, seed=seed, death=death, spent_at_death=(None if death is None else next(x[2] for x in traj if x[0] >= death)), traj=traj),
          open(f"b5b_L{L}_e{EPS}_s{seed}.json", "w"))
print(L, EPS, seed, death, flush=True)
