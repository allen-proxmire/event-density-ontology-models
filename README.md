# Event Density

*Allen Proxmire.*

[![DOI](https://zenodo.org/badge/1366865757.svg)](https://doi.org/10.5281/zenodo.22718511)

**Event Density (ED) is an ontology** — an account of what the world is made of, underneath physics. It starts from one conviction: **time only runs one way.** Once something has happened, it can't be undone.

It is a theory of possibilities. It is not a theory of gravity or a theory of everything. It asks a different question: *what must be true for anything to have a structure at all?*

This repository holds the ontology, the results of testing it, models of what its own ingredients do, and the code. The central tested result is **3 quantities that CDT leaves free, and tunes by hand, are fixed by the ontology.**

---

## The idea

* The universe is a web of places, a web of relations. The web keeps growing; new places are continuously being born.
* What hasn't committed yet — **possibility**; unsettled, quantum things — spreads across the web like ripples, trying many paths at once.
* When a ripple meets something already settled (committed), it commits. It leaves a mark on the world. Once that mark is made, it can't be unmade; something definite has happened. That is a **commitment**.
* Commitments use up a finite budget. Matter, time and motion contribute to how this budget is consumed, so that near a lot of committed matter, clocks and motion slow down.

The only other inputs are the Born rule, the area law, 3+1 dimensions, and a starting shape. Everything else here is working out what these imply. The full account: [ontology/Event_Density_An_Ontology.md](ontology/Event_Density_An_Ontology.md).

---
## The results

### Results from analysis and proof

*These apply known mathematics and physics to ED's own claims; none is new mathematics. ED's contribution is the connection. Read these first.*

**1. ED's conservation laws fix three numbers that causal dynamical triangulations tunes by hand.** CDT builds spacetime from blocks stacked in time-slices and leaves three totals free — the corner points N₀ and the two kinds of block N₄₁ and N₃₂ — tuned through κ₀, Δ and κ₄. **ED's conserved budgets fix all three**: 

1. its event budget fixes N₀, 
2. its link budget fixes N₄₁, 
3. and conserving forward links fixes N₃₂ through an exact identity, N₁ᵀ = 2N₀ + N₃₂/2. 

Exact algebra, no new free parameters. In 2+1 dimensions the point they fix sits inside the phase where space does not collapse; in 3+1 it is unresolved, and the direction is unfavourable: the vertex density ED needs points toward the phase where space collapses.

**2. Below three dimensions, clocks cannot keep time together.** The coupling needed to hold a pattern's clocks together rises without limit in one and two dimensions, and at three and above rises at most very slowly, with a large majority staying locked. It reads the dimension, not the number of connections. So ED's own content rules out one- and two-dimensional worlds.

**3. Handedness cannot be written into mirror-symmetric rules.** A proved theorem, checked by a script here: symmetric rules give exactly zero drift. If the world has a handedness — and it does — its state picked it, not its laws.

**4. ED carries the dimension it is given.** Three-plus-one is a declared primitive; measured with ED's own definition of dimension, the rules carry a dimension they are given and add none of their own. With results 2 and 5 it is bounded to three, conditionally.

**5. If a particle is an uncuttable knot, three is the only dimension that works.** Loops cannot knot in two dimensions, and every knot comes undone in four or more; only in three do uncuttable loops come in many kinds that last. With result 2, that bounds the number from both sides: a reason for three, conditional on what a particle is, not a derivation of space. **What makes such a knot uncuttable in ED is that an uncommitted link's place is held for its own pair**, by identities fixed when those places came into being; models show the knot comes apart quickly without it.

### Results from models

*What ED's own ingredients do, mostly in supplied three-dimensional space: behaviours of the rules, not claims about nature.*

ED declares three-plus-one dimensions as an input; it does not claim to make space. So the models supply space as a 3D grid and ask what ED's own ingredients do in it.

With space supplied as the ontology declares, ED's own ingredients — flow, clocks slowed by committed matter, commitment, dissolution after ħ, new places being born, a spending budget, polarity — were run to see what they do. Among the results:

* **Structure has a switch**, derived on paper and found exactly at the predicted value, with nothing tuned.
* **Structure is temporary**: uniform, then structure, then uniform again, ended from outside by new places being born or from inside by spending.
* **The only memory is the present state**: a clump is wherever its stuff is.
* **Patterns host, merge, bind and part**, and polarity is selected by the surroundings.
* **A medium orders itself**: under the ontology's commitment rule, the whole medium comes to share one phase that nothing supplied.
* **Where a new event goes costs little** once space is given.
* **When the rate of commitment is the clock**, the switch stays exactly in place, and structure is ended mainly from outside.
* **Space is a necessary input**: nine models tried to grow space from ED's other ingredients and none did, so the dimension and arrangement of space are inputs, not outputs — and what the input adds is **the dimension of a neighbour relation the ontology already supplies**, which four further candidate rules failed to fix from ED's other ingredients.
* **Local three-dimensional order can be made from disorder, but not kept as space grows**: ED's ingredients grow a near-cubic glass, right on average and wrong in detail, and nothing tried crystallises it.
* **A region can be cut off two ways, by breaking its links or by stopping its clock, and the clock wins**: a sharp, mass-sized decoupling surface exists while the region is fed, and a growing mass slows the region's clock without limit.

---

## How to judge it

ED should be judged as an ontology, not as a new physical theory. Most ontologies, from process philosophy to relational pictures of physics, stay entirely verbal: they describe how the world might be built, and there is nothing to run or check. Judged as an ontology, ED has what most lack:

1. **It is runnable.** Its ideas were turned into exact rules a computer can run: fourteen model builds, then a programme of some forty models, with code here for the results it covers.
2. **It constrains an established framework.** Its conservation laws fix three numbers that CDT, a working approach to quantum spacetime, tunes by hand — at a viable point in 2+1, and with 3+1 unresolved.
3. **It forbids things, from its own content:** one- and two-dimensional worlds, four or more dimensions if a particle is an uncuttable knot, handedness written into mirror-symmetric laws, and a regular grid as the substrate.
4. **Its concepts behave as claimed when built.** "Nothing accumulates a record of itself": the only memory is the present state. "Every structure is a temporary attractor": the full arc appears. Polarity binds patterns in step and parts them out of step. These are behaviours of the rules, not labels on them.
5. **It is carefully scoped.** Every claim carries its strength and its scope, and the code is here or available on request.

ED supplies, in its own words, *"the conditions of possibility, not the full catalogue of outcomes."* It says what may happen, not where a new event goes — and with space supplied, the models show that "where" costs structure little. Space itself is a necessary input; the natural next extension is what the commitment that makes a place decides about its relations.

---

## What's here

|||
|-|-|
|[ontology/Event\_Density\_An\_Ontology.md](ontology/Event_Density_An_Ontology.md)|**the paper** — what ED is, what follows from it, and what testing established|
|[PLAIN\_LANGUAGE.md](PLAIN_LANGUAGE.md)|**the whole programme in plain language** — the story, the results, how strongly each stands|
|[results/RESULTS.md](results/RESULTS.md)|**results from analysis and proof** — five results applying known mathematics to ED's claims; read first|
|[results/MODEL\_RESULTS.md](results/MODEL_RESULTS.md)|**results from models** — eighteen results on what ED's own ingredients do in supplied space|
|[results/CDT\_Constraint.md](results/CDT_Constraint.md)|the CDT result in full, for readers who know causal dynamical triangulations|
|[results/Constraints.md](results/Constraints.md)|what ED forbids, what it fixes, what it leaves open|
|[results/Handedness/](results/Handedness/)|the handedness theorem: statement, proof, assumptions, and a script that checks it|
|[method/HOW\_IT\_WAS\_DONE.md](method/HOW_IT_WAS_DONE.md)|how the work was done: meanings, cards, pre-set measurements, calibration, controls, review|
|[method/STANDARDS.md](method/STANDARDS.md)|the working rules everything here was held to|
|[method/models/](method/models/)|the code for model results 1–12 and the clock floor, with a table of which script reproduces which result|

## Check it yourself

```
python results/Handedness/check_result.py
```

Needs Python with numpy. It tests the handedness theorem for up to six lanes, for random mirrors, and for hops reaching several places at once, plus two edge cases.

Model results 1–12 and the clock floor can be rerun from [method/models/](method/models/) (Python with numpy and scipy); its README lists the script and command for each. The scripts for results 13–18 are held with the working record and available on request.

## Further reading

* H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981).
* J. Ambjørn, J. Jurkiewicz and R. Loll on causal dynamical triangulations; the identities used in result 1 are from [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267).
* S. H. Strogatz and R. E. Mirollo, "Phase-locking and critical phenomena in lattices of coupled nonlinear oscillators with random intrinsic frequencies," *Physica D* 31, 143 (1988) — the patch argument behind result 2.
* H. Hong, H. Chaté, H. Park and L.-H. Tang, "Entrainment Transition in Populations of Random Frequency Oscillators," *Phys. Rev. Lett.* 99, 184101 ([2007](https://dx.doi.org/10.1103/PhysRevLett.99.184101)) — two dimensions as the borderline for a large locked majority.
* S. Aaronson, S. M. Carroll and L. Ouellette, "Quantifying the Rise and Fall of Complexity in Closed Systems" ([arXiv:1405.6903](https://arxiv.org/abs/1405.6903)).
* Full references in [results/Handedness/PAPER\_Reflection-Symmetric Transport Carries No Handedness.md](results/Handedness/PAPER_Reflection-Symmetric%20Transport%20Carries%20No%20Handedness.md).

The full working record — every model build, ledger, dated note, log and data file — is held separately and available on request.

