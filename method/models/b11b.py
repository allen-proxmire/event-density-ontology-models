"""B-11b: rerun with an INCOHERENT background (random phase per site). The first run gave the background phase 0,
which biases the alignment measure toward phase 0. Same pre-registration.
Model B-11: is polarity SELECTED? (Allen chose to test the working answer to 'what sets relative polarity?')
One species, hbar fixed (100), P 20, NO expansion (so any death is by cancellation, not thinning).
Start: 10 small drops (radius 4, contrast 8 over background 0.5) at random positions, each with its own phase.
Phase travels with the stuff (P05, trivial connection); slowing = |sqrt(s) w / sqrt(c)|^2 per site (B-9's rule;
stuff of different phases at one site partly cancels in w).
Measured every 1,000 steps: committed fraction; ALIGNMENT R = |sum of w| / sum of c over the whole grid
(1 = all committed stuff in step; about 1/sqrt(10) ~ 0.3 for ten random phases); number of clumps.
PRE-REGISTERED: selection -> R rises over time toward 1 while a fair share of structure survives.
Alternatives written down: (a) everything cancels (committed fraction -> ~0); (b) R stays random (drops never
meet or never interact). Control: all ten drops in step (R = 1 throughout; the baseline for surviving structure).
Usage: python b11.py SEED ALIGNED"""
import sys, json, numpy as np
from scipy import ndimage
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P = 100, 20.0; s = P / (K * HB * TH)
seed, aligned = int(sys.argv[1]), sys.argv[2] == "1"
rng = np.random.default_rng(seed)
x = np.indices((N,) * 3)
rho = np.full((N,) * 3, 0.5); u = rho * np.exp(1j * rng.uniform(0, 2 * np.pi, rho.shape))   # background INCOHERENT (fix: first run gave it phase 0)
phases = np.zeros(10) if aligned else rng.uniform(0, 2 * np.pi, 10)
for k in range(10):
    c0 = rng.integers(0, N, 3)
    d2 = sum(((x[i] - c0[i] + N // 2) % N - N // 2) ** 2 for i in range(3))
    blob = d2 < 16
    rho[blob] = 8.0; u[blob] = 8.0 * np.exp(1j * phases[k])
rho *= (1 + 1e-3 * rng.standard_normal(rho.shape)); u *= rho / np.maximum(np.abs(u), 1e-30)
c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex); tot = rho.sum(); rows = []
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
for t in range(40001):
    if t % 1000 == 0:
        R = float(np.abs(w.sum()) / max(c.sum(), 1e-12)); lab, n = ndimage.label(c > 0.1)
        rows.append((t, round(float(c.sum() / tot), 3), round(R, 3), int(n)))
    if t == 40000: break
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    rho, u = flow(rho, r), flow(u, r)
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0)
    du = frac * u; back = c / HB; dw = w / HB
    rho, c = rho - ex + back, c + ex - back; u, w = u - du + dw, w + du - dw
drift = abs(rho.sum() + c.sum() - tot) / tot
start_R = float(abs(np.exp(1j * phases).sum()) / 10)
out = dict(seed=seed, aligned=aligned, phase_order_at_start=round(start_R, 3), rows=rows, drift=float(drift))
print(json.dumps(dict(seed=seed, aligned=aligned, R_start=round(start_R, 3), rows=rows[::5], last=rows[-1])), flush=True)
json.dump(out, open(f"b11b_s{seed}_a{int(aligned)}.json", "w"))
