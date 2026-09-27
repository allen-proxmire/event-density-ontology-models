"""B-8: TWO STRONG patterns (A P 20 with B P 20, and A P 20 with B P 8), lone controls, hbar fixed 100.
PRE-REGISTERED: clocks are shared by place, so each strong pattern shelters the other: shared clumps (high
co-location both ways) and each outlives its lone self. Co-location reported as (t, share of B inside A, share of A inside B).
Usage: python b8.py PA PB WITH_A WITH_B
Model B-7: two kinds of pattern in one space, hbar FIXED (Allen, 2026-09-26: one number for the substrate).
Design from the other session: interaction strength is carried BY THE STUFF (two species A and B, each with its
own free rho_X and committed c_X); clocks belong to the PLACE and are slowed by all committed stuff there:
    r = 1 / (1 + sA cA + sB cB)
Each species flows (D r rho_X to each neighbour), commits its own free stuff above theta (kappa per step), and
dissolves at 1/hbar. Expansion thins both free fields (3h per step). Each species' total is conserved separately.
Starts: a drop of A (contrast 8 over background 0.5) left of centre, a drop of B right of centre.
Conditions (P_X = s_X kappa hbar theta, hbar = 100): A strong P 20; B weak-but-above P 2, or B below the bar P 0.5.
Runs per condition: A alone, B alone, A + B together (the lone-weak control is the experiment).
PRE-REGISTERED: weak B lingers inside A's clumps (slow clocks), commits there, and lives LONGER than alone
(shelter), with its committed stuff co-located with A's. Below-bar B forms nothing alone but may form structure
inside A's clumps (enabled). Measured: each species' death (committed < 1% after a peak > 5%, else its peak
if it never formed), peak committed fraction, and co-location = share of B's committed stuff on sites where A's
committed stuff is above 0.1.
Usage: python b7.py PB WITH_A WITH_B"""
import sys, json, numpy as np
import b3_card as m
N, D, TH, K = m.N, m.D, m.THETA, m.KAPPA
HB, H = 100, 1e-4
PA, PB, withA, withB = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3] == "1", sys.argv[4] == "1"
sA, sB = PA / (K * HB * TH), PB / (K * HB * TH)
x = np.indices((N,) * 3) - (N - 1) / 2
def drop(cx): return np.where(np.sqrt((x[0]-cx)**2 + x[1]**2 + x[2]**2) < 0.22 * N, 8.0, 0.5)
rng = np.random.default_rng(1)
rA = drop(-8) * (1 + 1e-3 * rng.standard_normal(x[0].shape)) if withA else np.zeros(x[0].shape)
rB = drop(+8) * (1 + 1e-3 * rng.standard_normal(x[0].shape)) if withB else np.zeros(x[0].shape)
cA, cB = np.zeros_like(rA), np.zeros_like(rB)
tA, tB = rA.sum() + 1e-300, rB.sum() + 1e-300; lkA = lkB = 0.0
def flow(rho, r):
    send = D * r * rho; return rho - 6 * send + sum(np.roll(send, sh, ax) for ax in range(3) for sh in (1, -1))
def commit(rho, c):
    ex = np.maximum(rho - TH, 0) * K; back = c / HB; return rho - ex + back, c + ex - back
res = {"A": dict(peak=0.0, death=None), "B": dict(peak=0.0, death=None)}; coloc = []; t = 0
while t < 120000:
    if t % 100 == 0:
        for nm, c, tot in (("A", cA, tA), ("B", cB, tB)):
            f = float(c.sum() / tot); R = res[nm]; R["peak"] = max(R["peak"], f)
            if R["death"] is None and R["peak"] > 0.05 and f < 0.01: R["death"] = t
        if withA and withB and t % 2000 == 0 and cB.sum() > 1e-6:
            coloc.append((t, round(float(cB[cA > 0.1].sum() / cB.sum()), 3), round(float(cA[cB > 0.1].sum() / max(cA.sum(), 1e-12)), 3)))
        done = all((not w) or R["death"] is not None or (t > 20000 and R["peak"] <= 0.05) for w, R in ((withA, res["A"]), (withB, res["B"])))
        if done and t > 2000: break
    r = 1.0 / (1.0 + sA * cA + sB * cB)
    rA, rB = flow(rA, r), flow(rB, r)
    rA, cA = commit(rA, cA); rB, cB = commit(rB, cB)
    la, lb = 3 * H * rA, 3 * H * rB; rA, rB = rA - la, rB - lb; lkA += la.sum(); lkB += lb.sum(); t += 1
drift = max(abs(rA.sum() + cA.sum() + lkA - tA) / tA if withA else 0, abs(rB.sum() + cB.sum() + lkB - tB) / tB if withB else 0)
out = dict(PA=PA, PB=PB, withA=withA, withB=withB, A=res["A"] if withA else None, B=res["B"] if withB else None,
           coloc=coloc[:12], ended=t, drift=float(drift))
print(json.dumps(out), flush=True)
json.dump(out, open(f"b8_PA{PA}_PB{PB}_A{int(withA)}_B{int(withB)}.json", "w"))
