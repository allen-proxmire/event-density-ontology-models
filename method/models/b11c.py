"""B-11c: which drops survive, and does it depend on their phase relative to the BACKGROUND?
(Written after B-11 / B-11b, before this run.) B-11 (coherent background, phase 0): mixed-phase drops left lasting
structure at flat partial alignment. B-11b (incoherent background): every random-phase drop died by ~2,000 steps,
while in-step drops survived. Hypothesis, written now: a drop survives if its phase is close to the phase of the
stuff around it (the background), not according to its phase relative to other drops.
Test: B-11's setup (background phase 0), 10,000 steps; per drop, committed stuff within its starting sphere at the
end, against |drop phase| (distance from the background's phase 0)."""
import sys, json, numpy as np
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P = 100, 20.0; s = P / (K * HB * TH)
seed = int(sys.argv[1]); rng = np.random.default_rng(seed); x = np.indices((N,) * 3)
rho = np.full((N,) * 3, 0.5); u = rho.astype(complex)
phases = rng.uniform(0, 2 * np.pi, 10); blobs = []
for k in range(10):
    c0 = rng.integers(0, N, 3); d2 = sum(((x[i] - c0[i] + N // 2) % N - N // 2) ** 2 for i in range(3))
    b = d2 < 16; blobs.append(b); rho[b] = 8.0; u[b] = 8.0 * np.exp(1j * phases[k])
rho *= (1 + 1e-3 * rng.standard_normal(rho.shape)); u *= rho / np.maximum(np.abs(u), 1e-30)
c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
for t in range(10000):
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    rho, u = flow(rho, r), flow(u, r)
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0)
    du = frac * u; back = c / HB; dw = w / HB
    rho, c = rho - ex + back, c + ex - back; u, w = u - du + dw, w + du - dw
res = []
for k in range(10):
    dphi = abs((phases[k] + np.pi) % (2 * np.pi) - np.pi) / np.pi   # distance from background phase, in units of pi
    res.append((round(float(dphi), 2), round(float(c[blobs[k]].sum()), 1)))
res.sort(); print(json.dumps(dict(seed=seed, drops=res)), flush=True)
