"""Does the clock-timing result read DIMENSION or LINK BUDGET - and does 3D really settle? (A11 C21, C22.)

TWO QUESTIONS, both about a claim standing in the public repository. RESULTS.md section 2 says: on a line and a
flat grid the pull needed to hold the clocks together "rises without limit" as the pattern grows; on a
three-dimensional grid and on a random web it "settles and stops rising". So ED's own content rules out one and
two dimensions.

  Q1  THE BUDGET CONTROL. That comparison used a line at 2 relations per event, a flat grid at 4, a 3D grid at 6
      and a web at 6. Timing gets easier as the budget rises - measured here at one size: ring 4.38, flat grid
      1.12, 3D grid 0.62. So part of "1D and 2D fail" may be the BUDGET, not the dimension. The control is a
      TRIANGULAR sheet: two-dimensional at a budget of 6. A single size cannot answer this, because the claim is
      about how the pull behaves as the pattern GROWS - a point on which an earlier note of mine overreached and
      is corrected here. This measures several sizes.

  Q2  DOES 3D ACTUALLY SETTLE? Strogatz and Mirollo (1988) proved that full phase-locking on a regular grid fails
      as the pattern grows in EVERY dimension, three included - only very slowly in three. If so, "settles and
      stops rising" is slow growth that was invisible between 2,000 and 16,000 events, and the honest wording is
      "at most very slowly". What genuinely switches on above two dimensions is not whether EVERY clock locks but
      the SHARE that do (Hong, Chate, Park and Tang, 2007). So both are measured.

TWO MEASURES
  K_c            the pull at which EVERY clock locks - attempt 11's own quantity, and the one the public claim is
                 about. Bisected, as there.
  SHARE LOCKED   at fixed pull, the largest fraction of clocks whose long-run rates agree to within tolerance.
                 This is the quantity the literature says distinguishes dimensions.

PRE-REGISTERED, before the run.
  E5  (from review, and from the area-against-edge argument) the triangular sheet's K_c KEEPS RISING with size,
      because the argument is about a patch's surplus outgrowing its edge and the budget only changes the
      constant. If so, the public result is about dimension and stands - with better wording and citations.
  E6  (Strogatz-Mirollo) the 3D grid's K_c ALSO rises with size, only slowly. If so "settles and stops rising"
      is too strong and must be softened.
  E7  (Hong et al.) the SHARE locked at fixed pull stays high for the 3D grid and the web as size grows, and
      falls for the two-dimensional shapes. That is the measure that separates them.

NOTE ON PRIORITY: this is not model work. It checks a claim already published in the public repository, which
outranks building B-2.
"""
import io
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
# (n1_sync.py sits beside this file in the public copy)
import shapes as S                                          # noqa: E402
import n1_sync as N1                                        # noqa: E402

OUT = os.path.join(HERE, "runs")
SEEDS = (1, 2)
FIXED_K = (0.5, 1.0, 2.0)
TOL = N1.TOL

FAMILIES = (
    ("triangular 2D  (budget 6)", [(s, lambda s=s: S.triangular(s)) for s in (8, 11, 14, 18, 22)]),
    ("3D grid        (budget 6)", [(s, lambda s=s: S.torus(s, 3)) for s in (4, 5, 6, 7, 8)]),
    ("random web     (budget 6)", [(s, lambda s=s: S.web(s, 6, np.random.default_rng(3)))
                                   for s in (64, 121, 216, 343, 512)]),
    ("flat grid 2D   (budget 4)", [(s, lambda s=s: S.torus(s, 2)) for s in (8, 11, 14, 18, 22)]),
)


def rates(A, omega, K, seed=0):
    """Long-run rate of every clock, using attempt 11's integrator settings."""
    n = A.shape[0]
    rng = np.random.default_rng(seed)
    th = rng.uniform(0, 2 * np.pi, n)
    dmax = float(np.asarray(A.sum(axis=1)).max())
    dtk = min(N1.DT, 0.2 / max(K * dmax, 1e-9))
    nt, nm = int(N1.T_TRANS / dtk), int(N1.T_MEAS / dtk)

    def dth(t):
        s, c = np.sin(t), np.cos(t)
        return omega + K * (c * (A @ s) - s * (A @ c))
    for _ in range(nt):
        th = th + dtk * dth(th)
    th0 = th.copy()
    for _ in range(nm):
        th = th + dtk * dth(th)
    return (th - th0) / N1.T_MEAS


def share_locked(A, omega, K, seed=0, tol=TOL):
    """Largest fraction of clocks whose long-run rates agree to within `tol`."""
    Om = np.sort(rates(A, omega, K, seed))
    n = len(Om)
    best = j = 0
    for i in range(n):
        while j < n and Om[j] - Om[i] <= tol:
            j += 1
        best = max(best, j - i)
    return best / float(n)


