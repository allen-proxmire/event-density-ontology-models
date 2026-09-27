"""Model B-17: committing runs on the local clock (card: cards/Model_B-17_Committing_On_The_Local_Clock.md).
Allen's decisions (RULES.md, 2026-09-27): the rate of commitment IS the clock; dissolving runs on the tick too;
new space arrives on one shared beat (expansion stays per global step, off the local clock).
Built on b16.py unchanged except for the clock factor on commit and dissolve (spending follows dissolving).
ARMS:  old     commit kappa(rho-theta), dissolve c/hbar                 (B-3..B-16; control)
       both    commit kappa r (rho-theta), dissolve c r/hbar            (Allen's decision; the model)
       commit  commit kappa r (rho-theta), dissolve c/hbar              (COMPARISON, not a meaning)
       (gentle = arm 'both' at P just above the switch, where clocks slow least while structure still forms)
CONDITIONS: H in {0, 1e-4} (expansion, one shared beat) x spending EPS in {0, 0.01}. With H = 0 and EPS = 0 structure
lives indefinitely, so those runs stop at TMAX_FIXED.
GATE (card sec. 5): overlap of free becoming with slowed clocks = [sum rho (1-r) / sum rho] / mean(1-r)
(1 = free stuff indifferent to slow places, > 1 = free stuff sits where clocks are slow), and the correlation of rho with 1-r.
Density distribution of committed stuff (sec. 4 saturation): percentiles of c at c > 0.1 sites, and max c.
Usage: python b17.py BASE ARM H SPEND RULE MODE SEED [P]   (BASE p11|pres; H 0|1; SPEND 0|1; RULE R1-R4; MODE live|frozen)"""
import sys, os, json, numpy as np
from scipy import ndimage
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB = float(os.environ.get("B17_HB", 100)); TMAX_FIXED = int(os.environ.get("B17_TMAX", 20000))   # B17_HB env: hbar for the switch check only
base, arm = sys.argv[1], sys.argv[2]
H = 1e-4 if sys.argv[3] == "1" else 0.0
EPS = 0.01 if sys.argv[4] == "1" else 0.0
rule, mode, seed = sys.argv[5], sys.argv[6], int(sys.argv[7])
P = float(sys.argv[8]) if len(sys.argv) > 8 else 20.0
s = P / (K * HB * TH)
rng = np.random.default_rng(seed)
rho = 3.0 * (1 + 1e-3 * rng.standard_normal((N,) * 3))
ph = np.zeros(rho.shape) if base == "pres" else rng.uniform(0, 2 * np.pi, rho.shape)
u = rho * np.exp(1j * ph); c = np.zeros(rho.shape); w = np.zeros(rho.shape, complex)
tot = rho.sum(); spent = leaked = 0.0; rows = []; peak = 0.0; death = None
gate_dev = 0.0; Wfrozen = None; clumps_life = []; lk_cl = 0.0   # lk_cl: dilution taken at clump sites (c > 0.1), diagnostic added after stage A
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
wrap = lambda x: (x + np.pi) % (2 * np.pi) - np.pi
t = 0
while t <= 150000:
    a = np.sqrt(s) * w / np.sqrt(np.maximum(c, 1e-30)); r = 1.0 / (1.0 + np.abs(a) ** 2)
    if t % 1000 == 0:
        cf = float(c.sum() / tot); peak = max(peak, cf)
        lab, ncl = ndimage.label(c > 0.1); clumps_life.append(ncl)
        sl = 1 - r; msl = float(sl.mean())
        ov = float((rho * sl).sum() / rho.sum() / msl) if msl > 1e-9 else None
        cor = float(np.corrcoef(rho.ravel(), sl.ravel())[0, 1]) if sl.std() > 1e-12 and rho.std() > 1e-12 else None
        cc = c[c > 0.1]
        rows.append(dict(t=t, cf=round(cf, 4), Rc=round(float(np.abs(w.sum()) / max(c.sum(), 1e-12)), 3), clumps=int(ncl),
                         overlap=None if ov is None else round(ov, 3), corr=None if cor is None else round(cor, 3),
                         c_p50=round(float(np.percentile(cc, 50)), 2) if cc.size else None,
                         c_p99=round(float(np.percentile(cc, 99)), 2) if cc.size else None, c_max=round(float(c.max()), 2),
                         r_min=round(float(r.min()), 3),
                         rho_cl=round(float(rho[c > 0.1].mean()), 3) if cc.size else None, rho_bg=round(float(rho[c <= 0.1].mean()), 3) if (c <= 0.1).any() else None,
                         c_cl=round(float(cc.mean()), 2) if cc.size else None, frac_cl=round(float((c > 0.1).mean()), 3),
                         leak_at_clumps=round(lk_cl / max(leaked, 1e-300), 3) if leaked > 0 else None, spent=round(spent / tot, 3), leaked=round(leaked / tot, 3)))
        if death is None and peak > 0.05 and cf < 0.01: death = t
        if death is not None or (t > 30000 and peak <= 0.05): break
        if H == 0 and EPS == 0 and t >= TMAX_FIXED: break
    rho, u = flow(rho, r), flow(u, r)
    rc = r if arm in ("both", "commit") else 1.0          # clock factor on committing
    rd = r if arm == "both" else 1.0                      # clock factor on dissolving
    ex = np.maximum(rho - TH, 0) * K * rc; frac = np.where(rho > 0, ex / np.maximum(rho, 1e-30), 0); du = frac * u
    if base == "pres":
        exa = ex; rho, c = rho - ex, c + ex; u, w = u - du, w + du
    else:
        theta = rng.uniform(0, 2 * np.pi, rho.shape)
        med = u + sum(np.roll(u, sh, ax) for ax in range(3) for sh in (1, -1))
        acc = np.abs(wrap(theta - np.angle(med))) < np.pi / 2
        exa = ex * acc; rho, c = rho - exa, c + exa; u = u - du; w = w + exa * np.exp(1j * theta)
    back = c * rd / HB; dw = w * rd / HB
    rho, c = rho + back, c - back; u, w = u + dw, w - dw
    sp = EPS * back; rho = rho - sp; u = u - EPS * dw; spent += sp.sum()
    if H > 0:                                             # expansion on the shared beat, placed by rule (as B-16)
        if rule == "R1": Wt = np.ones(rho.shape)
        elif rule == "R2": Wt = rho + c
        elif rule == "R3": Wt = r
        else: Wt = exa.copy()
        if mode == "frozen":
            if t == 1000: Wfrozen = Wt.copy()
            if Wfrozen is not None: Wt = Wfrozen
        target = 3 * H * rho.sum(); denom = float((rho * Wt).sum())
        f = np.full(rho.shape, 3 * H) if denom <= 0 else 3 * H * Wt * rho.sum() / denom
        for _ in range(20):
            over = f > 0.5
            if not over.any(): break
            f = np.where(over, 0.5, f)
            rem = target - float((f * rho).sum()); free_w = np.where(f < 0.5, Wt, 0.0); dd = float((rho * free_w).sum())
            if rem <= 0 or dd <= 0: break
            f = np.where(f < 0.5, f + rem * free_w / dd, f)
        f = np.minimum(f, 0.5)
        lk = f * rho; gate_dev = max(gate_dev, abs(lk.sum() - target) / max(target, 1e-300))
        rho = rho - lk; u = u * (1 - f); leaked += lk.sum(); lk_cl += float(lk[c > 0.1].sum())
    t += 1
