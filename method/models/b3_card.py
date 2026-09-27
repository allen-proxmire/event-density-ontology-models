"""Model B-3, the ink drop, built as the card specifies (Model_B-3_Ink_Drop_Card.md).

Two amounts per site of a periodic 3D grid: rho (free) and c (committed). Total conserved.
Each step:
  1. clocks: r = 1 / (1 + s*c)
  2. flow: every site sends D*r*rho to each of its 6 neighbours  (becoming lingers where clocks are slow)
  3. commit: where rho > theta, a fraction kappa of the excess moves rho -> c
     dissolve: c returns to rho at rate 1/L   (L = hbar, memory before dissolving)
Observables along the trajectory: coarse entropy, apparent complexity (zlib size of coarse-grained,
quantised total field), committed fraction, committed clusters.
"""
import sys, zlib, json
import numpy as np
from scipy import ndimage

N, D, THETA, KAPPA = 32, 0.1, 2.0, 0.2
B = 4                      # coarse-graining block


def drop(rng, eps, radius=0.22, contrast=8.0):
    x = np.indices((N, N, N)) - (N - 1) / 2
    rr = np.sqrt((x ** 2).sum(0))
    rho = np.where(rr < radius * N, contrast, 1.0)
    rho = rho * (1 + eps * rng.standard_normal(rho.shape))
    return rho, np.zeros_like(rho)


def coarse(f):
    return f.reshape(N // B, B, N // B, B, N // B, B).mean(axis=(1, 3, 5))


def entropy(tot):
    p = coarse(tot).ravel(); p = p / p.sum()
    return float(-(p * np.log(p)).sum() / np.log(p.size))


def complexity(tot):
    cg = coarse(tot)
    q = np.clip(np.floor(cg / tot.mean() * 3 + 0.5), 0, 15).astype(np.uint8)
    return len(zlib.compress(q.tobytes(), 9))


def step(rho, c, s, L):
    r = 1.0 / (1.0 + s * c)
    send = D * r * rho
    inflow = sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
    rho = rho - 6 * send + inflow
    ex = np.maximum(rho - THETA, 0.0) * KAPPA
    back = c / L
    return rho - ex + back, c + ex - back


def clusters(c):
    lab, n = ndimage.label(c > 0.1)
    if n == 0:
        return 0, 0
    sizes = np.bincount(lab.ravel())[1:]
    return int(n), int(sizes.max())


def run(s, L, seed, eps=1e-3, T=20000, every=250):
    rng = np.random.default_rng(seed)
    rho, c = drop(rng, eps)
    total0 = (rho + c).sum()
    rows = []
    for t in range(T + 1):
        if t % every == 0:
            tot = rho + c
            n, big = clusters(c)
            rows.append(dict(t=t, S=entropy(tot), K=complexity(tot), cfrac=float(c.sum() / tot.sum()),
                             ncl=n, big=big, spread=float(tot.std() / tot.mean())))
        if t < T:
            rho, c = step(rho, c, s, L)
    drift = abs((rho + c).sum() - total0) / total0
    return rows, drift, rho, c


def calibrate():
    rng = np.random.default_rng(1)
    uni = np.ones((N, N, N))
    noise = 1 + 0.5 * rng.standard_normal((N, N, N)).clip(-1.9, 1.9)
    blobs = np.ones((N, N, N))
    x = np.indices((N, N, N))
    for _ in range(12):
        c0 = rng.integers(0, N, 3)
        d2 = sum(((x[i] - c0[i] + N // 2) % N - N // 2) ** 2 for i in range(3))
        blobs += 6 * (d2 < rng.integers(4, 16))
    rho, _ = drop(rng, 0)
    return {k: complexity(v) for k, v in dict(uniform=uni, noise=noise, blobs=blobs, drop=rho).items()}


if __name__ == "__main__":
    out = {"calibration": calibrate(), "runs": []}
    print("calibration (complexity, bytes):", out["calibration"]); sys.stdout.flush()
    for L in (10, 100):
        for s in (0.0, 0.3, 1.0, 3.0, 10.0):
            for seed in (1, 2):
                rows, drift, rho, c = run(s, L, seed)
                K = [r["K"] for r in rows]; S = [r["S"] for r in rows]
                ipk = int(np.argmax(K))
                dS = min(np.diff(S))
                summ = dict(L=L, s=s, seed=seed, K0=K[0], Kpeak=K[ipk], t_peak=rows[ipk]["t"], Kend=K[-1],
                            cfrac_end=rows[-1]["cfrac"], ncl_end=rows[-1]["ncl"], big_end=rows[-1]["big"],
                            spread_end=rows[-1]["spread"], S_min_step=float(dS), drift=float(drift))
                out["runs"].append(dict(summary=summ, rows=rows))
                print(summ); sys.stdout.flush()
    # symmetry check, eps = 0
    rows, drift, rho, c = run(3.0, 100, 1, eps=0.0, T=4000)
    tot = rho + c
    out["symmetry_err"] = float(np.abs(tot - tot[::-1, :, :]).max() / tot.max())
    print("eps=0 mirror asymmetry:", out["symmetry_err"])
    json.dump(out, open(sys.argv[1] if len(sys.argv) > 1 else "b3_card.json", "w"))
