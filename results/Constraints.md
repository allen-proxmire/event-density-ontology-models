# ED as an ontology: what it forbids, what it fixes, what it leaves open

*Allen Proxmire, 2026-09-23, updated 2026-10-02. The framing piece. Results are in [RESULTS.md](RESULTS.md) and [MODEL_RESULTS.md](MODEL_RESULTS.md).*

---

## What kind of thing this is

**Event Density is an ontology, not a theory of gravity and not a candidate for a theory of everything.**

The name causes some confusion, so: "Event Density" names a *mechanism* — how densely events happen in a region, and what that does to clocks and therefore to gravity — in the way "special relativity" names a mechanism. The ontology is the larger thing the mechanism sits inside: an account of what the world is made of.

Its founding statement says what it is for:

> *"ED does not predict every structure in the universe. It explains why structure is possible... conditions of possibility, not the full catalogue of outcomes."*
> *"It is a theory of why anything can have a structure at all."*

An ontology is judged differently from a theory. A theory is asked *what will happen?* An ontology is asked *what must be true for anything to happen at all?* — and it is judged on whether the structures physics already uses turn out to be forced, and whether the things it says are impossible are in fact absent.

The central tested result is **3 quantities that CDT leaves free, and tunes by hand, are fixed by the ontology.**

---

## What ED forbids

An ontology earns its keep by ruling things out. These are the exclusions that survived testing.

**One and two dimensions.** Events carry rates, and rates must be able to match across a pattern. A patch's surplus grows like the square root of its size while its edge grows more slowly in low dimensions, so large patches always break away. Measured, not just argued: in one and two dimensions the pull needed rises without limit as the pattern grows; at three and above it rises at most very slowly, with a large majority of clocks staying locked. A flat triangular sheet with the same six connections per event as the three-dimensional grid still fails, so this reads the dimension and not the number of connections.

**Patterns too sparse to hold together.** Below about five relations per event, a growing pattern fragments. Above it, it holds and copies itself more faithfully.

**Handedness in mirror-symmetric rules.** Proved: mirror-symmetric rules give exactly zero drift. If the world has a handedness — and it does — the rules didn't supply it; the state did.

**Collapse.** In the 2+1 simulations, from either starting condition, ED never produced the collapsed phase that the comparable framework falls into outside its tuned window.

**A regular lattice as the substrate.** If ED's connections lay on a regular grid, the number crossing a surface would depend on which way the surface faced — measured at 1.00, 1.41 and 1.73 for surfaces facing along an edge, a face diagonal and a body diagonal. Read through Jacobson's thermodynamic derivation of Einstein's equations, that would give **different gravity in different directions**. So ED's connections have to point every way equally: a random web, not a grid.

*(From a numerical check with its expectations fixed first. It came out of an earlier reading in which ED supplies the one physical assumption in Jacobson's derivation — a reading that rested on ED's web being smooth and three-dimensional at large scales, which the rules tested could not supply. The constraint above does not depend on that reading and stands on its own.)*

---

## What ED fixes

**Three numbers that causal dynamical triangulations tunes by hand.** Its conserved budgets fix two of CDT's three free totals and a conserved forward-link count fixes the third, through an exact identity. One point, nothing tuned.

This is the clearest example of the form an ontological result takes: **it doesn't predict a new number, it removes a freedom.**

**Two things checking the literature added.** First, the framing is *microcanonical*: CDT treats those totals as ensemble variables whose averages the couplings fix, while ED fixes the counts themselves — so the claim is that ED picks a definite point, and the open question is whether CDT's ensemble reaches it. Second, the result splits by dimension: **in 2+1 it holds**, with the value ED fixes reachable inside the non-collapsing phase; **in 3+1 it has been measured and ED's point lies outside the non-collapsing phase**, which reads a vertex density of about 0.075 and never below 0.073 anywhere scanned, against ED's 0.044. The fixing itself is unaffected: exact, in any dimension, with nothing tuned.

The full statement, with the identities, the numbers and what would settle it, is in [CDT_Constraint.md](CDT_Constraint.md).

---

## What ED leaves open

**Where a new event goes.** ED says what may happen — an event passes on its budget, commitments stick, rates must be able to match — but not *where*. It is the natural place for the ontology to be extended, and it now has a precise form: what the commitment that makes a place decides about its relations. With space supplied, the models show that where new places appear costs structure at most about a fifth of its life and changes nothing else measured ([MODEL_RESULTS.md](MODEL_RESULTS.md), result 11).

**Which shape space has.** 3+1 is a declared primitive. The testing confirms that the declaration is honest rather than decorative: ED carries a dimension it is given and never manufactures one, in sixteen runs using ED's own definition of dimension.

What it does add is that the primitive is **bounded**: the rate-matching floor rules out one and two dimensions from ED's own content, and if a particle is an uncuttable knot, four and more are ruled out too ([RESULTS.md](RESULTS.md), result 5). The input narrows from *any number* to *three*, with that condition stated. And the input is **necessary**: nine models tried to grow space from ED's other ingredients and none did ([MODEL_RESULTS.md](MODEL_RESULTS.md), result 16); space that is supplied keeps its local order as it grows but becomes a glass (result 18). What the input adds is the **dimension** of a neighbour relation the ontology already supplies, and four candidate rules for fixing that from ED's other ingredients were screened and none behaved like space (result 16). Asked from the other side as well, possibility left to dissolve and re-form under ED's own rules heals a structure's connectivity but collapses any dimension it is given, so **the dimension is the irreducible part of the input** (result 16).

**Every specific structure.** Galaxies, particles, constants. The ontology says explicitly that it doesn't supply these, and nothing in the testing suggests otherwise.

---

## The honest shape of the whole thing

| | |
|---|---|
| **What it is** | an ontology: an account of what the world is made of, and of why structure is possible at all |
| **What it supplies** | the Born rule, the area law, 3+1 dimensions, and a starting shape |
| **What it removes** | three free parameters of an established framework (its own input list is as declared) |
| **What it constrains** | one and two dimensions; four or more, if a particle is an uncuttable knot; over-sparse patterns; handedness in symmetric rules; collapse; and three free parameters of an established framework |
| **What it leaves open** | where a new event goes: what the commitment that makes a place decides about its relations |

---

## How it was done

Every test was specified before it was run, with its expected outcome recorded in advance and its instruments calibrated on objects whose answers were already known. An ontology that cannot be wrong about anything is not saying anything, so each result here carries the test that could have gone the other way. In full: [../method/HOW_IT_WAS_DONE.md](../method/HOW_IT_WAS_DONE.md).

The full record — fourteen model builds, then a programme of some forty models, with ledgers, dated notes, code and data — is held separately and available on request.
