"""Event-layer benchmarks: reproduces results 20-25 of results/EVENT_LAYER.md.

ED says becoming happens in discrete commitments, each holding a place for a while before
dissolving back into possibility, with a clock at a place counting its own commitments.
This is that, directly -- no continuous amounts anywhere.

    python run_event_layer.py medium      result 20: the steady medium
    python run_event_layer.py arrow       result 22: the arrow and the age relic (2 seeds)
    python run_event_layer.py well        results 24-25: the clock well around matter (2 seeds)
    python run_event_layer.py all         all three
    python run_event_layer.py medium --quick      smaller/shorter, for a fast look

Needs Python with numpy and scipy. Each benchmark prints the published figure beside the one
it just measured.

--------------------------------------------------------------------------------------------
THE RULES, AND WHOSE EACH ONE IS
--------------------------------------------------------------------------------------------
ED's:
  * A place is committed (ON) or it is not. Nothing else is stored.
  * A commitment holds for HBAR ticks, then dissolves back into possibility.
  * The One Being start: every place in step at tick 0.
  * One budget. A commitment spends one unit of possibility from each of the two places,
    and nothing else limits it.
  * Universal return: when a commitment dissolves, what it spent returns to possibility at
    large -- a uniformly random place -- not to the spender or its neighbours.
  * Chance acts at every commitment, through the Born weighting.
  * The pull: committing together moves two cadences toward their mean.
  * A clock is a place's own count of completed commitments. There is no formula for it.
  * Cadence is a place's accumulated count of its own commitments.
  * Matter: a place that also holds one internal commitment on a reserved slot with a fixed
    partner, renewed the moment it ends if both places hold possibility. It is otherwise an
    ordinary place of the medium and commits with the space beside it as any place does.

Ours (the model's, not the ontology's):
  * A supplied 3D periodic grid with 6 neighbours. Which pairs of places may be neighbours is
    an input to every model in this programme (result 4).
  * DPHI = 0.1, the cadence advance per completed commitment. In-step percentages depend on
    it; the ~2-blink neighbour difference underneath them does not.
  * K = 0.5, the strength of the pull: half way to the mean per commitment.
  * PHOP, how fast possibility wanders (0.2, up to a ceiling of 1.0).
  * DENS, the units of possibility per place at the start.
  * HBAR = 5 ticks.
  * A pair commits only on mutual proposal.
  * One reserved commitment per matter place, the fixed pairing, and that matter is a ball.
  * PHI_C = 0.3, the window within which two cadences are *reported* as in step. It is a
    reading, not a rule: nothing in the engine gates on it.

NOT shown by any of this: how space or the neighbour relation arises (both supplied); that
matter persists (that is a rule, and the clock well is the consequence of its being paid for);
gravity's reach, which trades against its strength -- see result 25.
"""

import sys
import numpy as np
from scipy import ndimage

HBAR = 5          # a commitment holds this many ticks
DPHI = 0.1        # cadence advance per completed commitment (ours)
K = 0.5           # the pull: fraction of the way to the mean (ours)
PHI_C = 0.3       # the window for *reporting* in-step share (a reading, not a rule)
DIRS = [(ax, sh) for ax in range(3) for sh in (1, -1)]
STAR = np.zeros((3, 3, 3), int)
STAR[1, 1, :] = STAR[1, :, 1] = STAR[:, 1, 1] = 1


def wrap(x):
    return np.angle(np.exp(1j * x))


