# The discrete line, C-O44 to C-O54 — what was shown, what is ours, what is not shown

*Allen Proxmire, 2026-10-05. A synthesis of the event-layer models, written from the ledger entries rather than from the running commentary. Its purpose is to separate four things that the day's exchanges ran together: **what ED's own content produced**, **what the harness supplied**, **what failed and what each failure taught**, and **what is not shown.***

---

## 1. Why this line exists: the shadow and the substance

**Allen's observation, 2026-10-05, which started it:** the nineteen model results had been **coarse-graining commitments**. `b3_card.py` carries ρ and c as continuous densities; commitment is `max(ρ−θ,0)·κ`, a fraction of an excess flowing between two reservoirs; dissolution is `c/ħ`; and the clock reads `1/(1+s·c)`. **There is no commitment event anywhere in it** — no discrete blink, no lifetime, no duty cycle, nothing unsynchronised. Those are precisely the quantities averaging destroys.

**By ED's own §6 that is not a failure.** Spacetime is *"the smooth, continuous approximation that emerges when granular activity is coarse-grained over vast numbers of events."* So the nineteen results are results about **ED's shadow**, and they mostly work. What had never been written as a model was the **substance**: individual blinks competing for integer capacity.

**One correction from inside the line, recorded in C-O47a:** the integer token store is `b3_card.py`'s ρ, discretised — state at each place, flowing to neighbours, spent on commitment, returned on dissolution. **ρ came back on purpose, and "we removed the continuous fields" would be false.** The real gains of the pivot are narrower and they hold: **commitment became an event, and the clock became a count rather than an assigned formula.**

---

## 2. What ED's own content produced

**Five things, each with the reading that supports it.**

**(a) Scarcity is necessary for the One to differentiate.** With the pool able to serve every member at once (B = 7 for a pool of a place and its six neighbours), the One blinks in perfect unison with even clocks — in-step 1.000 throughout, clock 0.187 ± 0.007 (C-O44). **Below that, unison does not survive.** No slips were imposed.

> **But scarcity is not *sufficient*, and the stronger claim is withdrawn.** See §3: what breaks the tie is not in ED.

**(b) An unknotted medium relaxes into independent clocks.** Over 5,000 ticks the in-step share falls to 0.13–0.14 at ħ 10 and 0.11–0.12 at ħ 5, against a random-beat floor of ~0.10; the largest domain ends at 0.3–0.8%, against **C-O49's 27–84% at tick 1,000**; nobody is starved (0–0.04%). Box sizes agree to ~0.01 (C-O50). **Longer memory slows the decay and does not stop it.**

**(c) Memory governs how long coherence lasts.** At ħ 10 the largest domain is 73–84% with persistence 0.82–0.86; at ħ 5 it is 27–40% with persistence 0.49–0.58 (C-O49). **ħ is an ED quantity, so dependence on it is a property rather than an artefact** — stated openly in C-O49 rather than reinterpreted after the fact.

**(d) Clocks run on what is left, and a drain is visible.** A pinned-ON core cuts the blinking of the adjacent shell by ~90%: **lower by 0.031–0.032 against a control of 0.034**, so that shell blinks at about 0.003. The effect reaches **one shell** and stops, which is the pool's own reach (C-O51). **This is the instrument check, and it passed.**

**(e) Matter holds, is a net drain, and slows the clocks next to it.** With a held-slot knot and spent possibility released to the whole medium, and with tokens free to random-walk: the token deficit runs **0.74, 0.47, 0.33, 0.11** across distances 0–3 at box 15 and **0.44, 0.36, 0.30, 0.08** at box 20, vanishing beyond; **the first shell outside the knot blinks 12–15% slower than the background, the same at both box sizes and both seeds** (C-O53).

> **(e) is the result of the line.** Matter slowing the clocks around it, out of blinking and a shared budget, with no metric formula anywhere in the model.

---

## 3. What ED does not supply, and it is the central finding

**C-O46 is the most consequential entry in the series and it is a negative.**

Below full budget, something must decide which of two eligible pairs gets a contested slot. **At C-O46 the ontology had no rule for this**, and the harness's choice determined the world:

| contention rule | outcome |
|---|---|
| **fixed turn order** (two different scans) | **freezes at once** — in-step pinned at 0.68 / 0.57 from the first reading, largest domain 68% / 62%, persistence 1.00, role correlation 1.00, and **the numbers differ between the two scans** |
| **random turn order** | **scatters** — steady decoherence to 0.16 |
| **resonance + headroom** (b+d, ruled 2026-10-05) | **freezes** — 49–54% of places permanently starved at B 4, 41% permanently busy in one connected network, roles 0.96–0.99, robust across box, seed and ħ (C-O47) |
| **standing Born weighting + genuine depletion** | **neither, for 1,000 ticks** — then decoheres to the random floor by 5,000 (C-O49, C-O50) |

