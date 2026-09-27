"""Model B-5: the return trip without expansion - commitments use up a budget (written before running).
ED source: README 'Commitments use up a budget'; paper s2 'An event commits and is spent'.
B-3's card model, no expansion, plus: when committed becoming dissolves (rate 1/L), a fraction EPS is SPENT -
it leaves the active field (tallied, conserved in the bookkeeping: active + spent = start). Committing churns
only where density is above threshold, so spending happens where structure is.
PREDICTION: a clump's life scales as L / EPS. At a clump, dissolve flux c/L spends EPS*c/L per step, and the
clump's mass is mostly c, so it decays like exp(-EPS t / L). Doubling EPS halves the life; x10 L (at fixed
P = s kappa L theta) gives about x10. EPS = 0 is B-3: clumps forever (control).
Also expected: the active field returns to smooth (complexity back to the uniform value 14), and the spent
tally ends up as a large share of the total.
Usage: python b5_spend.py L EPS   (P fixed at 5)"""
import sys, json, numpy as np
import b3_card as m
L, EPS = int(sys.argv[1]), float(sys.argv[2]); P = 5.0; s = P / (m.KAPPA * L * m.THETA)
T = 400000; rng = np.random.default_rng(1)
rho, c = m.drop(rng, 1e-3); total0 = (rho + c).sum(); spent = 0.0; rows = []; peak = 0.0; death = None
for t in range(T + 1):
    if t % 1000 == 0:
        tot = rho + c; cf = float(c.sum() / total0); peak = max(peak, cf)
        rows.append((t, m.complexity(tot), round(cf, 4), round(spent / total0, 4)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None and t > death + 20000: break
    if t == T: break
    rho, c = m.step(rho, c, s, L)
    lost = EPS * c / L          # the spent share of this step's dissolving (step() already returned c/L to rho)
    rho = rho - lost; spent += lost.sum()
drift = abs((rho + c).sum() + spent - total0) / total0
K = [r[1] for r in rows]; i = int(np.argmax(K))
d = dict(L=L, EPS=EPS, s=s, death=death, Kpeak=K[i], t_peak=rows[i][0], Kend=K[-1], spent_end=rows[-1][3],
         cfrac_end=rows[-1][2], life_x_eps_over_L=(None if death is None else round(death * EPS / L, 3)), drift=float(drift))
print(d, flush=True); json.dump(dict(summary=d, rows=rows), open(f"b5_L{L}_e{EPS}.json", "w"))
