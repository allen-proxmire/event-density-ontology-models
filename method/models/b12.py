"""Model B-12: structure condensing out of the One Being.
Start: uniform free becoming rho0 = 3 (above theta = 2), nothing committed, ONE PHASE everywhere (the One Being:
all possibilities uncommitted, nothing distinguished), plus a 1e-3 density ripple (the first difference).
Phase scatter at the start is the variable: sigma = 0 (exact One Being), 0.3, 1.0 rad, or fully scrambled.
Rules: B-9/B-11 (phase travels with the stuff; slowing = |sqrt(s) w / sqrt(c)|^2), hbar 100, P 20, and both
endings on: expansion h = 1e-4 and spending eps = 0.01 of each dissolution.
Measured every 1,000 steps: committed fraction, alignment R = |sum w| / sum c, clumps, spent, leaked.
PRE-REGISTERED: sigma 0 -> structure condenses, stays aligned (R = 1), full arc back to uniform. Scrambled -> no
lasting structure (as B-11b). In between -> weaker, shorter-lived structure the larger the scatter (mixing
partly cancels). Structure needs a coherent start.
Usage: python b12.py SIGMA SEED   (SIGMA = -1 means fully scrambled)"""
import sys, json, numpy as np
from scipy import ndimage
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P, H, EPS = 100, 20.0, 1e-4, 0.01; s = P / (K * HB * TH)
sig, seed = float(sys.argv[1]), int(sys.argv[2]); rng = np.random.default_rng(seed)
rho = 3.0 * (1 + 1e-3 * rng.standard_normal((N,) * 3))
ph = rng.uniform(0, 2 * np.pi, rho.shape) if sig < 0 else sig * rng.standard_normal(rho.shape)
u = rho * np.exp(1j * ph); c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
tot = rho.sum(); spent = leaked = 0.0; rows = []; peak = 0.0; death = None
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
t = 0
while t <= 150000:
    if t % 1000 == 0:
        cf = float(c.sum() / tot); peak = max(peak, cf); R = float(np.abs(w.sum()) / max(c.sum(), 1e-12))
        lab, n = ndimage.label(c > 0.1)
        rows.append((t, round(cf, 4), round(R, 3), int(n), round(spent / tot, 3), round(leaked / tot, 3)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None or (t > 30000 and peak <= 0.05): break
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    rho, u = flow(rho, r), flow(u, r)
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0)
    du = frac * u; back = c / HB; dw = w / HB
    rho, c = rho - ex + back, c + ex - back; u, w = u - du + dw, w + du - dw
    sp = EPS * back; sw = EPS * dw; rho = rho - sp; u = u - sw; spent += sp.sum()      # spending: part of each dissolution
    lk = 3 * H * rho; rho = rho - lk; u = u * (1 - 3 * H); leaked += lk.sum(); t += 1
drift = abs(rho.sum() + c.sum() + spent + leaked - tot) / tot
out = dict(sigma=sig, seed=seed, death=death, peak=round(peak, 3), rows=rows, drift=float(drift))
print(json.dumps(dict(sigma=sig, seed=seed, death=death, peak=round(peak, 3), rows=rows[::4] + [rows[-1]], drift=drift)), flush=True)
json.dump(out, open(f"b12_sig{sig}_s{seed}.json", "w"))
