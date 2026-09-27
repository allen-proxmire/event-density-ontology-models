"""Model B-6: expansion AND spending together (written before running).
B-3's card model at fixed P = 5 (s = P/(kappa L theta)), with both endings on: free becoming thins by 3h per step
(new places being born), and a fraction EPS of each dissolution is spent. Bookkeeping: active + leaked + spent
is conserved exactly. Deaths read every 100 steps.
PREDICTION (independent drains): 1/t_both = 1/t_expansion_only + 1/t_spending_only, to within about 15%.
Spending-only deaths at P = 5 come from B-5b; expansion-only deaths at P = 5 are measured here (EPS = 0).
Usage: python b6.py L EPS H"""
import sys, json, numpy as np
import b3_card as m
L, EPS, H = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]); P = 5.0; s = P / (m.KAPPA * L * m.THETA)
rng = np.random.default_rng(1); rho, c = m.drop(rng, 1e-3); total0 = (rho + c).sum(); spent = leaked = 0.0
peak = 0.0; death = None; t = 0; traj = []
while t < 600000:
    if t % 100 == 0:
        cf = float(c.sum() / total0); peak = max(peak, cf)
        if t % 1000 == 0: traj.append((t, round(cf, 4), round(spent / total0, 4), round(leaked / total0, 4)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None and t > death + 2000: break
    rho, c = m.step(rho, c, s, L)
    sp = EPS * c / L; rho = rho - sp; spent += sp.sum()
    lk = 3 * H * rho; rho = rho - lk; leaked += lk.sum(); t += 1
drift = abs((rho + c).sum() + spent + leaked - total0) / total0
d = dict(L=L, EPS=EPS, H=H, death=death, spent=round(spent / total0, 3), leaked=round(leaked / total0, 3), drift=float(drift))
print(d, flush=True); json.dump(dict(summary=d, traj=traj), open(f"b6_L{L}_e{EPS}_h{H}.json", "w"))