def main():
    os.makedirs(OUT, exist_ok=True)
    nl = chr(10)
    out, res = [], []
    out.append("CLOCK TIMING vs SIZE | checking a claim in the public repository, not building a model")
    out.append("K_c = pull at which EVERY clock locks (attempt 11's measure). share = largest fraction locked at "
               "fixed pull.")
    out.append("")
    out.append("%-26s %6s %7s %9s %s" % ("family", "n", "K_c", "rise x", "share locked at K = " + str(FIXED_K)))
    print(nl.join(out), flush=True)
    for fam, entries in FAMILIES:
        first = None
        for arg, build in entries:
            A = build().tocsr()
            n = A.shape[0]
            kcs, shares = [], {k: [] for k in FIXED_K}
            for sd in SEEDS:
                rng = np.random.default_rng(sd)
                om = rng.normal(0, 1, n)
                om -= om.mean()
                kc = N1.k_c(A, om, seed=sd)
                if kc is not None:
                    kcs.append(kc)
                for K in FIXED_K:
                    shares[K].append(share_locked(A, om, K, seed=sd))
            kc = float(np.mean(kcs)) if kcs else None
            first = first if first is not None else kc
            sh = {K: round(float(np.mean(v)), 3) for K, v in shares.items()}
            res.append(dict(family=fam, n=n, kc=kc, share=sh))
            out.append("%-26s %6d %7s %9s %s"
                       % (fam, n, ("%.3f" % kc) if kc is not None else "no lock",
                          ("%.2f" % (kc / first)) if (kc and first) else "-",
                          "  ".join("%.2f" % sh[K] for K in FIXED_K)))
            print(out[-1], flush=True)
            json.dump(res, open(os.path.join(OUT, "timing_scaling.json"), "w"), indent=1, default=str)
        out.append("")

    def series(fam, k="kc"):
        return [(r["n"], r[k]) for r in res if r["family"] == fam and r[k] is not None]

    out.append("=" * 112)
    for fam, _ in FAMILIES:
        s = series(fam)
        if len(s) < 3:
            continue
        ns = np.array([a for a, b in s], float)
        ks = np.array([b for a, b in s], float)
        slope = float(np.polyfit(np.log(ns), np.log(ks), 1)[0])
        out.append("%-26s K_c from %.3f to %.3f over n %d to %d | log-log slope %+.3f | %s"
                   % (fam, ks[0], ks[-1], int(ns[0]), int(ns[-1]), slope,
                      "RISING" if slope > 0.08 else ("flat" if abs(slope) <= 0.08 else "falling")))
        print(out[-1], flush=True)
    out.append("")
    for fam, _ in FAMILIES:
        s = [(r["n"], r["share"][FIXED_K[-1]]) for r in res if r["family"] == fam]
        if s:
            out.append("%-26s share locked at K=%.1f across sizes: %s"
                       % (fam, FIXED_K[-1], "  ".join("%.2f" % b for a, b in s)))
            print(out[-1], flush=True)

    def slope_of(fam):
        s = series(fam)
        if len(s) < 3:
            return None
        ns = np.array([a for a, b in s], float)
        ks = np.array([b for a, b in s], float)
        return float(np.polyfit(np.log(ns), np.log(ks), 1)[0])
    tri, g3 = slope_of("triangular 2D  (budget 6)"), slope_of("3D grid        (budget 6)")
    out.append("")
    if tri is not None and g3 is not None:
        out.append("E5 the 2D sheet at budget 6 keeps rising: %s  (slope %+.3f)" % (tri > 0.08, tri))
        out.append("E6 the 3D grid also rises, only slowly: %s  (slope %+.3f)" % (g3 > 0.08, g3))
        out.append("")
        if tri > 0.08 and tri > 2 * max(g3, 0.0):
            out.append("** The public result is about DIMENSION, not link budget: a two-dimensional shape at the "
                       "SAME budget as the 3D grid still rises, and faster. It stands, and needs only citations "
                       "and the wording fix below. **")
        elif tri <= 0.08:
            out.append("** The 2D sheet does NOT rise at a budget of 6. The public result is then substantially "
                       "about link budget rather than dimension, and its scope must be narrowed. **")
        if g3 > 0.08:
            out.append("** And 'settles and stops rising' is too strong for 3D - it rises too, slowly, exactly as "
                       "Strogatz and Mirollo (1988) require. The wording must become 'at most very slowly'. **")
    io.open(os.path.join(HERE, "timing_scaling.txt"), "w", encoding="utf-8").write(nl.join(out) + nl)


if __name__ == "__main__":
    main()
