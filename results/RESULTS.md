# Results from analysis and proof

*Allen Proxmire. Last updated 2026-10-02. Read these first: they are the results in most direct contact with outside physics. What ED's own ingredients do in supplied space is in [MODEL_RESULTS.md](MODEL_RESULTS.md), the results from models; how the work was done is in [../method/HOW_IT_WAS_DONE.md](../method/HOW_IT_WAS_DONE.md).*

**Event Density (ED) is an ontology** — an account of what the world is made of, from which physics is supposed to follow. The central tested result is **3 quantities that CDT leaves free, and tunes by hand, are fixed by the ontology.**

**These five results apply known mathematics and physics to ED's own claims. None is new mathematics:** the CDT identities are Ambjørn, Jurkiewicz and Loll's; the handedness argument is close to Nielsen–Ninomiya; the clock floor is the known synchronisation result of Strogatz–Mirollo and Hong et al.; the knot facts are standard knot theory. **ED's contribution is the connection** — asking these questions of its own principles, and what the answers then fix or rule out.

Each result below had its expected outcome recorded before it was tested. The working record is held separately and available on request.

---

## 1. A conservation law fixes three numbers CDT tunes

Causal dynamical triangulations is a well-developed approach to quantum spacetime. Its bulk counts leave **three totals free** — **N₀**, the corner points; **N₄₁**, the blocks with four corners on one time-slice and one on the next; and **N₃₂**, the blocks with three on one slice and two on the next. Those three are what its couplings κ₀, Δ and κ₄ are tuned against.

**What ED adds is an idea: treat these three totals as conserved budgets — fixed quantities — rather than dials to tune.** In CDT those numbers are meant to be tuned, so nobody inside CDT had a reason to fix them from outside. ED did, because conservation is central to it.

**ED's conserved budgets fix all three.** The event budget fixes N₀, the link budget fixes N₄₁, and conserving forward links fixes N₃₂ through an exact identity, N₁ᵀ = 2N₀ + N₃₂/2. The result is a single point with nothing tuned — and in 2+1 dimensions that point sits **inside the phase where space doesn't collapse**, rather than the collapsed one.

Exact algebra. No new free parameters.

**Scope.** It is a statement about CDT's framework, not about nature: *if* spacetime is a CDT-like triangulation, this conservation removes the freedom. It predicts nothing newly measurable. The step linking ED's budgets to CDT's totals rests on recorded modelling decisions. **No one who works on CDT has reviewed it.**

**And it splits in two when checked against the literature.** In **2+1 it holds**: ED's conservation fixes the order parameter at exactly 1/3, and a validated run reaches that value inside the extended phase, at around k0 = 3.2. In **3+1 it is unresolved and currently leaning against**: ED needs a vertex density N0/N4 of 0.044, while the published measurements near the A-C transition are 0.152-0.164 — about three times larger. A later search found no measurement inside phase C itself, and that CDT's phases are told apart by this same quantity: small vertex density is the signature of the crumpled phase. So ED's value points toward collapse rather than deeper into the good phase. One run at the right point would settle it, and anyone with a CDT code could do it in an afternoon. Details: [CDT_Constraint.md](CDT_Constraint.md).

**The honest framing, also found by checking:** CDT treats these totals as ensemble variables that fluctuate, with the couplings fixing only their averages. ED fixes the counts themselves. So the claim is *microcanonical* — ED picks a definite point, and the question is whether CDT's ensemble ever reaches it.

**Full version, with the identities and the caveats: [CDT_Constraint.md](CDT_Constraint.md).**

---

## 2. The rate-matching floor, measured

ED says events carry rates that must be able to match across a pattern. The argument: a patch's rate surplus grows like the square root of its size, the relations crossing its edge grow more slowly in one or two dimensions, so large patches always break away.

**That was turned from an argument into a measurement.** On a line and on a flat grid, the pull needed to hold **every** clock together **rises without limit** as the pattern grows. On a three-dimensional grid and on a random web it rises **at most very slowly** — below what the measurement could resolve across the sizes tested.

The share of clocks that lock together tells the same story more sharply. At a coupling of 0.5, across an eightfold range of sizes, it collapses on flat patterns — 0.98 → 0.23 on a triangular sheet, 0.40 → 0.07 on a square grid — while staying high in three dimensions (0.99 → 0.88) and on a random web (0.96 → 0.98). *The coupling matters: at 1.0 and above every pattern locks fully and the measure says nothing.*

So ED's own content rules out one and two dimensions.

**Checked since, against the obvious objection** that this reads the number of connections rather than the dimension. The original comparison used a line with 2 connections per event, a flat grid with 4, and a three-dimensional grid with 6. A **triangular sheet has the same six connections as the three-dimensional grid and still fails** — its pull rises with size (0.625 → 0.812) where the three-dimensional grid's does not. It is the dimension.

