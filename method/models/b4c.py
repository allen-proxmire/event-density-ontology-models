"""B-4c: grain-level robustness test of B-3 (written before running).
Commit rule now MATCHES B-3: a free grain commits (prob KAP per sweep) when the count of FREE grains in its
3x3x3 neighbourhood is >= THG. Committed grains don't count, so commitment is self-limiting, as in B-3.
Settings chosen for a mid-range committed fraction (B-3 sat at 0.40-0.92): occupancy 0.5, THG = 6.
B-3's switch, translated to grains: P_grain = S x KAP x L x THG (S = slowing per committed grain in the
neighbourhood, L = hbar in sweeps). PREDICTION: structure switches on near P_grain = 1, i.e. S ~ 1/120 = 0.0083,
possibly shifted by grain noise. Sweep P_grain = 0, 0.5, 1, 2, 8, both grain types, 1,500 sweeps, seed 3.
Reported every 250 sweeps: committed fraction, contrast (spread of the coarse-grained field), complexity,
most grains on one site. Grains must be conserved exactly."""
import json, numpy as np
import b4_grains as g
N = g.N; KAP, L, THG = 0.2, 100, 6
def contrast(tot):
    cg = tot.reshape(N//8, 8, N//8, 8, N//8, 8).sum(axis=(1, 3, 5)).astype(float); return float(cg.std() / cg.mean())
out = []
for P in (0.0, 0.5, 1.0, 2.0, 8.0):
    S = P / (KAP * L * THG)
    for excl in (False, True):
        rng = np.random.default_rng(3)
        mob = (rng.random((N,)*3) < 0.5).astype(np.int32) if excl else rng.poisson(0.5, (N,)*3).astype(np.int32)
        com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
        for t in range(1501):
            if t % 250 == 0:
                tot = mob + com
                rows.append((t, round(float(com.sum() / n0), 2), round(contrast(tot), 3), g.complexity(tot), int(tot.max()), int(tot.sum()) == n0))
            if t == 1500: break
            r = 1.0 / (1.0 + S * g.nbhd(com)); nfree = g.nbhd(mob)
            cm = rng.binomial(mob, KAP * (nfree >= THG)); dv = rng.binomial(com, 1.0 / L)
            mob = mob - cm + dv; com = com + cm - dv
            mob = g.sweep_exclusion(mob, com, r, rng) if excl else g.sweep_independent(mob, r, rng)
        out.append(dict(P=P, S=S, exclusion=excl, rows=rows))
        print(f"P={P:3.1f} S={S:.4f} {'exclusion  ' if excl else 'independent'}  (t, committed, contrast, complexity, max/site):",
              [r[:5] for r in rows], " conserved:", all(r[5] for r in rows), flush=True)
json.dump(out, open("b4c.json", "w"), indent=1)
