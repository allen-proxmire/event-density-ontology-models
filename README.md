# Event Density

*Allen Proxmire.*

**Event Density (ED) is an ontology** — an account of what the world is made of, underneath physics. It starts from one conviction: **time only runs one way.** Once something has happened, it can't be undone.

It is a theory of possibilities. It is not a theory of gravity or a theory of everything. It asks a different question: *what must be true for anything to have a structure at all?*

**Untunability** is what the testing found, and what this repository is named for: **quantities that established frameworks leave free, and tune by hand, turn out to be fixed by what ED conserves.**

---

## The idea

- **The world is a web of places,** called *loci*. The web keeps growing: new places keep being born.
- **Things spread across the web like ripples,** trying many paths at once.
- **When a ripple meets something already settled** it leaves a mark. Once that mark is made, it can't be brought back; something definite has happened — a **commitment**.
- **Commitments use up a budget,** so near a lot of settled matter, clocks and motion slow down.

Everything else is working out what that implies. The full account: [ontology/Event_Density_An_Ontology.md](ontology/Event_Density_An_Ontology.md).

---

## The results

### From analysis and proof

**1. Untunability: ED's conservation laws fix three numbers that causal dynamical triangulations tunes by hand.** CDT builds spacetime from blocks stacked in time-slices and leaves three totals free — the corner points N₀ and the two kinds of block N₄₁ and N₃₂ — tuned through κ₀, Δ and κ₄. **ED's conserved budgets fix all three**: its event budget fixes N₀, its link budget fixes N₄₁, and conserving forward links fixes N₃₂ through an exact identity, N₁ᵀ = 2N₀ + N₃₂/2. Exact algebra, no new free parameters. In 2+1 dimensions the point they fix sits inside the phase where space does not collapse; in 3+1, one published measurement decides it.

**2. Below three dimensions, clocks cannot keep time together.** The coupling needed to hold a pattern's clocks together rises without limit in one and two dimensions, and at three and above rises at most very slowly, with a large majority staying locked. It reads the dimension, not the number of connections. So ED's own content rules out one- and two-dimensional worlds.

**3. Handedness cannot be written into mirror-symmetric rules.** A proved theorem, checked by a script here: symmetric rules give exactly zero drift. If the world has a handedness — and it does — its state picked it, not its laws.

**4. ED carries the dimension it is given.** Three-plus-one is a declared primitive; measured with ED's own definition of dimension, the rules carry a dimension they are given and add none of their own. With result 2 the primitive is *partly forced*: three or more.

### From models in supplied space

With space supplied as the ontology declares, ED's own ingredients — flow, clocks slowed by committed matter, commitment, dissolution after ħ, new places being born, a spending budget, polarity — were run to see what they do. Among the results:

- **Structure has a switch**, derived on paper and found exactly at the predicted value, with nothing tuned.
- **Structure is temporary**: uniform, then structure, then uniform again, ended from outside by new places being born or from inside by spending.
- **The only memory is the present state**: a clump is wherever its stuff is.
- **Patterns host, merge, bind and part**, and polarity is selected by the surroundings.
- **A medium orders itself**: under the ontology's commitment rule, the whole medium comes to share one phase that nothing supplied.
- **Where a new event goes costs little** once space is given.
- **When the rate of commitment is the clock**, the switch stays exactly in place, and structure is ended mainly from outside.

---

## How to judge it

ED should be judged as an ontology, not as a new physical theory. Most ontologies, from process philosophy to relational pictures of physics, stay entirely verbal: they describe how the world might be built, and there is nothing to run or check. Judged as an ontology, ED has what most lack:

1. **It is runnable.** Its ideas were turned into exact rules a computer can run: fourteen model builds, then a full model programme, with the code here.
2. **It constrains an established framework.** Its conservation laws fix three numbers that CDT, a working approach to quantum spacetime, tunes by hand.
3. **It forbids things, from its own content:** one- and two-dimensional worlds, handedness written into mirror-symmetric laws, and a regular grid as the substrate.
4. **Its concepts behave as claimed when built.** "Nothing accumulates a record of itself": the only memory is the present state. "Every structure is a temporary attractor": the full arc appears. Polarity binds patterns in step and parts them out of step. These are behaviours of the rules, not labels on them.
5. **It is carefully scoped.** Every claim carries its strength and its scope, and every model result can be rerun from the code.

ED supplies, in its own words, *"the conditions of possibility, not the full catalogue of outcomes."* It says what may happen, not where a new event goes — and with space supplied, the models show that "where" costs structure little. Whether new events *build* space is the natural next extension.

---

## What's here

| | |
|---|---|
| [ontology/Event_Density_An_Ontology.md](ontology/Event_Density_An_Ontology.md) | **the paper** — what ED is, what follows from it, and what testing established |
| [PLAIN_LANGUAGE.md](PLAIN_LANGUAGE.md) | **the whole programme in plain language** — the story, the results, how strongly each stands |
| [results/RESULTS.md](results/RESULTS.md) | the results from analysis and proof, each with its scope |
| [results/MODEL_RESULTS.md](results/MODEL_RESULTS.md) | what ED's own ingredients do in supplied space: twelve model results |
| [results/CDT_Constraint.md](results/CDT_Constraint.md) | the untunability result in full, for readers who know CDT |
| [results/Constraints.md](results/Constraints.md) | what ED forbids, what it fixes, what it leaves open |
| [results/Handedness/](results/Handedness/) | the handedness theorem: statement, proof, assumptions, and a script that checks it |
| [method/HOW_IT_WAS_DONE.md](method/HOW_IT_WAS_DONE.md) | how the work was done: meanings, cards, pre-set measurements, calibration, controls, review |
| [method/STANDARDS.md](method/STANDARDS.md) | the working rules everything here was held to |
| [method/models/](method/models/) | the code for every model result, with a table of which script reproduces which result |

## Check it yourself

```
python results/Handedness/check_result.py
```

Needs Python with numpy. It tests the handedness theorem for up to six lanes, for random mirrors, and for hops reaching several places at once, plus two edge cases.

Every model result can be rerun from [method/models/](method/models/) (Python with numpy and scipy); its README lists the script and command for each.

## Further reading

- H. B. Nielsen and M. Ninomiya, "A no-go theorem for regularizing chiral fermions," *Physics Letters B* 105, 219 (1981).
- J. Ambjørn, J. Jurkiewicz and R. Loll on causal dynamical triangulations; the identities used in result 1 are from [hep-th/0105267](https://arxiv.org/abs/hep-th/0105267).
- S. H. Strogatz and R. E. Mirollo, "Phase-locking and critical phenomena in lattices of coupled nonlinear oscillators with random intrinsic frequencies," *Physica D* 31, 143 (1988) — the patch argument behind result 2.
- H. Hong, H. Chaté, H. Park and L.-H. Tang, "Entrainment Transition in Populations of Random Frequency Oscillators," *Phys. Rev. Lett.* 99, 184101 ([2007](https://dx.doi.org/10.1103/PhysRevLett.99.184101)) — two dimensions as the borderline for a large locked majority.
- S. Aaronson, S. M. Carroll and L. Ouellette, "Quantifying the Rise and Fall of Complexity in Closed Systems" ([arXiv:1405.6903](https://arxiv.org/abs/1405.6903)).
- Full references in [results/Handedness/PAPER_Reflection-Symmetric Transport Carries No Handedness.md](results/Handedness/PAPER_Reflection-Symmetric%20Transport%20Carries%20No%20Handedness.md).

The full working record — every model build, ledger, dated note, log and data file — is held separately and available on request.
