"""B-4b, the corrected grain experiment (written before running). Both grain types now share one move schedule
(dilute wander 5.87 vs 5.76 per sweep), so exclusion is the only difference between the two columns.
PART 1 (ED off): the drop, 1,000 sweeps - complexity trajectory, exclusion vs independent.
PART 2 (ED on): a UNIFORM random field of grains at occupancy 0.5 (neighbourhood count ~13.5, just above the
commit threshold 12), so there is no packed drop to freeze. Clock slowing S = 0 (no amplifier) or S = 10;
exclusion or not. 2,000 sweeps. Measured: complexity; committed fraction; most grains on one site; committed
pieces and the largest piece's share; contrast (std / mean of the coarse-grained total).
Expectations: S = 0 gives no lasting structure in either column (no amplifier). S = 10, independent: clumps
(grains pile up, as in B-3). S = 10, exclusion: no prediction - capped clumps, sheets, foam, or nothing."""
import json, numpy as np
from scipy import ndimage
import b4_grains as g
N = g.N; out = {"part1": [], "part2": []}

def contrast(tot):
    cg = tot.reshape(N//8, 8, N//8, 8, N//8, 8).sum(axis=(1, 3, 5)).astype(float); return float(cg.std() / cg.mean())

print("PART 1 - drop, ED off (complexity every 100 sweeps)")
for excl in (False, True):
    rng = np.random.default_rng(1); mob = g.start(rng); com = np.zeros_like(mob); r = np.ones(mob.shape); Ks = []
    for t in range(1001):
        if t % 100 == 0: Ks.append(g.complexity(mob))
        if t < 1000: mob = g.sweep_exclusion(mob, com, r, rng) if excl else g.sweep_independent(mob, r, rng)
    out["part1"].append(dict(exclusion=excl, K=Ks)); print(" ", "exclusion  " if excl else "independent", Ks, flush=True)

print("PART 2 - uniform field at occupancy 0.5, ED on")
for S in (0.0, 10.0):
    for excl in (False, True):
        rng = np.random.default_rng(2)
        if excl: mob = (rng.random((N,)*3) < 0.5).astype(np.int32)
        else: mob = rng.poisson(0.5, (N,)*3).astype(np.int32)
        com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
        for t in range(2001):
            if t % 250 == 0:
                tot = mob + com; lab, k = ndimage.label(com > 0); sz = np.bincount(lab.ravel())[1:]
                rows.append(dict(t=t, K=g.complexity(tot), cfrac=round(float(com.sum()/n0), 3), maxsite=int(tot.max()),
                                 pieces=int(k), largest=round(float(sz.max()/sz.sum()) if k else 0.0, 3),
                                 contrast=round(contrast(tot), 3), ok=int(tot.sum()) == n0))
            if t == 2000: break
            r = 1.0 / (1.0 + S * g.nbhd(com)); n = g.nbhd(mob + com)
            cm = rng.binomial(mob, g.KAP * (n >= g.THG)); dv = rng.binomial(com, 1.0 / 100)
            mob = mob - cm + dv; com = com + cm - dv
            mob = g.sweep_exclusion(mob, com, r, rng) if excl else g.sweep_independent(mob, r, rng)
        out["part2"].append(dict(S=S, exclusion=excl, rows=rows))
        print(f"  S={S:4.1f} {'exclusion  ' if excl else 'independent'}", [(x['t'], x['K'], x['cfrac'], x['maxsite'], x['pieces'], x['largest'], x['contrast']) for x in rows[::2]] , "grains conserved:", all(x['ok'] for x in rows), flush=True)
json.dump(out, open("b4b.json", "w"), indent=1)
