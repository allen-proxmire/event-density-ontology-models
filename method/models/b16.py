"""Model B-16: where a new event goes (card: cards/Model_B-16_Where_New_Events_Go.md).
Expansion is dilution: each step free becoming is removed (booked to 'leaked') at the SAME TOTAL as the existing
models (3h x total free), but distributed by rule:
  R1 evenly (weight 1: the models' unstated default since B-3 - must reproduce them exactly)
  R2 where becoming is densest (weight = local event density rho + c)
  R3 where clocks run fastest (weight = local clock rate r)
  R4 at commitments (weight = amount committing at the site this step)
Per-site removed fraction f = 3h x W x sum(rho) / sum(rho W), capped at 0.5, with any capped excess spread over the uncapped sites by weight (water-filling; added after R4-live failed the
matched-total gate in the first run, where the plain cap left totals up to 85% short). Amplitude u scaled
by the same (1 - f). Committed stuff is not diluted (as before).
GUARD 1 (gate, printed first): removed total per step / (3h x sum rho) must be 1 to several digits for every rule.
GUARD 2: live weights vs FROZEN weights (weight field fixed at its step-1,000 value from then on).
R4 also with spending OFF (does R4 duplicate spending?).
Bases: 'p11' = P11 + filter, medium target, no flow sign, W = pi, scrambled start (B-14/B-15: 9,000; the ordering
result); 'pres' = phase-preserving, One Being start (B-12: 18,000).
Measured: death, peak, clumps (c > 0.1 clusters) at the peak step and mean over the life, whole-grid alignment
Rc/(2/pi) for p11 with the committed-fraction guard (not quoted when committed < 1/5 of its peak), spent, leaked.
Usage: python b16.py BASE RULE MODE SEED [SPEND]   (RULE R1-R4; MODE live|frozen; SPEND 1 default, 0 = off)"""
import sys, json, numpy as np
from scipy import ndimage
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, P, H = 100, 20.0, 1e-4; s = P / (K * HB * TH)
base, rule, mode, seed = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
EPS = 0.01 if (len(sys.argv) < 6 or sys.argv[5] == "1") else 0.0
rng = np.random.default_rng(seed)
rho = 3.0 * (1 + 1e-3 * rng.standard_normal((N,) * 3))
ph = np.zeros(rho.shape) if base == "pres" else rng.uniform(0, 2 * np.pi, rho.shape)
u = rho * np.exp(1j * ph); c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
tot = rho.sum(); spent = leaked = 0.0; rows = []; peak = 0.0; death = None
gate_dev = 0.0; caps = 0; Wfrozen = None; clumps_life = []
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
t = 0
while t <= 150000:
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    if t % 1000 == 0:
        cf = float(c.sum() / tot); peak = max(peak, cf)
        lab, ncl = ndimage.label(c > 0.1); clumps_life.append(ncl)
        rows.append(dict(t=t, cf=round(cf, 4), Rc=round(float(np.abs(w.sum()) / max(c.sum(), 1e-12)), 3), clumps=int(ncl),
                         spent=round(spent / tot, 3), leaked=round(leaked / tot, 3)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None or (t > 30000 and peak <= 0.05): break
    rho, u = flow(rho, r), flow(u, r)
    ex = np.maximum(rho - TH, 0) * K; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0); du = frac * u
    if base == "pres":
        exa = ex; rho, c = rho - ex, c + ex; u, w = u - du, w + du
    else:
        theta = rng.uniform(0, 2 * np.pi, rho.shape)
        med = u + sum(np.roll(u, sh, ax) for ax in range(3) for sh in (1, -1))
        acc = np.abs(wrap(theta - np.angle(med))) < np.pi / 2
        exa = ex * acc; rho, c = rho - exa, c + exa; u = u - du; w = w + exa * np.exp(1j * theta)
    back = c / HB; dw = w / HB
    rho, c = rho + back, c - back; u, w = u + dw, w - dw
    sp = EPS * back; rho = rho - sp; u = u - EPS * dw; spent += sp.sum()
    # --- where the dilution falls ---
    if rule == "R1": Wt = np.ones(rho.shape)
    elif rule == "R2": Wt = rho + c
    elif rule == "R3": Wt = r
    else: Wt = exa.copy()
    if mode == "frozen":
        if t == 1000: Wfrozen = Wt.copy()
        if Wfrozen is not None: Wt = Wfrozen
    target = 3 * H * rho.sum(); denom = float((rho * Wt).sum())
    f = np.full(rho.shape, 3 * H) if denom <= 0 else 3 * H * Wt * rho.sum() / denom
    for _ in range(20):                          # water-filling: cap at 0.5, spread the excess over uncapped sites by W
        over = f > 0.5
        if not over.any(): break
        caps += int(over.sum()); f = np.where(over, 0.5, f)
        rem = target - float((f * rho).sum()); free_w = np.where(f < 0.5, Wt, 0.0); dd = float((rho * free_w).sum())
        if rem <= 0 or dd <= 0: break
        f = np.where(f < 0.5, f + rem * free_w / dd, f)
    f = np.minimum(f, 0.5)
    lk = f * rho; gate_dev = max(gate_dev, abs(lk.sum() - target) / max(target, 1e-300))
    rho = rho - lk; u = u * (1 - f); leaked += lk.sum(); t += 1
drift = abs(rho.sum() + c.sum() + spent + leaked - tot) / tot
pk = max(range(len(rows)), key=lambda i: rows[i]["cf"])
guard = [dict(t=x["t"], Rc_ceiling=round(x["Rc"] / 0.6366, 2)) for x in rows if x["cf"] >= peak / 5] if base == "p11" else None
out = dict(base=base, rule=rule, mode=mode, seed=seed, spend=EPS > 0, death=death, peak=round(peak, 3),
           clumps_at_peak=rows[pk]["clumps"], clumps_mean=round(float(np.mean(clumps_life)), 1),
           gate_total_dev=float(gate_dev), cap_hits=caps, align_guarded=guard, rows=rows, drift=float(drift))
print(json.dumps({k: out[k] for k in ("base", "rule", "mode", "seed", "spend", "death", "peak", "clumps_at_peak", "clumps_mean", "gate_total_dev", "cap_hits")}), flush=True)
json.dump(out, open(f"b16wf_{base}_{rule}_{mode}_sp{int(EPS>0)}_s{seed}.json", "w"))
