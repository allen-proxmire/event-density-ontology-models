"""B-4e: pinning the grain switch at three densities and testing the SCALING (written before running).
Pre-registered (other session's form): if grain amplitude noise holds the instability back, the switch's
OFFSET above B-3's P = 1 shrinks like 1/sqrt(grains per site), i.e. HALVES for each fourfold increase in density
(0.5 -> 2 -> 8). Near-threshold points run 4,000 sweeps (under-running guard); contrast reported at 750, 1,500,
3,000 and 4,000 so flat vs climbing is visible. Committed fraction reported every time.
Usage: python b4e.py DENSITY THG P SWEEPS"""
import sys, json, numpy as np
import b4_grains as g
N = g.N; KAP, L = 0.2, 100
dens, THG, P, T = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4])
S = P / (KAP * L * THG); rng = np.random.default_rng(3)
def contrast(tot):
    cg = tot.reshape(N//8, 8, N//8, 8, N//8, 8).sum(axis=(1, 3, 5)).astype(float); return float(cg.std() / cg.mean())
mob = rng.poisson(dens, (N,)*3).astype(np.int32); com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
for t in range(T + 1):
    if t in (0, 750, 1500, 3000, 4000) or t == T:
        tot = mob + com; rows.append((t, round(float(com.sum()/n0), 2), round(contrast(tot), 3), int(tot.max()), int(tot.sum()) == n0))
    if t == T: break
    r = 1.0 / (1.0 + S * g.nbhd(com)); nfree = g.nbhd(mob)
    cm = rng.binomial(mob, KAP * (nfree >= THG)); dv = rng.binomial(com, 1.0 / L)
    mob = mob - cm + dv; com = com + cm - dv
    mob = g.sweep_independent(mob, r, rng)
line = f"density {dens} THG {THG} P={P:4.2f} T={T}  (t, committed, contrast, max/site): {[r[:4] for r in rows]}  conserved: {all(r[4] for r in rows)}"
print(line, flush=True)
json.dump(dict(density=dens, THG=THG, P=P, S=S, T=T, rows=rows), open(f"b4e_d{dens}_P{P}.json", "w"))
