"""Step 2-3: the death law with a DERIVED leak term. Written before the peak states were looked at.

The rule's own flow across a face between sites x and y is exactly D*(r_x*rho_x - r_y*rho_y)
(each site sends D*r*rho to each neighbour). So a clump loses free becoming through its surface at
    leak = D * A * (r_in*rho_in - r_out*rho_out)
Treat the densest clump as uniform (THE ONE SIMPLIFICATION - real clumps are denser in the middle):
    V   = number of sites in it, A = number of faces between it and the outside     (counted at the peak)
    c   = its mean committed density; rho_in = theta + c/(kappa*L)   (local commit balance, as before)
    r_in = 1/(1 + s*c);  outside: r_out = 1, rho_out = free density of the non-clump sites, which thins as
          rho_out(t) = rho_out(t0) * exp(-3h (t - t0))                                  (measured at the peak)
Mass in the clump m = V*(rho_in + c) = V*(theta + c*(1 + 1/(kappa*L))), so
    dc/dt = -[ 3h*rho_in + (D*A/V)*(r_in*rho_in - rho_out) ] / (1 + 1/(kappa*L))
Integrate from c(t0) until c reaches 0 (the clump can no longer commit): that is the predicted death.
NO fitted number: every input (V, A, c(t0), rho_out(t0), t0) is measured at the peak; D, h, kappa, theta, L, s
are the rule's own values. The bare shielding formula is the same equation with the leak term removed; it is
reported alongside, so the change the leak makes is visible.
Reported: predicted / measured death for each case. Target (Allen / other session): the ratio should come to
1.00 without any coefficient being chosen - an upper bound turning into an estimate. If a fitted factor is
needed, it is labelled as one.
"""
import json
import numpy as np
from scipy import ndimage
import b3_card as m

K, TH, D, h = m.KAPPA, m.THETA, m.D, 3e-5
DEATH = {(10, 1.0): 16000, (10, 10.0): 62500, (100, 1.0): 152000, (100, 10.0): 359000}


def clump_geometry(c):
    lab, n = ndimage.label(c > 0.1, structure=ndimage.generate_binary_structure(3, 1))
    k = lab[np.unravel_index(np.argmax(c), c.shape)]
    mask = lab == k
    A = sum(int((mask & ~np.roll(mask, sh, ax)).sum()) for ax in range(3) for sh in (1, -1))
    return mask, int(mask.sum()), A


def predict(c0, V, A, rho_out0, t0, L, s, leak=True, dt=1.0, tmax=2_000_000):
    c, t = c0, 0.0
    while c > 0 and t < tmax:
        rho_in = TH + c / (K * L)
        r_in = 1.0 / (1.0 + s * c)
        rho_out = rho_out0 * np.exp(-3 * h * t)
        loss = 3 * h * rho_in + ((D * A / V) * (r_in * rho_in - rho_out) if leak else 0.0)
        c -= dt * loss / (1 + 1 / (K * L))
        t += dt
    return t0 + t


out = []
print("hbar   s     t0     V    A    c_mean  rho_out   shielding-only   with leak   measured   ratio(shield)  ratio(leak)")
for (L, s), td in DEATH.items():
    z = np.load(f"peak_L{L}_s{int(s)}.npz")
    rho, c, t0 = z["rho"], z["c"], int(z["t0"])
    mask, V, A = clump_geometry(c)
    cm = float(c[mask].mean())
    rho_out0 = float(rho[c <= 0.1].mean())
    p0 = predict(cm, V, A, rho_out0, t0, L, s, leak=False)
    p1 = predict(cm, V, A, rho_out0, t0, L, s, leak=True)
    d = dict(L=L, s=s, t0=t0, V=V, A=A, c_mean=cm, rho_out0=rho_out0, pred_shield=p0, pred_leak=p1, measured=td,
             ratio_shield=p0 / td, ratio_leak=p1 / td)
    out.append(d)
    print(f"{L:4d} {s:5.1f} {t0:7d} {V:5d} {A:4d} {cm:8.1f} {rho_out0:8.4f}   {p0:10.0f}    {p1:10.0f}   {td:8d}      "
          f"{p0/td:5.2f}         {p1/td:5.2f}", flush=True)
json.dump(out, open("b3_leaklaw.json", "w"), indent=1)