**This lands on established physics.** The patch argument is the one Strogatz and Mirollo made for lattices of coupled oscillators ([1988](https://www.sciencedirect.com/science/article/abs/pii/0167278988900747)), and two dimensions is the known borderline for a large locked majority ([Hong, Chaté, Park and Tang, 2007](https://dx.doi.org/10.1103/PhysRevLett.99.184101)). ED arrives at it from its own content.

**Scope.** It doesn't pick three — three and everything above it pass equally. **Locking every single clock eventually fails in any dimension**, by the theorem above; what separates three from two is that a large majority stays locked. And it says nothing about where a pattern's shape comes from.

*Working record: attempt 11, claim C21.*

---

## 3. The handedness theorem

A proved theorem, checked by a script in this repository: in a hopping model, **mirror-symmetric rules give exactly zero drift.** Handedness cannot be written into rules that look the same in a mirror — if a world has one, its state picked it, the way a magnet picks a direction its laws don't prefer. And handedness is possible at all only because time runs one way.

**Scope.** The mathematics is simple and something close to it is already known (Nielsen–Ninomiya). ED's own rules can settle into a handed state, but only with three ingredients supplied rather than derived.

*Where: [Handedness/](Handedness/). Check it: `python results/Handedness/check_result.py`.*

---

## 4. On the rules tested, ED conditions space rather than producing it

**No dimension appeared under any rule set tested.**

This was tested in the regime ED's own papers specify (thick participation, not the sparse minimum), with **ED's own definition of dimension** — *"the number of independent participation directions available at scale"* — calibrated first on shapes already known: a ring reads 1, a flat grid 2, a cubic grid 3, a random web nothing.

Then, starting from a pattern with no dimension and growing it under every rule ED supplies: **sixteen runs, two sizes, eight seeds — none ever appears.**

These rules carry a dimension they are given, blur it as the pattern grows, and never make one. That is a result about this formalisation; it is not a proof that no ED mechanism could.

**3+1 is a declared primitive of the ontology**, not something it claimed to derive. What the testing adds is that the declaration is honest: dimension is genuinely an input, not something assumed and then presented as a result. Taken with result 2, one and two dimensions are excluded by ED's own content, narrowing the input from any number of dimensions to three or more; with result 5 it is bounded to three, conditionally.

*Working record: attempt 13, claims C10, C11, C15.*

---

## 5. If a particle is an uncuttable knot, three is the only dimension that works

Two of the ontology's own meanings, settled on 15 September 2026: **a particle is a knot of commitments that cannot be cut**, and *cannot be cut* includes that **a knot's strands cannot pass through each other**.

Those two meanings, with standard knot theory, give a sharp statement about dimension:

- **In two dimensions a loop cannot be knotted at all.** There is one kind of loop and no others.
- **In three, there are endlessly many distinct knots**, and none can be undone without either cutting a strand or passing one through another — both of which these meanings forbid. So the kinds are endless, and each one lasts.
- **In four dimensions and above, every knotted loop can be untied** by sliding strands past one another through the extra room, with nothing cut. So no kind lasts.

**So above three dimensions a particle cannot keep its kind, and below three, by result 2, clocks cannot keep time together.** Result 2 already narrows the input from any number of dimensions to three or more. This caps it at three. Taken together, the two bounds pin the number from both sides.

**What is ED's here is the connection, not the mathematics.** The knot facts are standard and old. What the ontology supplies is the identification of a particle with an uncuttable knot of commitments — and that is what makes a fact about topology into a statement about what can exist.

**Scope.** The *if* is load-bearing, which is why it is in the heading. The bound holds for **loops**, which are one-dimensional; two-dimensional membranes *can* knot in four dimensions, so if the ontology's lasting objects could be membranes rather than loops, four reopens. And this is not a derivation of space: model result 16 stands, and space remains a necessary input. What this gives is a **reason for the number**, conditional on what a particle is. Exactly three from the primitives alone, without this meaning of a particle, is not claimed.

*Working record: attempt 4, decisions D14 and D16. The mathematics: a simple closed curve in the plane cannot be knotted ([Jordan–Schoenflies theorem](https://en.wikipedia.org/wiki/Schoenflies_problem)); knots in three dimensions are classified and permanent under isotopy ([knot theory](https://en.wikipedia.org/wiki/Knot_theory)); every embedded circle in four or more dimensions is isotopic to the unknot ([higher dimensions](https://en.wikipedia.org/wiki/Knot_theory#Higher_dimensions)).*

---

## 6. Further findings

- **Patterns fragment below about five connections per event.** A threshold on how sparse a web can be and still hold together. *(Working record: attempt 12, claim C7.)*
- **ED never collapses.** In the 2+1 runs, from either starting condition, it never produced the collapsed phase CDT falls into outside its tuned window. *(Working record: attempt 11, claim C20.)*
- **A regular lattice cannot be ED's substrate.** On a grid, the connections crossing a surface depend on which way it faces (1.00, 1.41, 1.73), which would make gravity direction-dependent. ED's connections must point every way equally.
- **ED's growth degrades directional structure as it grows** — at a similar rate whatever the dimension. *(Working record: attempt 13, claim C15.)*

---

## What ED takes as input

**Declared inputs:** the Born rule, the area law, 3+1 dimensions, and a starting shape in every model.

Result 1 removes free numbers from *another* framework; it leaves ED's own input list as declared. The distinction is kept deliberately: a result would shorten ED's own input list only if one of these came out as a consequence, with no new free parameters.

---

## What would extend it

1. **Something in ED that says where a new event goes.** ED specifies what may happen, not where; in supplied space the models show that "where" costs little ([MODEL_RESULTS.md](MODEL_RESULTS.md), result 11), and the deeper form is answered by model result 16: new events do not build space, so space is a necessary input. What remains is what the commitment that makes a place decides about its relations.
2. **A second result of the same form:** *a free parameter of an established framework is not free, given this conservation.*
3. **A checkable difference from the standard account.**

---

## Method

Every test was specified before it ran, with its expected outcome recorded in advance and its instruments calibrated against objects whose answers were already known. Published work was checked before anything was claimed. Settings chosen to make something work are labelled as tuned. In full: [../method/HOW_IT_WAS_DONE.md](../method/HOW_IT_WAS_DONE.md).

The working record — fourteen model builds, then a programme of some forty models, with their ledgers, dated notes, code and data — is held separately and available on request.
