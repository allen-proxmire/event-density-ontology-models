"""Model B-3b: the ink drop with expansion ("new places keep being born"; paper s12, heat death is ED thinning).

Same model as b3_card.py, plus: each step, new places are born between the existing ones, so FREE becoming is
spread thinner - a fraction x = 3h of the free density at every site passes into the newborn places (tracked as
'leaked', so grid + leaked is conserved exactly). Committed becoming is settled and does not thin (variant
'both' thins it too). Everything else identical.
"""
import sys, json
import numpy as np
import b3_card as m

m.B = 4


def run(s, L, h, seed, thin_committed=False, T=30000, every=500, eps=1e-3):
    rng = np.random.default_rng(seed)
    rho, c = m.drop(rng, eps)
    total0 = (rho + c).sum(); leaked = 0.0
    x = 3 * h
    rows = []; peak_c = 0.0; death = None
    for t in range(T + 1):
        if t % every == 0:
            tot = rho + c
            n, big = m.clusters(c)
            cf = float(c.sum() / total0)
            peak_c = max(peak_c, cf)
            if death is None and peak_c > 0.05 and cf < 0.01:
                death = t
            rows.append(dict(t=t, K=m.complexity(tot), cfrac=cf, ncl=n, big=big,
                             free_mean=float(rho.mean()), spread=float(tot.std() / tot.mean())))
        if t < T:
            rho, c = m.step(rho, c, s, L)
            lost = x * rho; leaked += lost.sum(); rho = rho - lost
            if thin_committed:
                lc = x * c; leaked += lc.sum(); c = c - lc
    drift = abs((rho + c).sum() + leaked - total0) / total0
    return rows, death, drift


if __name__ == "__main__":
    out = []
    for h in (0.0, 1e-4, 3e-4):
        for L in (10, 100):
            for s in (1.0, 10.0):
                for seed in (1, 2):
                    rows, death, drift = run(s, L, h, seed)
                    K = [r["K"] for r in rows]; ipk = int(np.argmax(K))
                    summ = dict(h=h, L=L, s=s, seed=seed, Kpeak=K[ipk], t_peak=rows[ipk]["t"], Kend=K[-1],
                                cpeak=max(r["cfrac"] for r in rows), cend=rows[-1]["cfrac"], death=death,
                                ncl_end=rows[-1]["ncl"], free_end=rows[-1]["free_mean"], drift=float(drift))
                    out.append(dict(summary=summ, rows=rows)); print(summ); sys.stdout.flush()
    for L in (10, 100):   # variant: committed matter thins too
        rows, death, drift = run(10.0, L, 1e-4, 1, thin_committed=True)
        K = [r["K"] for r in rows]
        summ = dict(variant="both_thin", h=1e-4, L=L, s=10.0, seed=1, Kpeak=max(K), Kend=K[-1], death=death,
                    cend=rows[-1]["cfrac"], drift=float(drift))
        out.append(dict(summary=summ, rows=rows)); print(summ); sys.stdout.flush()
    json.dump(out, open("b3_expand.json", "w"))
