"""Attempt B: the reference shapes every observable is calibrated against.

FOUR KINDS, and the naming is deliberate. The third is a REFERENCE, not a target - a known object whose values
can be checked, used to verify an instrument responds. It is not what a model is supposed to become. Calling it
a target would encode "lattice = success" into the infrastructure and kill principle 2 on the first day.

  null          a random regular web at the same link budget - maximum disorder, locally tree-like, expander
  intermediate  a flat torus progressively damaged by budget-preserving rewiring - a LADDER, not one point
  reference     a flat torus of the matching dimension - values known analytically
  control       a TRIANGULAR lattice: link budget 6 but TWO-dimensional

The control exists because attempt 14 assumed budget 6 meant three dimensions throughout and never checked. If a
dimension observable reads 2 on the triangular lattice it is reading dimension; if it reads 3 it is reading the
link budget, and it is worthless. No observable enters the Attempt B set without passing that.

RECORDED GAP: there is no negative-curvature reference here. A hyperbolic tiling at fixed degree (e.g. {4,6}) is
buildable and would test whether the set can tell curved-but-geometric from disordered - which matters, since the
one published ordered phase of this kind is hyperbolic. Not built yet; recorded rather than glossed.
"""
import numpy as np
import scipy.sparse as sp


def _A(n, pairs):
    rows = [a for a, b in pairs] + [b for a, b in pairs]
    cols = [b for a, b in pairs] + [a for a, b in pairs]
    A = sp.csr_matrix((np.ones(len(rows)), (rows, cols)), shape=(n, n))
    A.data[:] = 1.0
    A.sum_duplicates()
    A.data[:] = 1.0
    return A


def torus(side, D):
    """Flat D-dimensional torus, link budget 2D."""
    n = side ** D
    idx = np.arange(n)
    pairs = []
    for d in range(D):
        st = side ** d
        c = (idx // st) % side
        nb = idx + ((c + 1) % side - c) * st
        pairs += list(zip(idx.tolist(), nb.tolist()))
    return _A(n, pairs)


def triangular(side):
    """Triangular lattice on a torus: link budget 6, but TWO-dimensional. The control."""
    n = side * side
    pairs = []
    for y in range(side):
        for x in range(side):
            v = y * side + x
            for dx, dy in ((1, 0), (0, 1), (1, 1)):
                pairs.append((v, ((y + dy) % side) * side + (x + dx) % side))
    return _A(n, pairs)


def web(n, deg, rng):
    """Random regular web at the given link budget. The null case."""
    for _ in range(200):
        stubs = np.repeat(np.arange(n), deg)
        rng.shuffle(stubs)
        pairs = list(zip(stubs[0::2].tolist(), stubs[1::2].tolist()))
        if any(a == b for a, b in pairs):
            continue
        A = _A(n, pairs)
        if A.nnz == n * deg:
            return A
    return A


def tree(deg, depth):
    """A regular tree at the given link budget: the LOOP-FREE extreme of negative curvature.

    Every interior event has `deg` relations; the boundary is large and unavoidable, which is intrinsic to a
    negatively curved object at finite size rather than a flaw in the construction. Reported, not hidden.
    """
    pairs = []
    frontier = [0]
    nxt_id = 1
    for d in range(depth):
        new = []
        for v in frontier:
            kids = deg if v == 0 else deg - 1
            for _ in range(kids):
                pairs.append((v, nxt_id))
                new.append(nxt_id)
                nxt_id += 1
        frontier = new
    return _A(nxt_id, pairs)


def tree_times_cycle(tree_deg, depth, k):
    """An ORDERED, NEGATIVELY CURVED, SQUARE-RICH shape at a fixed link budget - the reference class the set was
    missing, and the one the B-1 trigger asks for.

    A regular tree crossed with a cycle. Every event is (tree node, position on the cycle); it keeps its tree
    relations at fixed position and its cycle relations at fixed node, so the budget is tree_deg + 2 exactly in
    the interior. Every tree relation paired with every cycle relation closes a SQUARE, so the shape is square-
    rich like a flat lattice, while inheriting the tree's EXPONENTIAL growth - which is what makes it hyperbolic
    rather than flat. It is quasi-isometric to a tree.

    NOT a {4,6} tiling, and not claimed to be. It is a construction whose properties can be checked directly:
    fixed budget, all faces squares, exponential volume growth, negative curvature. That is the reference class
    the calibration lacked. Recorded honestly in case {4,6} itself is wanted later.
    """
    T = tree(tree_deg, depth).tocsr()
    m = T.shape[0]
    tp = [(i, j) for i in range(m) for j in T.indices[T.indptr[i]:T.indptr[i + 1]].tolist() if i < j]
    pairs = []
    for i, j in tp:                                          # tree relations, at each position on the cycle
        for c in range(k):
            pairs.append((i * k + c, j * k + c))
    for i in range(m):                                       # cycle relations, at each tree node
        for c in range(k):
            pairs.append((i * k + c, i * k + (c + 1) % k))
    return _A(m * k, pairs)


def times_cycle(B, k):
    """Any shape crossed with a cycle: adds 2 to the link budget and makes every relation square-rich.

    Why this exists. A finite TREE is mostly boundary - a degree-6 tree of depth 4 has mean degree 4.00 against an
    interior 6 - so it cannot be compared with a closed degree-6 web. Crossing a CLOSED shape with a cycle keeps
    it closed. So `times_cycle(web(m, 4), k)` gives a shape that is:
        closed, budget 6 exactly, SQUARE-RICH like a flat lattice, and with a web's SHORT distances.
    That combination - loops everywhere but nowhere far to go - is precisely the reference the set was missing,
    and precisely the thing B-1's attractor has to be told apart from.
    """
    B = B.tocsr()
    m = B.shape[0]
    be = [(i, j) for i in range(m) for j in B.indices[B.indptr[i]:B.indptr[i + 1]].tolist() if i < j]
    pairs = []
    for i, j in be:
        for c in range(k):
            pairs.append((i * k + c, j * k + c))
    for i in range(m):
        for c in range(k):
            pairs.append((i * k + c, i * k + (c + 1) % k))
    return _A(m * k, pairs)


def to_adj(A):
    A = A.tocsr()
    return [set(A.indices[A.indptr[i]:A.indptr[i + 1]].tolist()) for i in range(A.shape[0])]


def damaged(A, frac, rng):
    """A shape put through frac x (number of relations) budget-preserving rewirings. The intermediate ladder."""
    adjs = to_adj(A)
    n = len(adjs)
    want = int(round(frac * A.nnz / 2))
    done = tries = 0
    while done < want and tries < 200 * max(1, want):
        tries += 1
        i = int(rng.integers(n))
        k = int(rng.integers(n))
        if not adjs[i] or not adjs[k]:
            continue
        j = int(rng.choice(sorted(adjs[i])))
        l = int(rng.choice(sorted(adjs[k])))
        if len({i, j, k, l}) != 4 or k in adjs[i] or l in adjs[j]:
            continue
        for a, b in ((i, j), (k, l)):
            adjs[a].discard(b)
            adjs[b].discard(a)
        for a, b in ((i, k), (j, l)):
            adjs[a].add(b)
            adjs[b].add(a)
        done += 1
    pairs = [(i, j) for i in range(n) for j in adjs[i] if i < j]
    return _A(n, pairs)
