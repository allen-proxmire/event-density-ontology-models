# The models: code for model results 1–12

*The scripts behind [../../results/MODEL_RESULTS.md](../../results/MODEL_RESULTS.md) and the clock-floor result in [../../results/RESULTS.md](../../results/RESULTS.md), as they were run, for model results 1–12 and the clock floor; the scripts for results 13–18 are held with the working record and available on request. Each script's opening comment states what it tests and was written before it ran.*

**Needs:** Python 3 with numpy and scipy. Every model runs on a 32×32×32 periodic grid; most runs take from under a minute to about half an hour on a laptop. Each script prints a one-line JSON summary and writes a JSON file of its full trajectory.

**The base model** is [b3_card.py](b3_card.py): uncommitted possibility ρ and committed becoming c on each site; clock rate r = 1/(1 + s·c); each site sends D·r·ρ to each of its six neighbours; above a threshold θ a fraction κ of the excess commits; committed becoming dissolves back into possibility at c/ħ. Everything else is built on it. The switch value *P = s·κ·ħ·θ* is the quantity in result 1.

---

## Which script reproduces which result

| result | script(s) | example | what to look for |
|---|---|---|---|
| **1. The switch** | `b3_switch.py` | `python b3_switch.py` | ripples in a dense uniform state fade below P = 1 and grow above it, at two ħ |
| **2. Memory is the present state** | `b3_knockout.py`, `b3_knockout_big.py` | `python b3_knockout.py` | a knocked-out clump re-forms where its free stuff remains, and follows it when moved |
| **3. The arc, and both endings** | `b3_expand.py` (expansion), `b5_spend.py` (spending), `b6.py` (both) | `python b5_spend.py 100 0.01` | committed fraction rises, peaks and returns to zero |
| **4. The lifetime estimate** | `b3_peak.py` → `b3_leaklaw.py` → `b3_halo.py` (run in that order: the first saves the peak states the others read) | `python b3_peak.py` | predicted against measured death for each setting |
| **5. ħ shelters structure** | `b6p.py` (against thinning), `b5b.py` (under spending) | `python b5b.py 100 0.01 1` | lifetime against ħ at fixed drive |
| **6. Grains and exclusion** | `b4_grains.py` (grain model), `b4b.py`–`b4f.py` (switch against density) | `python b4f.py DENSITY THG P SWEEPS SEED` | same switch with grains; none with one grain per place |
| **7. Hosting and merging** | `b7.py` (strong with weak), `b8.py` (strong with strong) | `python b7.py 2.0 1 1` | the weak pattern's lifetime with and without the strong one |
| **8. Bind or part; selection** | `b9.py` (in step / opposite phase), `b11.py`, `b11b.py`, `b11c.py` (selection by surroundings) | `python b9.py 1 1.0` | opposite phase: cancelled slowing, separation, early death |
| **9. Local agreement at commitment** | `b12.py` (One Being and scattered starts), `b14.py` (P11 with the commitment filter and its controls) | `python b12.py 0 1`; `python b14.py 2 scr 1 1` (arms: 0 none, 1 random, 2 medium target, 3 constant, 4 phase-blind, 5 frozen pattern; set `B14_NOSIGN=1` for the form result 9 reports, without the flow sign) | alignment held from the start; under P11, structure with agreement and none without |
| **10. The medium orders itself** | `b15.py` | `python b15.py p11 0 1` | agreement between neighbouring regions and whole-medium alignment over the run |
| **11. Where new events go** | `b16.py` | `python b16.py pres R1 live 1` | lifetime and structure for readings R1–R4 at matched total thinning |
| **12. The rate of commitment is the clock** | `b17.py`, with `b17_batch.sh` and `b17_stageB.sh` for the full sets | `python b17.py pres both 1 1 R1 live 1` | arm `old` (common clock) against `both` (local clock) |
| **Clock floor** (RESULTS.md, result 2) | `timing_scaling.py`, with `n1_sync.py` and `shapes.py` | `python timing_scaling.py` | the coupling needed to hold clocks together, against size, by dimension |

**Arguments** are listed in each script's opening comment (`Usage:`). Seeds are fixed, so a run reproduces its numbers exactly.

**The handedness theorem** has its own check: `python ../../results/Handedness/check_result.py`.

The code for the CDT calculation and for the dimension runs, and the full working record behind every script — ledgers, dated notes, logs and data — is held separately and available on request.
