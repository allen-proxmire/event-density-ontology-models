"""Third and fourth expansion rates for the dilution law (does h * t_death stay constant?).
Earlier rates: h = 1e-4 and 3e-4 (b3_expand.log, b3_censored.log). Adds h = 1e-3 (fast) and h = 3e-5 (slow)."""
import json
import b3_expand as e
out = []
for h, T in ((1e-3, 40000), (3e-5, 400000)):
    for L in (10, 100):
        for s in (1.0, 10.0):
            rows, death, drift = e.run(s, L, h, 1, T=T, every=500)
            d = dict(h=h, L=L, s=s, death=death, h_x_death=(None if death is None else round(h * death, 3)), drift=float(drift))
            out.append(d); print(d, flush=True)
json.dump(out, open("b3_dilution.json", "w"), indent=1)