drift = abs(rho.sum() + c.sum() + spent + leaked - tot) / tot
pk = max(range(len(rows)), key=lambda i: rows[i]["cf"])
guard = [dict(t=x["t"], Rc_ceiling=round(x["Rc"] / 0.6366, 2)) for x in rows if x["cf"] >= peak / 5] if base == "p11" else None
out = dict(base=base, arm=arm, H=H, spend=EPS > 0, rule=rule, mode=mode, seed=seed, P=P, death=death, peak=round(peak, 3),
           ended=rows[-1]["t"], clumps_at_peak=rows[pk]["clumps"], clumps_mean=round(float(np.mean(clumps_life)), 1),
           at_peak=rows[pk], gate_total_dev=float(gate_dev), align_guarded=guard, rows=rows, drift=float(drift))
print(json.dumps({k: out[k] for k in ("base", "arm", "H", "spend", "rule", "mode", "seed", "P", "death", "peak", "ended",
                                        "clumps_at_peak", "gate_total_dev", "drift")} | {"at_peak": rows[pk]}), flush=True)
json.dump(out, open(f"b17_{base}_{arm}_H{int(H>0)}_sp{int(EPS>0)}_{rule}_{mode}_P{P:g}_hb{HB:g}" + ("" if TMAX_FIXED == 20000 else f"_T{TMAX_FIXED}") + f"_s{seed}.json", "w"))
