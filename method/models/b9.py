"""Model B-9: polarity. Two species, hbar fixed (100), h = 1e-4, both strong (P 20). Read from the primitives:
  P09 + Paper 001: participation is a complex amplitude  P = sqrt(b) e^{i pi}  (pi = the polarity angle)
  P05: polarity is transported locus to locus along edges -> phase lives per locus and travels WITH the stuff.
    Implemented with the SIMPLEST connection (phase carried unchanged along each edge): each species carries a
    complex free field u = rho e^{i phi} that flows with the same operator as rho; committing moves the same
    fraction of u into a complex committed field w; dissolving moves it back. |u| <= rho, |w| <= c always.
  Slowing: the clock rate is r = 1 / (1 + |a_A + a_B|^2),  a_X = sqrt(s_X) * w_X / sqrt(c_X)
    (= sqrt(s c) e^{i phi} for coherent stuff). One species: r = 1/(1 + s c) exactly, which is B-3's rule.
    Two species: s_A c_A + s_B c_B + 2 sqrt(s_A c_A s_B c_B) cos(dphi) - adds, super-adds, or cancels.
  P07: channels are distinct; NOT assumed to ignore each other (clocks are still shared by place).
Runs: A alone; A+B with phase difference 0, pi/2, pi.
PRE-REGISTERED: in step (0): merge, both outlive B-8's 25,000 (the cross term adds slowing). Quarter turn (pi/2):
the cross term vanishes, so B-8 exactly (about 25,000, full co-location). Opposite (pi): overlapping slowing
cancels, so the two species AVOID each other's clumps (low co-location) - the first pushing-apart.
Usage: python b9.py WITH_B DPHI_OVER_PI"""
import sys, json, numpy as np
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, H, P = 100, 1e-4, 20.0; s = P / (K * HB * TH)
withB, dphi = sys.argv[1] == "1", float(sys.argv[2]) * np.pi
x = np.indices((N,) * 3) - (N - 1) / 2
def drop(cx): return np.where(np.sqrt((x[0]-cx)**2 + x[1]**2 + x[2]**2) < 0.22 * N, 8.0, 0.5)
rng = np.random.default_rng(1)
sp = []
for cx, ph, on in ((-8, 0.0, True), (8, dphi, withB)):
    rho = drop(cx) * (1 + 1e-3 * rng.standard_normal(x[0].shape)) if on else np.zeros(x[0].shape)
    sp.append(dict(rho=rho, u=rho * np.exp(1j * ph), c=np.zeros(x[0].shape), w=np.zeros(x[0].shape, complex),
                   tot=rho.sum() + 1e-300, leak=0.0, peak=0.0, death=None, on=on))
def flow(f, r):
    send = D * r * f; return f - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
t = 0; coloc = []
while t < 150000:
    if t % 100 == 0:
        for S in sp:
            if not S["on"]: continue
            f = float(S["c"].sum() / S["tot"]); S["peak"] = max(S["peak"], f)
            if S["death"] is None and S["peak"] > 0.05 and f < 0.01: S["death"] = t
        if withB and t % 2000 == 0:
            cA, cB = sp[0]["c"], sp[1]["c"]
            coloc.append((t, round(float(cB[cA > 0.1].sum() / max(cB.sum(), 1e-12)), 3), round(float(cA[cB > 0.1].sum() / max(cA.sum(), 1e-12)), 3)))
        if all((not S["on"]) or S["death"] is not None or (t > 20000 and S["peak"] <= 0.05) for S in sp) and t > 2000: break
    amp = sum(np.sqrt(s) * S["w"] / np.sqrt(np.maximum(S["c"], 1e-30)) for S in sp if S["on"])
    r = 1.0 / (1.0 + np.abs(amp) ** 2)
    for S in sp:
        if not S["on"]: continue
        S["rho"], S["u"] = flow(S["rho"], r), flow(S["u"], r)
        ex = np.maximum(S["rho"] - TH, 0) * K; frac = np.where(S["rho"] > 0, ex / np.maximum(S["rho"], 1e-30), 0)
        du = frac * S["u"]; back = S["c"] / HB; dw = S["w"] / HB
        S["rho"], S["c"] = S["rho"] - ex + back, S["c"] + ex - back
        S["u"], S["w"] = S["u"] - du + dw, S["w"] + du - dw
        S["leak"] += (3 * H * S["rho"]).sum(); S["rho"] *= (1 - 3 * H); S["u"] *= (1 - 3 * H)
    t += 1
drift = max(abs(S["rho"].sum() + S["c"].sum() + S["leak"] - S["tot"]) / S["tot"] for S in sp if S["on"])
coh = [round(float(np.abs(S["w"]).sum() / max(S["c"].sum(), 1e-12)), 3) for S in sp if S["on"]]
out = dict(withB=withB, dphi_over_pi=float(sys.argv[2]), A=dict(peak=sp[0]["peak"], death=sp[0]["death"]),
           B=(dict(peak=sp[1]["peak"], death=sp[1]["death"]) if withB else None), coloc=coloc, coherence_end=coh, ended=t, drift=float(drift))
print(json.dumps(out), flush=True); json.dump(out, open(f"b9_B{int(withB)}_d{sys.argv[2]}.json", "w"))
