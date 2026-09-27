"""Model B-14 - variation at commitment, selection by the flow. Built from cards/Model_B-14_Commitment_Phase_Filter.md.
Base: B-12 (uniform rho0 = 3, 1e-3 ripple; hbar 100, P 20; expansion h 1e-4; spending eps 0.01; phase travels
with the stuff; slowing = |sqrt(s) w / sqrt(c)|^2).  New at the commitment gate:
  RANDOMIZATION (P11): each step's committing stuff at a site proposes a fresh phase, uniform on U(1).
  FILTER (tension_polarity s124): the proposal commits only if phase-compatible with the local flow.
    Allen's s2 decision (2026-09-26, option (a) as recommended, "go ahead"): the medium supplies the angle, the flow
    supplies the sign. Angle = phase of the local medium (summed free amplitude of the site and its 6 neighbours).
    Sign = is stuff GATHERING at the site this step (net inflow > 0: target = medium phase) or DISPERSING (target =
    medium phase + pi). Time reversal swaps gathering and dispersing, so it adds half a turn (the file's constraint).
  Accept if |proposal - target| < W/2 (acceptance width W, swept). Accepted: commits with the proposed phase at
  full magnitude. Rejected: decoheres - the stuff stays free, and its amplitude is lost (no definite phase).
Arms: 0 no randomization, no filter (must reproduce B-12); 1 randomization, no filter; 2 filter (a);
      3 filter (b): global reference 0 with the same gathering/dispersing sign (answer handed in);
      4 phase-blind filter: accept with probability = arm 2's measured acceptance fraction (matched rejection);
      5 (added after review, the other session's design): target = a FROZEN SMOOTH RANDOM angle field, unrelated to the
        medium and not a constant, same gathering/dispersing sign. Tests whether ANY locally consistent target will do.
Measured every 1,000 steps: committed fraction; committed alignment Rc = |sum w|/sum c; medium alignment
Rm = |sum u|/sum |u| WITH surviving amplitude A = sum|u| / sum|u|(t=0) - Rm VOID when A < 0.1 (written before use);
acceptance fraction; spent; leaked.  FLOW-SIGN TEST (added after review): env B14_NOSIGN=1 removes the gathering/dispersing
sign, so every commitment aims at the same target wherever it is.  Usage: python b14.py ARM START W SEED [PACC]  (START: scr | one ; W in units of pi)"""
import sys, json, numpy as np
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P, H, EPS = 100, 20.0, 1e-4, 0.01; s = P / (K * HB * TH)
arm, start, W, seed = int(sys.argv[1]), sys.argv[2], float(sys.argv[3]) * np.pi, int(sys.argv[4])
pacc = float(sys.argv[5]) if len(sys.argv) > 5 else None
import os; NOSIGN = os.environ.get('B14_NOSIGN') == '1'
rng = np.random.default_rng(seed)
rho = 3.0 * (1 + 1e-3 * rng.standard_normal((N,) * 3))
ph = rng.uniform(0, 2 * np.pi, rho.shape) if start == "scr" else np.zeros(rho.shape)
u = rho * np.exp(1j * ph); c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
tot = rho.sum(); A0 = np.abs(u).sum(); spent = leaked = 0.0; prop = accd = 0.0
rows = []; peak = 0.0; death = None
if arm == 5:
    from scipy import ndimage
    fr = np.random.default_rng(seed + 100); z = np.exp(1j * fr.uniform(0, 2 * np.pi, rho.shape))
    z = ndimage.gaussian_filter(z.real, 3, mode='wrap') + 1j * ndimage.gaussian_filter(z.imag, 3, mode='wrap')
    frozen = np.angle(z)
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
t = 0
while t <= 150000:
    if t % 1000 == 0:
        cf = float(c.sum() / tot); peak = max(peak, cf)
        A = float(np.abs(u).sum() / A0); Rm = float(np.abs(u.sum()) / max(np.abs(u).sum(), 1e-30))
        Rc = float(np.abs(w.sum()) / max(c.sum(), 1e-12))
        rows.append(dict(t=t, cf=round(cf, 4), Rc=round(Rc, 3), Rm=(round(Rm, 3) if A >= 0.1 else "void"), A=round(A, 3),
                         acc=round(accd / prop, 3) if prop > 0 else None, spent=round(spent / tot, 3), leaked=round(leaked / tot, 3)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None or (t > 30000 and peak <= 0.05): break
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    rho_before = rho
    rho, u = flow(rho, r), flow(u, r)
    gather = (rho - rho_before) > 0
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0); du = frac * u
    if arm == 0:
        rho, c = rho - ex, c + ex; u, w = u - du, w + du
    else:
        theta = rng.uniform(0, 2 * np.pi, rho.shape)
        if arm == 1:
            acc = np.ones(rho.shape, bool)
        elif arm in (2, 3, 5):
            med = u + sum(np.roll(u, sh, ax) for ax in range(3) for sh in (1, -1))
            base = np.angle(med) if arm == 2 else (frozen if arm == 5 else 0.0)
            target = base + (0.0 if NOSIGN else np.where(gather, 0.0, np.pi))
            acc = np.abs(wrap(theta - target)) < W / 2
        else:
            acc = rng.random(rho.shape) < pacc
        exa = ex * acc; prop += ex.sum(); accd += exa.sum()
        rho, c = rho - exa, c + exa
        u = u - du                                  # accepted: amplitude leaves with the commit; rejected: decoheres
        w = w + exa * np.exp(1j * theta)
    back = c / HB; dw = w / HB
    rho, c = rho + back, c - back; u, w = u + dw, w - dw
    sp = EPS * back; rho = rho - sp; u = u - EPS * dw; spent += sp.sum()
    lk = 3 * H * rho; rho = rho - lk; u = u * (1 - 3 * H); leaked += lk.sum(); t += 1
drift = abs(rho.sum() + c.sum() + spent + leaked - tot) / tot
out = dict(arm=arm, start=start, W_over_pi=float(sys.argv[3]), seed=seed, pacc_used=pacc, death=death, peak=round(peak, 3),
           acceptance=(round(accd / prop, 4) if prop > 0 else None), rows=rows, drift=float(drift))
print(json.dumps({k: out[k] for k in ("arm", "start", "W_over_pi", "seed", "death", "peak", "acceptance", "drift")}), flush=True)
out["nosign"] = NOSIGN
json.dump(out, open(f"b14{'ns' if NOSIGN else ''}_a{arm}_{start}_W{sys.argv[3]}_s{seed}.json", "w"))