class World:
    """The discrete event layer. One budget, universal return, Born choice, the pull."""

    def __init__(self, L, dens, seed, mode="one", phop=0.2, radius=3):
        self.L, self.dens, self.phop, self.mode = L, dens, phop, mode
        self.rng = np.random.default_rng(seed)
        shape = (L, L, L)
        self.shape = shape
        self.on = np.zeros(shape, bool)        # committed now
        self.timer = np.zeros(shape, int)      # ticks left on the commitment
        self.phi = np.zeros(shape)             # cadence: the One Being start, all in step
        self.blinks = np.zeros(shape, int)     # the clock: completed commitments
        self.spent = np.zeros(shape, int)      # possibility held inside live commitments
        self.P = np.full(shape, dens, int)     # possibility, in units

        gx, gy, gz = np.indices(shape)
        c = L // 2
        self.dcen = np.sqrt((gx - c) ** 2 + (gy - c) ** 2 + (gz - c) ** 2)

        if mode == "conc":
            # all of the possibility piled into a central ball; the rest of space left quiet
            core = self.dcen <= 3
            n, total = int(core.sum()), dens * L ** 3
            self.P = np.zeros(shape, int)
            self.P[core] = total // n
            self.P[core] += self.rng.permutation(np.arange(n) < (total - (total // n) * n))

        # matter: a ball whose places each hold one internal commitment with a fixed partner
        self.knot = (self.dcen <= radius) if mode == "knot" else np.zeros(shape, bool)
        self.pairs = []
        if mode == "knot":
            taken = np.zeros(shape, bool)
            idx = np.argwhere(self.knot)
            for i in self.rng.permutation(len(idx)):
                a = tuple(int(v) for v in idx[i])
                if taken[a]:
                    continue
                cands = []
                for ax, sh in DIRS:
                    q = list(a)
                    q[ax] = (q[ax] + sh) % L
                    q = tuple(q)
                    if self.knot[q] and not taken[q]:
                        cands.append(q)
                if cands:
                    q = cands[int(self.rng.integers(len(cands)))]
                    taken[a] = taken[q] = True
                    self.pairs.append((a, q))
        self.int_on = np.zeros(len(self.pairs), bool)
        self.int_timer = np.zeros(len(self.pairs), int)

    # ------------------------------------------------------------------ possibility
    def wander(self):
        """each unit of possibility hops to a random neighbour with chance PHOP per tick"""
        hop = self.rng.binomial(self.P, self.phop)
        rem, moved = hop.copy(), np.zeros(self.shape, int)
        for k in range(6):
            take = rem if k == 5 else self.rng.binomial(rem, 1.0 / (6 - k))
            rem = rem - take
            ax, sh = DIRS[k]
            moved += np.roll(take, sh, ax)
        self.P = self.P - hop + moved

    def release(self, n):
        """universal return: n units go back to possibility at large, uniformly"""
        if n:
            flat = self.rng.integers(self.P.size, size=int(n))
            np.add.at(self.P.reshape(-1), flat, 1)

    # ------------------------------------------------------------------ matter
    def internal_step(self):
        """a reserved slot whose commitment ends re-commits at once, if both places can pay"""
        released = 0
        for i, (a, b) in enumerate(self.pairs):
            if self.int_on[i]:
                self.int_timer[i] -= 1
                if self.int_timer[i] > 0:
                    continue
                self.int_on[i] = False
                released += 2
            if self.P[a] >= 1 and self.P[b] >= 1:
                self.P[a] -= 1
                self.P[b] -= 1
                self.int_on[i] = True
                self.int_timer[i] = HBAR
        self.release(released)

    # ------------------------------------------------------------------ the tick
    def tick(self):
        # dissolve: a commitment whose hold has run out ends. That is one completed blink.
        self.timer[self.on] -= 1
        done = self.on & (self.timer <= 0)
        self.on[done] = False
        self.blinks[done] += 1
        self.phi[done] += DPHI          # cadence advances on a place's own completed blinks

        # universal return of what those commitments spent
        self.release(int(self.spent[done].sum()))
        self.spent[done] = 0

        if self.pairs:
            self.internal_step()

        self.wander()

        # Born choice: a place proposes to a neighbour with probability proportional to the
        # intensity of the pair's joint amplitude, |sqrt(P_i)e^{i0_i} + sqrt(P_j)e^{i0_j}|^2/4
        avail = ~self.on & (self.P >= 1)
        W = np.zeros((6,) + self.shape)
        for k in range(6):
            ax, sh = DIRS[k]
            nbP = np.roll(self.P, -sh, ax)
            cosd = np.cos(np.roll(self.phi, -sh, ax) - self.phi)
            w = (self.P + nbP + 2.0 * np.sqrt(self.P * nbP) * cosd) / 4.0
            W[k] = np.where(avail & np.roll(avail, -sh, ax), np.maximum(w, 0.0), 0.0)

        tot = W.sum(0)
        u = self.rng.random(self.shape) * tot
        pick = (np.cumsum(W, 0) > u[None]).argmax(0)
        choice = np.where(tot > 0, pick, -1)

        # a pair commits when the two propose to each other
        for ax in range(3):
            fwd, back = DIRS.index((ax, 1)), DIRS.index((ax, -1))
            m = (choice == fwd) & (np.roll(choice, -1, ax) == back)
            if not m.any():
                continue
            m2 = np.roll(m, 1, ax)
            both = m | m2
            self.on[both] = True
            self.timer[both] = HBAR
            self.P[both] -= 1
            self.spent[both] += 1
            # the pull: committing together moves the two cadences toward their mean
            nphi = np.roll(self.phi, -1, ax)
            mean = 0.5 * (self.phi + nphi)
            fi = self.phi + K * (mean - self.phi)
            fj = np.roll(nphi + K * (mean - nphi), 1, ax)
            self.phi[m] = fi[m]
            self.phi[m2] = fj[m2]

    # ------------------------------------------------------------------ readings
    def in_step(self):
        return float(np.mean([np.mean(np.abs(wrap(np.roll(self.phi, -1, ax) - self.phi)) < PHI_C)
                              for ax in range(3)]))

    def coherence(self):
        return float(np.mean([np.mean(np.cos(np.roll(self.phi, -1, ax) - self.phi))
                              for ax in range(3)]))

    def neighbour_gap_blinks(self):
        """the step-invariant reading: the spread of neighbouring cadences, in blinks.
        This is the quantity the in-step and coherence figures are two scalings of, and it
        does not depend on DPHI."""
        d = [wrap(np.roll(self.phi, -1, ax) - self.phi) for ax in range(3)]
        return float(np.sqrt(np.mean([(x ** 2).mean() for x in d])) / DPHI)

    def largest_domain(self):
        link = [np.abs(wrap(np.roll(self.phi, -1, ax) - self.phi)) < PHI_C for ax in range(3)]
        lab = np.arange(self.P.size).reshape(self.shape)
        for _ in range(200):
            prev = lab
            m = lab.copy()
            for ax in range(3):
                nb = np.roll(lab, -1, ax)
                m = np.where(link[ax], np.minimum(m, nb), m)
                nb2 = np.roll(lab, 1, ax)
                m = np.where(np.roll(link[ax], 1, ax), np.minimum(m, nb2), m)
            lab = m
            if np.array_equal(lab, prev):
                break
        return float(np.bincount(lab.ravel()).max() / lab.size)

    def shell_rate(self, counts, ticks):
        out = {}
        for k in range(self.L // 2):
            m = (self.dcen >= k - 0.5) & (self.dcen < k + 0.5)
            if m.any():
                out[k] = float(counts[m].mean() / ticks)
        return out

    def shell_age(self):
        out = {}
        for k in range(self.L // 2):
            m = (self.dcen >= k - 0.5) & (self.dcen < k + 0.5)
            if m.any():
                out[k] = float(self.blinks[m].mean())
        return out


def run(world, ticks, half_from=None, windows=False):
    half = ticks // 2 if half_from is None else half_from
    at_half, spreads, prev = None, [], np.zeros(world.shape, int)
    for t in range(1, ticks + 1):
        world.tick()
        if t == half:
            at_half = world.blinks.copy()
        if windows and t % 500 == 0:
            w = world.blinks - prev
            prev = world.blinks.copy()
            mu = w.mean()
            spreads.append((t, float(w.std() / mu), float(1 / np.sqrt(mu))))
    second_half = world.blinks - at_half
    return second_half, ticks - half, spreads


def line(label, measured, published):
    print(f"  {label:<44} {measured:>16}   published: {published}")


# ---------------------------------------------------------------------------- benchmarks
def bench_medium(quick):
    L, ticks = (15, 3000) if not quick else (15, 600)
    print(f"\nRESULT 20 - the steady medium   (box {L}, 1 unit of possibility per place, "
          f"{ticks} ticks, seed 1)")
    w = World(L, 1, 1)
    rate, n, spreads = run(w, ticks, windows=True)
    line("clock rate", f"{rate.mean() / n:.4f}", "0.1043")
    line("neighbouring places in step", f"{w.in_step():.3f}", "0.948-0.954")
    line("coherence of neighbouring cadences", f"{w.coherence():.3f}", "0.99")
    line("largest coherent domain", f"{w.largest_domain() * 100:.1f}%", "99.8-99.9%")
    line("spread of cadence between neighbours", f"{w.neighbour_gap_blinks():.1f} blinks", "~1.4-2.2")
    line("places holding no possibility", f"{(w.P == 0).mean() * 100:.0f}%", "65%")
    line("places committed at any moment", f"{w.on.mean():.2f}", "0.51-0.54")
    line("places starved of becoming", f"{(rate == 0).mean() * 100:.2f}%", "none")
    if spreads:
        t, cv, ch = spreads[-1]
        line("spread of rates / chance", f"{cv / ch:.2f}", "0.65-0.67")


def age_lead(world):
    """how much older the origin region is than the far region, in blinks, by shell"""
    a = world.shell_age()
    inner = np.mean([a[k] for k in (1, 2) if k in a])
    outer = np.mean([a[k] for k in a if k >= 6])
    return float(inner - outer)


def bench_arrow(quick):
    """result 22. Each seed's concentrated start is read against its own matched uniform
    control, and the seeds are then averaged -- the same methodology as the well."""
    L, ticks = (20, 3000) if not quick else (15, 800)
    seeds = (1, 2) if not quick else (1,)
    print(f"\nRESULT 22 - the arrow of time   (box {L}, all possibility in a ball of radius 3, "
          f"{ticks} ticks, seed{'s' if len(seeds) > 1 else ''} "
          f"{', '.join(str(s) for s in seeds)})")

    rows = []
    for s in seeds:
        conc = World(L, 1, s, mode="conc")
        ctrl = World(L, 1, s, mode="one")
        rc, nc, _ = run(conc, ticks)
        rk, nk, _ = run(ctrl, ticks)
        rows.append(dict(clock_c=rc.mean() / nc, clock_u=rk.mean() / nk,
                         step_c=conc.in_step(), step_u=ctrl.in_step(),
                         lead=age_lead(conc), floor=age_lead(ctrl)))

    def mean(key):
        return sum(r[key] for r in rows) / len(rows)

    def spread(key, fmt="{:.4f}"):
        return ("  " + ", ".join(fmt.format(r[key]) for r in rows)) if len(rows) > 1 else ""

    print("  --- the start is forgotten in every rate (read over the second half)")
    line("clock rate, concentrated start", f"{mean('clock_c'):.4f}", "matches the control")
    line("clock rate, uniform control", f"{mean('clock_u'):.4f}", "to within 0.0002")
    line("the difference", f"{abs(mean('clock_c') - mean('clock_u')):.4f}", "0.0001-0.0002")
    line("in step, concentrated / control",
         f"{mean('step_c'):.3f} / {mean('step_u'):.3f}", "equal")
    print("  --- and one thing does not fade")
    line("origin older than the far region, by",
         f"{mean('lead'):.1f} blinks", "13-18 (box 20), 6-17 (box 15)")
    line("the same reading in the control (the floor)",
         f"{mean('floor'):.1f} blinks", "a few blinks either way")
    if len(rows) > 1:
        print(f"    per seed - age lead:{spread('lead', '{:.1f}')}    "
              f"control floor:{spread('floor', '{:.1f}')}")
        print("    The lead is many times the control's own shell-to-shell scatter; that gap is")
        print("    the reading. Its exact size moves with the seed and the box.")


def bench_well(quick):
    """results 24-25. Each seed is read against its own matched control, and the two seeds
    are then averaged -- the same way the published table is built."""
    L, dens, phop, ticks = (30, 2, 1.0, 3000) if not quick else (20, 2, 1.0, 800)
    seeds = (1, 2) if not quick else (1,)
    print(f"\nRESULTS 24-25 - the clock well around matter   (box {L}, {dens} units per place, "
          f"possibility wandering at {phop}, {ticks} ticks, "
          f"seed{'s' if len(seeds) > 1 else ''} {', '.join(str(s) for s in seeds)})")
    print("  matter is a ball of radius 3; the profile is raw against a matched control, "
          "with no correction")

    per_seed = []
    for s in seeds:
        knot = World(L, dens, s, mode="knot", phop=phop)
        ctrl = World(L, dens, s, mode="one", phop=phop)
        rk, n, _ = run(knot, ticks)
        rc, _, _ = run(ctrl, ticks)
        sk, sc = knot.shell_rate(rk, n), ctrl.shell_rate(rc, n)
        per_seed.append({k: 100.0 * (sc[k] - sk[k]) / sc[k]
                         for k in sk if k in sc and sc[k] > 0})

    # reference figures for THIS setting (density 2, possibility wandering at 1.0, box 30).
    # Shallower wander gives a deeper interior; those figures are not mixed in here.
    pub = {0: "34%", 1: "34%", 2: "23%", 3: "11%", 4: "4.65%", 5: "2.25%",
           6: "1.14%", 7: "0.57%", 8: "0.30%", 9: "0.15%"}
    wide = len(seeds) > 1
    head = f"  {'shell':>6}  {'clock slowing':>14}   {'published':<18}"
    print(head + ("  per seed" if wide else ""))
    for k in sorted(per_seed[0]):
        if k > 11 or any(k not in d for d in per_seed):
            continue
        vals = [d[k] for d in per_seed]
        mean = sum(vals) / len(vals)
        tag = "   <- matter" if k <= 3 else ""
        spread = ("  " + ", ".join(f"{v:.2f}" for v in vals)) if wide else ""
        print(f"  {k:>6}  {mean:>13.2f}%   {pub.get(k, ''):<18}{spread}{tag}")
    print("  (shells 0-2 are inside the matter, 3 is its surface, 4 and outward are space)")
    if wide:
        print("  Reproduction is statistical, not bit-for-bit. Expect the inner shells, the")
        print("  surface and shells 4-6, 8, 10-11 to land on the published figures. Shells 7")
        print("  and 9 come out a few tenths of a percent high in both seeds -- a small")
        print("  systematic difference in the outer tail rather than scatter, on a noise floor")
        print("  of 0.07-0.24%. What reproduces is the depth, the shape, the roughly-halving")
        print("  falloff and the crossing to background by shell 11.")
    else:
        print("  QUICK MODE is one seed and a smaller box: the figures will not match.")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    quick = "--quick" in sys.argv
    which = (args[0] if args else "all").lower()
    if which not in ("medium", "arrow", "well", "all"):
        print(__doc__)
        return 1
    print("=" * 94)
    print("Event-layer benchmarks - results 20-25 of results/EVENT_LAYER.md")
    if quick:
        print("QUICK MODE: smaller boxes and shorter runs. The figures will not match the "
              "published ones.")
    print("=" * 94)
    if which in ("medium", "all"):
        bench_medium(quick)
    if which in ("arrow", "all"):
        bench_arrow(quick)
    if which in ("well", "all"):
        bench_well(quick)
    print("\nWhat is ED's and what is the model's is in this file's header, and in "
          "results/EVENT_LAYER.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
