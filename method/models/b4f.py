"""B-4f: bracket the densest setting from below, and test nucleation (written before running; design from the
other session). Contrast recorded every 500 sweeps, so a waiting time followed by takeoff is visible.
(a) density 8.0 (THG 96), P = 0.75 and 1.0, seeds 4 and 5, 6,000 sweeps. A point counts as NO structure only
    if BOTH seeds stay flat throughout; if one takes off and one doesn't, that is itself a result (stochastic onset).
(b) density 2.0 (THG 24), P = 1.5, seeds 4 and 5, 5,000 sweeps (seed 3 took off late, near 3,000-4,000).
PREDICTION (nucleation): takeoff times scatter widely between seeds. Amplitude noise instead: reproducible onset,
steady growth from the start. 'Takeoff' = first checkpoint where contrast exceeds 2x the density's P = 0 baseline
(0.079 at density 2.0 from B-4e P 1.0 plateau is NOT a baseline; baselines: 0.056 at 2.0, 0.039 at 8.0).
Usage: python b4f.py DENSITY THG P SWEEPS SEED"""
import sys, json, numpy as np
import b4_grains as g
N = g.N; KAP, L = 0.2, 100
dens, THG, P, T, seed = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
S = P / (KAP * L * THG); rng = np.random.default_rng(seed)
BASE = {2.0: 0.056, 8.0: 0.039}[dens]
def contrast(tot):
    cg = tot.reshape(N//8, 8, N//8, 8, N//8, 8).sum(axis=(1, 3, 5)).astype(float); return float(cg.std() / cg.mean())
mob = rng.poisson(dens, (N,)*3).astype(np.int32); com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
for t in range(T + 1):
    if t % 500 == 0:
        tot = mob + com; rows.append((t, round(float(com.sum()/n0), 2), round(contrast(tot), 3), int(tot.max()), int(tot.sum()) == n0))
    if t == T: break
    r = 1.0 / (1.0 + S * g.nbhd(com)); nfree = g.nbhd(mob)
    cm = rng.binomial(mob, KAP * (nfree >= THG)); dv = rng.binomial(com, 1.0 / L)
    mob = mob - cm + dv; com = com + cm - dv
    mob = g.sweep_independent(mob, r, rng)
take = next((r[0] for r in rows if r[2] > 2 * BASE), None)
print(f"density {dens} P={P:4.2f} seed {seed}: takeoff at {take} | (t, committed, contrast, max/site): {[r[:4] for r in rows]} conserved: {all(r[4] for r in rows)}", flush=True)
json.dump(dict(density=dens, P=P, seed=seed, takeoff=take, rows=rows), open(f"b4f_d{dens}_P{P}_s{seed}.json", "w"))
