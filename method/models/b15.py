"""Model B-15, stage A (card: cards/Model_B-15_Connection_As_A_Field.md): P05's connection gets a TIME component
sourced by ED's own slowing. Each step, all stuff (free u and committed w) at a place turns its phase by
OMEGA x r(x), r = the local clock rate 1/(1 + s|a|^2). Nothing else changes. OMEGA = 0 is the existing model.
Two base models: 'pres' = phase-preserving (B-12 / B-14 arm 0), One Being start;
                 'p11'  = P11 randomization + phase filter, medium target, no flow sign, W = pi (B-14 best), scrambled.
GATE (card s5), with one correction recorded here: the start is uniform, so every clock runs at the same rate and
the space-time flux is exactly zero AT STEP 0; the gate is therefore read at step 2,000, after clumps form.
  flux on space-time plaquettes = OMEGA x (r(x+e) - r(x)) per step (reported: mean |.|, max); space-space
  plaquettes = 0 by construction (reported). If the space-time flux is zero at step 2,000 -> another B-10, stop.
ROUTE TEST, measured directly: at step 2,000 two probes are placed, one at the densest committed site (in a clump)
and one at the lowest-density site; each accumulates OMEGA x r of its own site for 1,000 steps (the clock taken up
a mountain). Reported: their phase difference (mod 2 pi), i.e. route dependence over 1,000 steps.
Also: structure (death, peak), committed per-site coherence sum|w|/sum c (local agreement), committed alignment.
FIXES after the other session's review (2026-09-27), in b15b outputs:
 (1) REAL ROUTE TEST: at step 2,000 three probes leave the same point P (8 sites before the densest clump along x) and
     reach the same point Q (8 sites after it) in the same total time: A goes straight through the clump; B detours
     around it (out 8 in y, across, back); C repeats A's route exactly (control, must read 0). One move every 30 steps;
     A and C wait at Q to match B's 32 moves. Each accumulates OMEGA x r at the site it occupies, from the live r field.
 (2) BETWEEN-REGION AGREEMENT: committed clumps here are single isolated sites, so agreement is read at the clump-spacing
     scale: committed amplitude summed over 4x4x4 blocks; bsa = weighted mean cos(phase difference) between adjacent blocks,
     bcoh = within-block coherence |sum w| / sum c (combines several clumps; not fixed by the acceptance window) - not fixed by the acceptance window (the within-site sum|w|/sum c is
     2/pi = 0.637 by arithmetic under the filter, so it is not read in the P11 arm).
Usage: python b15.py MODEL OMEGA SEED"""
import sys, os, json, numpy as np
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P, H, EPS = 100, 20.0, 1e-4, 0.01; s = P / (K * HB * TH)
model, OM, seed = sys.argv[1], float(sys.argv[2]), int(sys.argv[3])
rng = np.random.default_rng(seed)
rho = 3.0 * (1 + 1e-3 * rng.standard_normal((N,) * 3))
ph = np.zeros(rho.shape) if model == "pres" else rng.uniform(0, 2 * np.pi, rho.shape)
u = rho * np.exp(1j * ph); c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
tot = rho.sum(); spent = leaked = 0.0; rows = []; peak = 0.0; death = None; gate = None; probe = None
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
t = 0
while t <= 150000:
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    if t % 1000 == 0:
        cf = float(c.sum() / tot); peak = max(peak, cf)
        Bk = 4; Wb = w.reshape(N//Bk, Bk, N//Bk, Bk, N//Bk, Bk).sum(axis=(1, 3, 5)); Cb = c.reshape(N//Bk, Bk, N//Bk, Bk, N//Bk, Bk).sum(axis=(1, 3, 5))
        ok = Cb > 1.0; ub = np.where(ok, Wb / np.maximum(np.abs(Wb), 1e-30), 0)
        num = den = 0.0
        for ax in range(3):
            mm = ok & np.roll(ok, -1, ax); wt = np.minimum(Cb, np.roll(Cb, -1, ax))[mm]
            num += float((wt * (ub * np.conj(np.roll(ub, -1, ax)))[mm].real).sum()); den += float(wt.sum())
        bsa = num / den if den > 0 else None
        bcoh = float(np.abs(Wb[ok]).sum() / max(Cb[ok].sum(), 1e-12)) if ok.any() else None
        rows.append(dict(t=t, bsa=(None if bsa is None else round(bsa, 3)), bcoh=(None if bcoh is None else round(bcoh, 3)), cf=round(cf, 4), coh=round(float(np.abs(w).sum() / max(c.sum(), 1e-12)), 3),
                         Rc=round(float(np.abs(w.sum()) / max(c.sum(), 1e-12)), 3)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None or (t > 30000 and peak <= 0.05): break
    if t == 2000:
        st = [OM * np.abs(np.roll(r, -1, ax) - r) for ax in range(3)]
        gate = dict(t=2000, st_flux_mean=float(np.mean(st)), st_flux_max=float(np.max(st)), ss_flux=0.0,
                    r_min=float(r.min()), r_max=float(r.max()))
        i_in = np.unravel_index(np.argmax(c), c.shape); i_out = np.unravel_index(np.argmin(rho + c), c.shape)
        probe = dict(phi_in=0.0, phi_out=0.0, i_in=[int(v) for v in i_in], i_out=[int(v) for v in i_out])
        cx, cy, cz = [int(v) for v in i_in]
        Aroute = [((cx - 8 + k) % N, cy, cz) for k in range(17)]
        Broute = [((cx - 8) % N, (cy + k) % N, cz) for k in range(9)] + [((cx - 8 + k) % N, (cy + 8) % N, cz) for k in range(1, 17)] + [((cx + 8) % N, (cy + 8 - k) % N, cz) for k in range(1, 9)]
        pad = len(Broute) - len(Aroute); Aroute = Aroute + [Aroute[-1]] * pad
        routes = dict(A=Aroute, B=Broute, C=list(Aroute)); rphase = dict(A=0.0, B=0.0, C=0.0)
    if probe is not None and 2000 <= t < 3000:
        probe["phi_in"] += OM * float(r[i_in]); probe["phi_out"] += OM * float(r[i_out])
    if probe is not None and 2000 <= t < 2000 + 30 * len(routes["B"]):
        k = (t - 2000) // 30
        for nm in rphase: rphase[nm] += OM * float(r[routes[nm][k]])
    rho_before = rho
    rho, u = flow(rho, r), flow(u, r)
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0); du = frac * u
    if model == "pres":
        rho, c = rho - ex, c + ex; u, w = u - du, w + du
    else:
        theta = rng.uniform(0, 2 * np.pi, rho.shape)
        med = u + sum(np.roll(u, sh, ax) for ax in range(3) for sh in (1, -1))
        acc = np.abs(wrap(theta - np.angle(med))) < np.pi / 2          # W = pi, no flow sign (B-14 best)
        exa = ex * acc; rho, c = rho - exa, c + exa; u = u - du; w = w + exa * np.exp(1j * theta)
    back = c / HB; dw = w / HB
    rho, c = rho + back, c - back; u, w = u + dw, w - dw
    sp = EPS * back; rho = rho - sp; u = u - EPS * dw; spent += sp.sum()
    lk = 3 * H * rho; rho = rho - lk; u = u * (1 - 3 * H); leaked += lk.sum()
    if OM > 0:                                                          # stage A: phase turns at the local clock rate
        rot = np.exp(1j * OM * r); u = u * rot; w = w * rot
    t += 1
if probe:
    probe["parked_diff_rad"] = round(float(abs(wrap(probe["phi_in"] - probe["phi_out"]))), 4)
    probe["route_AB_rad"] = round(float(abs(wrap(rphase["A"] - rphase["B"]))), 4); probe["route_AC_control_rad"] = round(float(abs(wrap(rphase["A"] - rphase["C"]))), 6)
    probe["route_total_A"] = round(rphase["A"], 4); probe["route_total_B"] = round(rphase["B"], 4)
drift = abs(rho.sum() + c.sum() + spent + leaked - tot) / tot
out = dict(model=model, omega=OM, seed=seed, death=death, peak=round(peak, 3), gate=gate, probe=probe, rows=rows, drift=float(drift))
print(json.dumps({k: out[k] for k in ("model", "omega", "seed", "death", "peak", "gate", "probe")}), flush=True)
json.dump(out, open(f"b15b_{model}_om{OM}_s{seed}.json", "w"))
