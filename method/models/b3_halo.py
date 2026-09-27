"""Halo test, with an out-of-sample check. Written before running.

Leak law as before, but the clump leaks into its measured SURROUNDINGS, not the bare background:
    leak = D * A * (r_in*rho_in - p_out(t)),   p_out = mean of r*rho over the sites touching the clump,
    p_out(t) = p_out(t0) * exp(-3h (t - t0))   (the halo thins with everything else).
The halo is summarised by one factor per (hbar, s) cell: g = p_halo(t0) / rho_bg(t0).
IN-SAMPLE: g measured at h = 3e-5, predict deaths at h = 3e-5.
OUT-OF-SAMPLE: g carried over UNCHANGED from h = 3e-5; peak state (c0, V, A, rho_bg, t0) measured at h = 1e-4;
predict deaths at h = 1e-4, which the formula never saw (5,500 / 18,500 / 41,000 / 86,000).
Measured inputs per prediction: 6 (c0, V, A, rho_bg, t0, g). Nothing fitted.
"""
import json, numpy as np
from scipy import ndimage
import b3_card as m
import b3_leaklaw as lk

K, TH, D = m.KAPPA, m.THETA, m.D
DEATH = {3e-5: {(10, 1.0): 16000, (10, 10.0): 62500, (100, 1.0): 152000, (100, 10.0): 359000},
         1e-4: {(10, 1.0): 5500, (10, 10.0): 18500, (100, 1.0): 41000, (100, 10.0): 86000}}


def peak_state(L, s, h):
    try:
        z = np.load(f"peak_L{L}_s{int(s)}" + ("" if h == 3e-5 else f"_h{h:g}") + ".npz")
        return z["rho"], z["c"], int(z["t0"])
    except FileNotFoundError:
        rng = np.random.default_rng(1)
        rho, c = m.drop(rng, 1e-3)
        best, t0, st = 0.0, 0, None
        for t in range(400000):
            rho, c = m.step(rho, c, s, L); rho = rho - 3 * h * rho
            if t % 200 == 0:
                cm = float(c.max())
                if cm > best: best, t0, st = cm, t, (rho.copy(), c.copy())
                elif cm < 0.8 * best or cm < 1e-6: break
        np.savez(f"peak_L{L}_s{int(s)}_h{h:g}.npz", rho=st[0], c=st[1], t0=t0)
        return st[0], st[1], t0


def measure(rho, c, s):
    lab, n = ndimage.label(c > 0.1, structure=ndimage.generate_binary_structure(3, 1))
    k = lab[np.unravel_index(np.argmax(c), c.shape)]; mask = lab == k
    V = int(mask.sum()); A = sum(int((mask & ~np.roll(mask, sh, ax)).sum()) for ax in range(3) for sh in (1, -1))
    shell = ndimage.binary_dilation(mask, structure=ndimage.generate_binary_structure(3, 1)) & ~mask
    r = 1 / (1 + s * c)
    p_halo = float((r * rho)[shell].mean()); rho_bg = float(rho[c <= 0.1].mean())
    return V, A, float(c[mask].mean()), rho_bg, p_halo


def predict(c0, V, A, p_out0, t0, L, s, h, dt=10.0):
    c, t = c0, 0.0
    while c > 0 and t < 5e6:
        rho_in = TH + c / (K * L); r_in = 1 / (1 + s * c)
        loss = 3 * h * rho_in + (D * A / V) * (r_in * rho_in - p_out0 * np.exp(-3 * h * t))
        c -= dt * loss / (1 + 1 / (K * L)); t += dt
    return t0 + t


out = []; g = {}
print("IN-SAMPLE, h = 3e-5 (halo measured here)")
print("hbar   s   halo factor g   no-halo ratio   halo ratio")
for (L, s), td in DEATH[3e-5].items():
    rho, c, t0 = peak_state(L, s, 3e-5)
    V, A, cm, bg, ph = measure(rho, c, s)
    g[(L, s)] = ph / bg
    p0 = predict(cm, V, A, bg, t0, L, s, 3e-5); p1 = predict(cm, V, A, ph, t0, L, s, 3e-5)
    out.append(dict(kind="in", h=3e-5, L=L, s=s, g=g[(L, s)], ratio_nohalo=p0 / td, ratio_halo=p1 / td))
    print(f"{L:4d} {s:5.1f}   {g[(L, s)]:10.2f}      {p0/td:8.2f}      {p1/td:8.2f}", flush=True)
print("\nOUT-OF-SAMPLE, h = 1e-4 (halo factor carried over from 3e-5; deaths never seen by the formula)")
print("hbar   s   no-halo ratio   halo ratio   (halo factor measured here, for reference only)")
for (L, s), td in DEATH[1e-4].items():
    rho, c, t0 = peak_state(L, s, 1e-4)
    V, A, cm, bg, ph = measure(rho, c, s)
    p0 = predict(cm, V, A, bg, t0, L, s, 1e-4); p1 = predict(cm, V, A, g[(L, s)] * bg, t0, L, s, 1e-4)
    out.append(dict(kind="out", h=1e-4, L=L, s=s, g_used=g[(L, s)], g_here=ph / bg, ratio_nohalo=p0 / td, ratio_halo=p1 / td))
    print(f"{L:4d} {s:5.1f}   {p0/td:8.2f}      {p1/td:8.2f}      ({ph/bg:.2f})", flush=True)
json.dump(out, open("b3_halo.json", "w"), indent=1)