> **The outcome of the whole line was set by a rule the ontology did not contain.** Freezing and scatter were each read at the time as fitting the picture; they cannot both. That is recorded in the ledger and it is the thing to carry forward.

**Allen has since ruled one** (RULES, 2026-10-05): first resonance plus headroom, then **standing chance at every commitment through the Born weighting**. So the gap is no longer that ED is silent on contention. **It is that the ruled principle is ED's and the weight it is computed from is ours** — see §6 and §8.1.

**And the headline of C-O44 is formally withdrawn in C-O47b:** once chance is licensed by the Born rule — a **declared input** of the ontology — the differentiation is **"scarcity plus a declared stochastic primitive,"** not scarcity alone.

---

## 4. The reach: a trend, not yet a law

C-O53's estimate, from the rates and not fitted: a drain in a medium that also consumes is screened with decay length **λ ≈ √(D/Γ)**; with D ≈ 0.033 and Γ ≈ 0.04 per tick that gives λ ≈ 0.9 steps, which is what was measured.

**C-O54 tested it. The honest tally:**

| setting | predicted λ | fitted λ | status |
|---|---|---|---|
| hop 0.2 | 0.94 | — | **one shell, unresolvable** |
| hop 0.6 | 1.54 | **0.82** | **rough** (2 shells), and **46% below prediction** |
| hop 1.0 | 1.95 | **1.75** | **agrees, within ~10%** |
| ħ 20 | 1.14 | 3.29 | **unreliable** (2 shells, negative values beyond) |
| ħ 40 | 1.47 | — | **no signal** — the knot barely depletes |

> **One setting agrees. The only other setting with any resolution is rough and sits 46% below prediction. The memory arm is inconclusive and confounded, since longer ħ also weakens the knot's own draw.** So *"confirmed quantitatively to within 10%"* rests on a single point and should not be written that way.

**What does hold is the trend:** faster flow gives longer reach, and the token deficit visibly widens — positive out to d ≈ 8 at hop 1.0 against one shell at hop 0.2.

**And a genuine structural finding came out of the scan, unlooked for:** the same drain spread over more space is **weaker near in**. The clock slowdown one shell out falls 0.0042 → 0.0025 → 0.0015 as mobility rises. **Reach and strength trade against each other.**

---

## 5. What is not shown

- **No 1/r.** The falloff is **screened**, with λ ≈ 1–2 steps. Real gravity is unscreened to infinity. And the formula itself says λ → ∞ requires **Γ → 0** — a background that almost never commits — while the ontology has becoming happening everywhere. **The more space becomes, the shorter gravity's reach.** That tension is in λ = √(D/Γ) and is not resolved.
- **No structure from the medium.** No lasting domains, no knots, no dimension arose on their own (C-O45, C-O50). Every knot in this line was **seeded**.
- **The knot's persistence is not a reading.** Held slots reserve a knot's partners by rule, so it holds by construction — the guard in card C-6 §5. The cadence-lock figures (0.97 → 0.62–0.70) describe what the rule does, not whether ED sustains matter.
- **The 1/r *shape*, if it ever appeared, would be diffusion in three dimensions** — the same caveat result 15 already makes about itself. What would be ED's is the **sink**, not the falloff law.
- **Whether C-O50 is the ontology's arrow of time is untested.** The paper's arrow is *gradients flatten toward uniform becoming* — uniform **rate**. C-O50 measured decay to random **phase**. A medium can have uniform rates and random phases. **The distinguishing reading — variance of blink rate over time, alongside the in-step share — was not taken** and is available from existing output.

---

## 6. The harness's choices, labelled

**These are ours. Each could have been otherwise, and several were shown to decide the outcome.**

| choice | status |
|---|---|
| **a place's beat advances only on its own completed blinks** | ours, after Allen's *"a clock measures its own ticking"*. **This is what makes cadence differences accumulate without limit**, and it is the proximate cause of C-O50's decoherence |
| **the pool is a place and its six neighbours, capacity B** | ours. B = 7 is the no-scarcity boundary **by construction**, not a baseline of a trend (C-O44a) |
| **W read as an amplitude in the Born weighting** | ours, and **W is not an amplitude** — it is a real match score, so squaring it is a sharpness choice rather than the Born rule. ED has a genuine amplitude in P09's `P_K = √b_K·e^{iπ_K}`, unused here |
| **PHOP, the hop probability** | ours, and **it is the D in λ = √(D/Γ)** — so the reach law contains one of our numbers |
| **the integer token store** | `b3_card.py`'s ρ, discretised (C-O47a) |
| **release to possibility at large** | a reading of the ontology, applied to **every** place and to the control, so the knot and background follow one rule |
| **λ = √(D/Γ)** | standard screening physics, borrowed. ED supplies Γ; the relation is not ED's |
| **agreement pull K = 0.5, in-step window 0.3, beat step per blink** | ours, and the pull is what the whole binding-versus-drift competition turns on |
| **ħ = 5 or 10 ticks; budget B = 4 or 6** | the quantities are ED's, **the values are ours** |
| **mutual proposals** — a pair commits only if each chooses the other | ours; it lowers the commit rate and was adopted to keep selection local and symmetric |
| **how the held slot is built** — knot places commit **only** with each other, with no cadence condition | **our implementation of Allen's b′ rule, and the exclusivity is ours.** It is also what explains the slight token *excess* just outside the knot in C-O52: shell places lose their knot-side partners, commit less, and keep more tokens |
| **knot radius 3, seeded** | ours. Nothing in the line produced a knot on its own |
| **release to possibility at large** | **a relayed proposal, adopted in practice but with no RULES entry.** It was applied to every place and to the control, so knot and background follow one rule — but it is not a recorded ruling and should either be ruled or kept labelled as ours |

