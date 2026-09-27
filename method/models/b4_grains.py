"""Model B-4: the ink drop made of GRAINS, to test exclusion properly (written before running).

Why grains: for a smooth ink, exclusion cancels exactly (flow x->y D rho_x(1-rho_y) minus y->x D rho_y(1-rho_x)
= D(rho_x - rho_y)), so it can only matter grain by grain (the coffee paper's setting).

2 x 2 design, same everything else:
  grains     : INDEPENDENT (any number per site)      vs  EXCLUSION (at most one grain per site)
  ED rules   : OFF (grains just wander)                vs  ON (commit / slow clocks / dissolve after hbar)
The independent-grains column is the control the other session asked for: it isolates exclusion from graininess.

Grid 64^3, periodic. Start: a sphere of radius 0.35 N filled one grain per site (18% of sites), none outside.
Movement: 6 sub-steps per sweep (3 axes x 2 directions); each mobile grain attempts a hop with probability 0.5 x r.
  Exclusion: hops into occupied sites are refused (implemented as swaps on disjoint bonds).
  Independent: the same bond schedule, hops never refused (fixed 2026-09-25: the first version used a
  different schedule and wandered 3.8x slower, which confounded the comparison).
ED rules ON (once per sweep): local count n = grains in the 3x3x3 neighbourhood.
  commit   : a mobile grain with n >= THG commits with probability KAP (becomes immobile, 'settled')
  clocks   : a mobile grain's hop probability is scaled by r = 1/(1 + S * committed grains in its neighbourhood)
  dissolve : a committed grain becomes mobile again with probability 1/L per sweep  (L = hbar)
Measured every 100 sweeps: apparent complexity (coarse block 8 -> 8^3 cells, bins one mean wide and centred, zlib; calibrated: random grains 14, drop 63, planted blobs 153),
committed fraction, grain count (must be exact), and a calibration of the instrument on random grain placements.
Expectations, recorded in advance:
  E1  ED OFF: exclusion and independent grains both blur; exclusion's field is a little smoother (sub-Poisson).
      Any complexity bump beyond the blurring edge is small in both (3D, large blocks).
  E2  ED ON, independent grains: clumps, as B-3 (grains can pile up without limit).
  E3  ED ON, exclusion: grains CANNOT pile past one per site, so clumps are capped. Open question, no prediction
      of the answer: do they spread into sheets / foams / fingers instead, or simply fail to form?
"""
import sys, zlib, json, time
import numpy as np
from scipy import ndimage

N, B = 64, 8
THG, KAP = 12, 0.2


def start(rng):
    x = np.indices((N, N, N)) - (N - 1) / 2
    return (np.sqrt((x ** 2).sum(0)) < 0.35 * N).astype(np.int32)


def nbhd(a):
    return np.rint(ndimage.uniform_filter(a.astype(float), size=3, mode="wrap") * 27).astype(np.int32)


