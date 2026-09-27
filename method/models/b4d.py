"""B-4d: pinning the grain switch, and WHY it is shifted (written before running; design from the other session).
Independent grains, B-3's commit rule (free grains only). Two densities: occupancy 0.5 (THG = 6, as B-4c) and 2.0
(THG = 24, threshold scaled with density so the committed fraction stays comparable). P_grain = S x KAP x L x THG.
Points: P = 0 (baseline, density 2.0 only - density 0.5's baseline is B-4c's), 2.5, 4, 6 at each density.
PREDICTIONS: noise hypothesis -> the switch sits LOWER (closer to B-3's 1) at density 2.0 than at 0.5 (half the
relative noise); threshold-mapping hypothesis -> the switch sits at the same P at both densities.
Read each run against its own density's P = 0 baseline (within-column ratio), and by whether contrast is still
CLIMBING at the end (contrast at 1,500 vs 750 sweeps)."""
import json, numpy as np
import b4_grains as g
N = g.N; KAP, L = 0.2, 100
def contrast(tot):
    cg = tot.reshape(N//8, 8, N//8, 8, N//8, 8).sum(axis=(1, 3, 5)).astype(float); return float(cg.std() / cg.mean())
out = []
runs = [(2.0, 24, 0.0)] + [(dens, thg, P) for dens, thg in ((0.5, 6), (2.0, 24)) for P in (2.5, 4.0, 6.0)]
for dens, THG, P in runs:
    S = P / (KAP * L * THG); rng = np.random.default_rng(3)
    mob = rng.poisson(dens, (N,)*3).astype(np.int32); com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
    for t in range(1501):
        if t % 250 == 0:
            tot = mob + com; rows.append((t, round(float(com.sum()/n0), 2), round(contrast(tot), 3), int(tot.max()), int(tot.sum()) == n0))
        if t == 1500: break
        r = 1.0 / (1.0 + S * g.nbhd(com)); nfree = g.nbhd(mob)
        cm = rng.binomial(mob, KAP * (nfree >= THG)); dv = rng.binomial(com, 1.0 / L)
        mob = mob - cm + dv; com = com + cm - dv
        mob = g.sweep_independent(mob, r, rng)
    out.append(dict(density=dens, THG=THG, P=P, S=S, rows=rows))
    print(f"density {dens} P={P:3.1f}  (t, committed, contrast, max/site): {[r[:4] for r in rows]}  climbing: {rows[-1][2] > 1.1*rows[3][2]}  conserved: {all(r[4] for r in rows)}", flush=True)
json.dump(out, open("b4d.json", "w"), indent=1)