---

## 7. The failed paths, and what each taught

| entry | what failed | what it established |
|---|---|---|
| **C-O45** | budget-driven desync made **scatter**, not structure — 1,200–9,250 groups, median size 1 | scarcity differentiates and does not organise |
| **C-O46** | fixed scan froze the world; two different scans gave different numbers | **ED has no contention rule**, and the missing rule was doing the work |
| **C-O47** | resonance + headroom froze it — half the places permanently starved | *"a winner burns its headroom"* assumed headroom is spent by winning; **pool room returns the moment a blink ends**, so nothing hands the turn on |
| **C-O48** | the spent token came back to the **same place** | the C-O40 lesson repeated in the discrete build: borrow-and-return is no cost |
| **C-O52** | the threshold flow rule (move only to a neighbour ≥2 lower) froze the medium | with ~1 token per place that gap almost never occurs. **A named free choice, shown to block the very transport being tested** |

**Two of the five were the same error in different clothing — C-O47 and C-O48, a cost that was not paid.** The others were scatter without structure, a rule of ours deciding the physics, and a transport rule that prevented transport. **The cost-not-paid pattern recurs more widely than this table shows**, in the smooth line at C-O40, C-O41 and C-O51, which is why it kept being rediscovered.

---

## 8. Open boundaries

1. **ED's contention rule.** The gap C-O46 opened is still open. Standing Born weighting is a *ruling*, and its W is ours; P09's actual amplitude has never been used.
2. **Why longer ħ weakens the knot's draw**, which confounded the memory half of the reach law.
3. **The rate-versus-phase reading of C-O50**, available from output already on disk.
4. **Larger lattices with lower background consumption**, so λ spans enough shells for a fit to mean anything — the present fits rest on two or three points.
5. **The screening tension of §5**: whether anything in ED permits a long reach without a vacuum that barely becomes.

---

## 9. In one paragraph

**The event layer was built and it works as a model: blinks as events, clocks as counts, a shared budget, possibility that flows and is spent.** Within it, a seeded knot held by Allen's reserved-slot rule is a net drain on the medium and **slows the clocks one step outside it by 12–15%, reproducibly** — clock slowing out of competition for becoming, with no metric anywhere in the code. **That is the line's result.** Against it: nothing organised itself, the medium decoheres to independent clocks over long runs, the reach is screened at one to two steps with no 1/r, the quantitative reach law has one supporting point, and **the rule that decides who commits when capacity is scarce is not in the ontology** — the harness supplied it, and which one it supplied determined whether the world froze, scattered, or briefly lived.

---

## 10. Corrections to this document, 2026-10-05

*The first draft was checked line by line against the ledger by the model session and five things were wrong. They are listed rather than quietly fixed, because a synthesis whose own errors are hidden is worth less than one whose are not.*

1. **The pinned-core number was misread.** 0.031 is the *drop*, not the residual rate; the shell blinks at about 0.003 against a control of 0.034. The draft's figures implied a 9% effect where the ledger records ~90%.
2. **The token deficit was quoted for one box size** and presented as if general. Box 20's values are lower (0.44, 0.36, 0.30, 0.08) and are now given alongside box 15's.
3. **"The contention rule is not in the ontology" was out of date.** True at C-O46; Allen ruled one on 2026-10-05. The accurate statement is that the *principle* is now ruled and the *weight* is ours — which §8.1 already said, so the document contradicted itself.
4. **"Three of the five failures" was two** — C-O47 and C-O48. The pattern's other instances are in the smooth line, not in that table.
5. **Hop 0.6 was called "resolvable"** where the ledger calls it rough, fitted from two shells. It is both rough *and* 46% below prediction, and now says so.

**And the §6 table was incomplete**, missing six harness choices, three of which shaped results: the agreement pull, the mutual-proposal rule, and the exclusivity in how b′ was built. **"Release to possibility at large" was also mislabelled** as a reading of the ontology; there is no RULES entry for it, and it is now marked as a relayed proposal pending a ruling.

**Two additions from the draft survive the check and are not in the ledger:** §5's rate-versus-phase point, and §6's observation that W is not an amplitude while P09's real one has never been used.