def complexity(tot):
    cg = tot.reshape(N // B, B, N // B, B, N // B, B).sum(axis=(1, 3, 5)).astype(float)
    q = np.clip(np.floor(cg / cg.mean() * 1 + 0.5), 0, 15).astype(np.uint8)
    return len(zlib.compress(q.tobytes(), 9))


def sweep_exclusion(mob, com, r, rng):
    occ = mob + com
    for ax in range(3):
        for par in (0, 1):
            sl_a = [slice(None)] * 3; sl_b = [slice(None)] * 3
            sl_a[ax] = slice(par, N, 2); idx_b = (np.arange(par, N, 2) + 1) % N
            A = mob[tuple(sl_a)]; Bm = np.take(mob, idx_b, axis=ax)
            oA = occ[tuple(sl_a)]; oB = np.take(occ, idx_b, axis=ax)
            rA = r[tuple(sl_a)]; rB = np.take(r, idx_b, axis=ax)
            u = rng.random(A.shape)
            a_to_b = (A == 1) & (oB == 0) & (u < 0.5 * rA)
            b_to_a = (Bm == 1) & (oA == 0) & (u < 0.5 * rB)
            dA = -a_to_b.astype(np.int32) + b_to_a
            mob[tuple(sl_a)] += dA; occ[tuple(sl_a)] += dA
            cur = np.take(mob, idx_b, axis=ax) - dA; curo = np.take(occ, idx_b, axis=ax) - dA
            sl_b[ax] = idx_b
            mob[tuple(sl_b)] = cur; occ[tuple(sl_b)] = curo
    return mob


def sweep_independent(mob, r, rng):
    """Same bond schedule as sweep_exclusion (3 axes x 2 parities, disjoint bonds), but grains never block:
    each grain on either end of a bond crosses it with probability 0.5 x r. So the ONLY difference between
    the two columns is whether two grains may share a site."""
    for ax in range(3):
        for par in (0, 1):
            sl_a = [slice(None)] * 3; sl_a[ax] = slice(par, N, 2); sl_a = tuple(sl_a)
            idx_b = (np.arange(par, N, 2) + 1) % N
            A = mob[sl_a]; Bm = np.take(mob, idx_b, axis=ax)
            rA = r[sl_a]; rB = np.take(r, idx_b, axis=ax)
            a_to_b = rng.binomial(A, 0.5 * rA); b_to_a = rng.binomial(Bm, 0.5 * rB)
            dA = -a_to_b + b_to_a
            newA = A + dA; newB = Bm - dA
            mob[sl_a] = newA
            sl_b = [slice(None)] * 3; sl_b[ax] = idx_b; mob[tuple(sl_b)] = newB
    return mob


def run(excl, ed, S=10.0, L=100, T=4000, every=100, seed=1):
    rng = np.random.default_rng(seed)
    mob = start(rng); com = np.zeros_like(mob); n0 = int(mob.sum()); rows = []
    for t in range(T + 1):
        if t % every == 0:
            tot = mob + com
            rows.append(dict(t=t, K=complexity(tot), cfrac=float(com.sum() / n0), grains=int(tot.sum()),
                             maxsite=int(tot.max())))
        if t == T:
            break
        if ed:
            r = 1.0 / (1.0 + S * nbhd(com))
            n = nbhd(mob + com)
            commit = rng.binomial(mob, KAP * (n >= THG))
            dissolve = rng.binomial(com, 1.0 / L)
            mob = mob - commit + dissolve; com = com + commit - dissolve
        else:
            r = np.ones(mob.shape)
        mob = sweep_exclusion(mob, com, r, rng) if excl else sweep_independent(mob, r, rng)
    return rows


def calibration(rng):
    n = int(start(rng).sum())
    flat = np.zeros(N ** 3, np.int32); flat[rng.choice(N ** 3, n, replace=False)] = 1
    pois = np.bincount(rng.integers(0, N ** 3, n), minlength=N ** 3)
    return dict(exclusion_random=complexity(flat.reshape((N,) * 3)), independent_random=complexity(pois.reshape((N,) * 3)),
                drop=complexity(start(rng)))


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    out = {"calibration": calibration(rng), "runs": []}
    print("calibration:", out["calibration"], flush=True)
    T = int(sys.argv[1]) if len(sys.argv) > 1 else 4000
    for ed in (False, True):
        for excl in (False, True):
            t0 = time.time(); rows = run(excl, ed, T=T)
            K = [r["K"] for r in rows]; i = int(np.argmax(K))
            summ = dict(ed=ed, exclusion=excl, K0=K[0], Kpeak=K[i], t_peak=rows[i]["t"], Kend=K[-1],
                        cfrac_end=rows[-1]["cfrac"], maxsite_end=rows[-1]["maxsite"],
                        grains_ok=len({r["grains"] for r in rows}) == 1, secs=round(time.time() - t0))
            out["runs"].append(dict(summary=summ, rows=rows)); print(summ, flush=True)
    json.dump(out, open(f"b4_grains_T{T}.json", "w"))
