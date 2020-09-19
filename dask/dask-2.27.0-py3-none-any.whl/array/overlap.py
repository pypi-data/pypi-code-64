import warnings
from operator import getitem
from itertools import product
from numbers import Integral
from tlz import merge, pipe, concat, partial, get
from tlz.curried import map

from . import chunk, wrap
from .core import (
    Array,
    map_blocks,
    concatenate,
    concatenate3,
    reshapelist,
    unify_chunks,
)
from ..highlevelgraph import HighLevelGraph
from ..base import tokenize
from ..core import flatten
from ..utils import concrete


def fractional_slice(task, axes):
    """

    >>> fractional_slice(('x', 5.1), {0: 2})  # doctest: +SKIP
    (getitem, ('x', 6), (slice(0, 2),))

    >>> fractional_slice(('x', 3, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(None, None, None), slice(-3, None)))

    >>> fractional_slice(('x', 2.9, 5.1), {0: 2, 1: 3})  # doctest: +SKIP
    (getitem, ('x', 3, 5), (slice(0, 2), slice(-3, None)))
    """
    rounded = (task[0],) + tuple(int(round(i)) for i in task[1:])

    index = []
    for i, (t, r) in enumerate(zip(task[1:], rounded[1:])):
        depth = axes.get(i, 0)
        if isinstance(depth, tuple):
            left_depth = depth[0]
            right_depth = depth[1]
        else:
            left_depth = depth
            right_depth = depth

        if t == r:
            index.append(slice(None, None, None))
        elif t < r and right_depth:
            index.append(slice(0, right_depth))
        elif t > r and left_depth:
            index.append(slice(-left_depth, None))
        else:
            index.append(slice(0, 0))
    index = tuple(index)

    if all(ind == slice(None, None, None) for ind in index):
        return task
    else:
        return (getitem, rounded, index)


def expand_key(k, dims, name=None, axes=None):
    """Get all neighboring keys around center

    Parameters
    ----------
    k: tuple
        They key around which to generate new keys
    dims: Sequence[int]
        The number of chunks in each dimension
    name: Option[str]
        The name to include in the output keys, or none to include no name
    axes: Dict[int, int]
        The axes active in the expansion.  We don't expand on non-active axes

    Examples
    --------
    >>> expand_key(('x', 2, 3), dims=[5, 5], name='y', axes={0: 1, 1: 1})  # doctest: +NORMALIZE_WHITESPACE
    [[('y', 1.1, 2.1), ('y', 1.1, 3), ('y', 1.1, 3.9)],
     [('y',   2, 2.1), ('y',   2, 3), ('y',   2, 3.9)],
     [('y', 2.9, 2.1), ('y', 2.9, 3), ('y', 2.9, 3.9)]]

    >>> expand_key(('x', 0, 4), dims=[5, 5], name='y', axes={0: 1, 1: 1})  # doctest: +NORMALIZE_WHITESPACE
    [[('y',   0, 3.1), ('y',   0,   4)],
     [('y', 0.9, 3.1), ('y', 0.9,   4)]]
    """

    def inds(i, ind):
        rv = []
        if ind - 0.9 > 0:
            rv.append(ind - 0.9)
        rv.append(ind)
        if ind + 0.9 < dims[i] - 1:
            rv.append(ind + 0.9)
        return rv

    shape = []
    for i, ind in enumerate(k[1:]):
        num = 1
        if ind > 0:
            num += 1
        if ind < dims[i] - 1:
            num += 1
        shape.append(num)

    args = [
        inds(i, ind) if any((axes.get(i, 0),)) else [ind] for i, ind in enumerate(k[1:])
    ]
    if name is not None:
        args = [[name]] + args
    seq = list(product(*args))
    shape2 = [d if any((axes.get(i, 0),)) else 1 for i, d in enumerate(shape)]
    result = reshapelist(shape2, seq)
    return result


def overlap_internal(x, axes):
    """Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    axes: dict
        The size of the shared boundary per axis

    The axes input informs how many cells to overlap between neighboring blocks
    {0: 2, 2: 5} means share two cells in 0 axis, 5 cells in 2 axis
    """
    dims = list(map(len, x.chunks))
    expand_key2 = partial(expand_key, dims=dims, axes=axes)

    # Make keys for each of the surrounding sub-arrays
    interior_keys = pipe(
        x.__dask_keys__(), flatten, map(expand_key2), map(flatten), concat, list
    )

    name = "overlap-" + tokenize(x, axes)
    getitem_name = "getitem-" + tokenize(x, axes)
    interior_slices = {}
    overlap_blocks = {}
    for k in interior_keys:
        frac_slice = fractional_slice((x.name,) + k, axes)
        if (x.name,) + k != frac_slice:
            interior_slices[(getitem_name,) + k] = frac_slice
        else:
            interior_slices[(getitem_name,) + k] = (x.name,) + k
            overlap_blocks[(name,) + k] = (
                concatenate3,
                (concrete, expand_key2((None,) + k, name=getitem_name)),
            )

    chunks = []
    for i, bds in enumerate(x.chunks):
        depth = axes.get(i, 0)
        if isinstance(depth, tuple):
            left_depth = depth[0]
            right_depth = depth[1]
        else:
            left_depth = depth
            right_depth = depth

        if len(bds) == 1:
            chunks.append(bds)
        else:
            left = [bds[0] + right_depth]
            right = [bds[-1] + left_depth]
            mid = []
            for bd in bds[1:-1]:
                mid.append(bd + left_depth + right_depth)
            chunks.append(left + mid + right)

    dsk = merge(interior_slices, overlap_blocks)
    graph = HighLevelGraph.from_collections(name, dsk, dependencies=[x])

    return Array(graph, name, chunks, meta=x)


def trim_overlap(x, depth, boundary=None):
    """Trim sides from each block.

    This couples well with the ``map_overlap`` operation which may leave
    excess data on each block.

    See also
    --------
    dask.array.overlap.map_overlap

    """

    # parameter to be passed to trim_internal
    axes = coerce_depth(x.ndim, depth)
    boundary2 = coerce_boundary(x.ndim, boundary)
    return trim_internal(x, axes=axes, boundary=boundary2)


def trim_internal(x, axes, boundary=None):
    """Trim sides from each block

    This couples well with the overlap operation, which may leave excess data on
    each block

    See also
    --------
    dask.array.chunk.trim
    dask.array.map_blocks
    """
    boundary = coerce_boundary(x.ndim, boundary)

    olist = []
    for i, bd in enumerate(x.chunks):
        bdy = boundary.get(i, "none")
        overlap = axes.get(i, 0)
        ilist = []
        for j, d in enumerate(bd):
            if bdy != "none":
                if isinstance(overlap, tuple):
                    d = d - sum(overlap)
                else:
                    d = d - overlap * 2

            else:
                if isinstance(overlap, tuple):
                    d = d - overlap[0] if j != 0 else d
                    d = d - overlap[1] if j != len(bd) - 1 else d
                else:
                    d = d - overlap if j != 0 else d
                    d = d - overlap if j != len(bd) - 1 else d

            ilist.append(d)
        olist.append(tuple(ilist))
    chunks = tuple(olist)

    return map_blocks(
        partial(_trim, axes=axes, boundary=boundary),
        x,
        chunks=chunks,
        dtype=x.dtype,
        meta=x._meta,
    )


def _trim(x, axes, boundary, block_info):
    """Similar to dask.array.chunk.trim but requires one to specificy the
    boundary condition.

    ``axes``, and ``boundary`` are assumed to have been coerced.

    """
    axes = [axes.get(i, 0) for i in range(x.ndim)]
    axes_front = (ax[0] if isinstance(ax, tuple) else ax for ax in axes)
    axes_back = (
        -ax[1]
        if isinstance(ax, tuple) and ax[1]
        else -ax
        if isinstance(ax, Integral) and ax
        else None
        for ax in axes
    )

    trim_front = (
        0 if (chunk_location == 0 and boundary.get(i, "none") == "none") else ax
        for i, (chunk_location, ax) in enumerate(
            zip(block_info[0]["chunk-location"], axes_front)
        )
    )
    trim_back = (
        None
        if (chunk_location == chunks - 1 and boundary.get(i, "none") == "none")
        else ax
        for i, (chunks, chunk_location, ax) in enumerate(
            zip(block_info[0]["num-chunks"], block_info[0]["chunk-location"], axes_back)
        )
    )
    ind = tuple(slice(front, back) for front, back in zip(trim_front, trim_back))
    return x[ind]


def periodic(x, axis, depth):
    """Copy a slice of an array around to its other side

    Useful to create periodic boundary conditions for overlap
    """

    left = (
        (slice(None, None, None),) * axis
        + (slice(0, depth),)
        + (slice(None, None, None),) * (x.ndim - axis - 1)
    )
    right = (
        (slice(None, None, None),) * axis
        + (slice(-depth, None),)
        + (slice(None, None, None),) * (x.ndim - axis - 1)
    )
    l = x[left]
    r = x[right]

    l, r = _remove_overlap_boundaries(l, r, axis, depth)

    return concatenate([r, x, l], axis=axis)


def reflect(x, axis, depth):
    """Reflect boundaries of array on the same side

    This is the converse of ``periodic``
    """
    if depth == 1:
        left = (
            (slice(None, None, None),) * axis
            + (slice(0, 1),)
            + (slice(None, None, None),) * (x.ndim - axis - 1)
        )
    else:
        left = (
            (slice(None, None, None),) * axis
            + (slice(depth - 1, None, -1),)
            + (slice(None, None, None),) * (x.ndim - axis - 1)
        )
    right = (
        (slice(None, None, None),) * axis
        + (slice(-1, -depth - 1, -1),)
        + (slice(None, None, None),) * (x.ndim - axis - 1)
    )
    l = x[left]
    r = x[right]

    l, r = _remove_overlap_boundaries(l, r, axis, depth)

    return concatenate([l, x, r], axis=axis)


def nearest(x, axis, depth):
    """Each reflect each boundary value outwards

    This mimics what the skimage.filters.gaussian_filter(... mode="nearest")
    does.
    """
    left = (
        (slice(None, None, None),) * axis
        + (slice(0, 1),)
        + (slice(None, None, None),) * (x.ndim - axis - 1)
    )
    right = (
        (slice(None, None, None),) * axis
        + (slice(-1, -2, -1),)
        + (slice(None, None, None),) * (x.ndim - axis - 1)
    )

    l = concatenate([x[left]] * depth, axis=axis)
    r = concatenate([x[right]] * depth, axis=axis)

    l, r = _remove_overlap_boundaries(l, r, axis, depth)

    return concatenate([l, x, r], axis=axis)


def constant(x, axis, depth, value):
    """ Add constant slice to either side of array """
    chunks = list(x.chunks)
    chunks[axis] = (depth,)

    try:
        c = wrap.full_like(
            getattr(x, "_meta", x),
            value,
            shape=tuple(map(sum, chunks)),
            chunks=tuple(chunks),
            dtype=x.dtype,
        )
    except TypeError:
        c = wrap.full(
            tuple(map(sum, chunks)), value, chunks=tuple(chunks), dtype=x.dtype
        )

    return concatenate([c, x, c], axis=axis)


def _remove_overlap_boundaries(l, r, axis, depth):
    lchunks = list(l.chunks)
    lchunks[axis] = (depth,)
    rchunks = list(r.chunks)
    rchunks[axis] = (depth,)

    l = l.rechunk(tuple(lchunks))
    r = r.rechunk(tuple(rchunks))
    return l, r


def boundaries(x, depth=None, kind=None):
    """Add boundary conditions to an array before overlaping

    See Also
    --------
    periodic
    constant
    """
    if not isinstance(kind, dict):
        kind = dict((i, kind) for i in range(x.ndim))
    if not isinstance(depth, dict):
        depth = dict((i, depth) for i in range(x.ndim))

    for i in range(x.ndim):
        d = depth.get(i, 0)
        if d == 0:
            continue

        this_kind = kind.get(i, "none")
        if this_kind == "none":
            continue
        elif this_kind == "periodic":
            x = periodic(x, i, d)
        elif this_kind == "reflect":
            x = reflect(x, i, d)
        elif this_kind == "nearest":
            x = nearest(x, i, d)
        elif i in kind:
            x = constant(x, i, d, kind[i])

    return x


def overlap(x, depth, boundary):
    """Share boundaries between neighboring blocks

    Parameters
    ----------

    x: da.Array
        A dask array
    depth: dict
        The size of the shared boundary per axis
    boundary: dict
        The boundary condition on each axis. Options are 'reflect', 'periodic',
        'nearest', 'none', or an array value.  Such a value will fill the
        boundary with that value.

    The depth input informs how many cells to overlap between neighboring
    blocks ``{0: 2, 2: 5}`` means share two cells in 0 axis, 5 cells in 2 axis.
    Axes missing from this input will not be overlapped.

    Examples
    --------
    >>> import numpy as np
    >>> import dask.array as da

    >>> x = np.arange(64).reshape((8, 8))
    >>> d = da.from_array(x, chunks=(4, 4))
    >>> d.chunks
    ((4, 4), (4, 4))

    >>> g = da.overlap.overlap(d, depth={0: 2, 1: 1},
    ...                       boundary={0: 100, 1: 'reflect'})
    >>> g.chunks
    ((8, 8), (6, 6))

    >>> np.array(g)
    array([[100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [  0,   0,   1,   2,   3,   4,   3,   4,   5,   6,   7,   7],
           [  8,   8,   9,  10,  11,  12,  11,  12,  13,  14,  15,  15],
           [ 16,  16,  17,  18,  19,  20,  19,  20,  21,  22,  23,  23],
           [ 24,  24,  25,  26,  27,  28,  27,  28,  29,  30,  31,  31],
           [ 32,  32,  33,  34,  35,  36,  35,  36,  37,  38,  39,  39],
           [ 40,  40,  41,  42,  43,  44,  43,  44,  45,  46,  47,  47],
           [ 16,  16,  17,  18,  19,  20,  19,  20,  21,  22,  23,  23],
           [ 24,  24,  25,  26,  27,  28,  27,  28,  29,  30,  31,  31],
           [ 32,  32,  33,  34,  35,  36,  35,  36,  37,  38,  39,  39],
           [ 40,  40,  41,  42,  43,  44,  43,  44,  45,  46,  47,  47],
           [ 48,  48,  49,  50,  51,  52,  51,  52,  53,  54,  55,  55],
           [ 56,  56,  57,  58,  59,  60,  59,  60,  61,  62,  63,  63],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
           [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100]])
    """
    depth2 = coerce_depth(x.ndim, depth)
    boundary2 = coerce_boundary(x.ndim, boundary)

    # is depth larger than chunk size?
    depth_values = [depth2.get(i, 0) for i in range(x.ndim)]
    for d, c in zip(depth_values, x.chunks):
        maxd = max(d) if isinstance(d, tuple) else d
        if maxd > min(c):
            raise ValueError(
                "The overlapping depth %d is larger than your\n"
                "smallest chunk size %d. Rechunk your array\n"
                "with a larger chunk size or a chunk size that\n"
                "more evenly divides the shape of your array." % (d, min(c))
            )
    x2 = boundaries(x, depth2, boundary2)
    x3 = overlap_internal(x2, depth2)
    trim = dict(
        (k, v * 2 if boundary2.get(k, "none") != "none" else 0)
        for k, v in depth2.items()
    )
    x4 = chunk.trim(x3, trim)
    return x4


def add_dummy_padding(x, depth, boundary):
    """
    Pads an array which has 'none' as the boundary type.
    Used to simplify trimming arrays which use 'none'.

    >>> import dask.array as da
    >>> x = da.arange(6, chunks=3)
    >>> add_dummy_padding(x, {0: 1}, {0: 'none'}).compute()  # doctest: +NORMALIZE_WHITESPACE
    array([..., 0, 1, 2, 3, 4, 5, ...])
    """
    for k, v in boundary.items():
        d = depth.get(k, 0)
        if v == "none" and d > 0:
            empty_shape = list(x.shape)
            empty_shape[k] = d

            empty_chunks = list(x.chunks)
            empty_chunks[k] = (d,)

            try:
                empty = wrap.empty_like(
                    getattr(x, "_meta", x),
                    shape=empty_shape,
                    chunks=empty_chunks,
                    dtype=x.dtype,
                )
            except TypeError:
                empty = wrap.empty(empty_shape, chunks=empty_chunks, dtype=x.dtype)

            out_chunks = list(x.chunks)
            ax_chunks = list(out_chunks[k])
            ax_chunks[0] += d
            ax_chunks[-1] += d
            out_chunks[k] = tuple(ax_chunks)

            x = concatenate([empty, x, empty], axis=k)
            x = x.rechunk(out_chunks)
    return x


def map_overlap(
    func, *args, depth=None, boundary=None, trim=True, align_arrays=True, **kwargs
):
    """Map a function over blocks of arrays with some overlap

    We share neighboring zones between blocks of the array, map a
    function, and then trim away the neighboring strips.

    Parameters
    ----------
    func: function
        The function to apply to each extended block.
        If multiple arrays are provided, then the function should expect to
        receive chunks of each array in the same order.
    args : dask arrays
    depth: int, tuple, dict or list
        The number of elements that each block should share with its neighbors
        If a tuple or dict then this can be different per axis.
        If a list then each element of that list must be an int, tuple or dict
        defining depth for the corresponding array in `args`.
        Asymmetric depths may be specified using a dict value of (-/+) tuples.
        Note that asymmetric depths are currently only supported when
        ``boundary`` is 'none'.
        The default value is 0.
    boundary: str, tuple, dict or list
        How to handle the boundaries.
        Values include 'reflect', 'periodic', 'nearest', 'none',
        or any constant value like 0 or np.nan.
        If a list then each element must be a str, tuple or dict defining the
        boundary for the corresponding array in `args`.
        The default value is 'reflect'.
    trim: bool
        Whether or not to trim ``depth`` elements from each block after
        calling the map function.
        Set this to False if your mapping function already does this for you
    align_arrays: bool
        Whether or not to align chunks along equally sized dimensions when
        multiple arrays are provided.  This allows for larger chunks in some
        arrays to be broken into smaller ones that match chunk sizes in other
        arrays such that they are compatible for block function mapping. If
        this is false, then an error will be thrown if arrays do not already
        have the same number of blocks in each dimension.
    **kwargs:
        Other keyword arguments valid in ``map_blocks``

    Examples
    --------
    >>> import numpy as np
    >>> import dask.array as da

    >>> x = np.array([1, 1, 2, 3, 3, 3, 2, 1, 1])
    >>> x = da.from_array(x, chunks=5)
    >>> def derivative(x):
    ...     return x - np.roll(x, 1)

    >>> y = x.map_overlap(derivative, depth=1, boundary=0)
    >>> y.compute()
    array([ 1,  0,  1,  1,  0,  0, -1, -1,  0])

    >>> x = np.arange(16).reshape((4, 4))
    >>> d = da.from_array(x, chunks=(2, 2))
    >>> d.map_overlap(lambda x: x + x.size, depth=1).compute()
    array([[16, 17, 18, 19],
           [20, 21, 22, 23],
           [24, 25, 26, 27],
           [28, 29, 30, 31]])

    >>> func = lambda x: x + x.size
    >>> depth = {0: 1, 1: 1}
    >>> boundary = {0: 'reflect', 1: 'none'}
    >>> d.map_overlap(func, depth, boundary).compute()  # doctest: +NORMALIZE_WHITESPACE
    array([[12,  13,  14,  15],
           [16,  17,  18,  19],
           [20,  21,  22,  23],
           [24,  25,  26,  27]])

    The ``da.map_overlap`` function can also accept multiple arrays.

    >>> func = lambda x, y: x + y
    >>> x = da.arange(8).reshape(2, 4).rechunk((1, 2))
    >>> y = da.arange(4).rechunk(2)
    >>> da.map_overlap(func, x, y, depth=1).compute() # doctest: +NORMALIZE_WHITESPACE
    array([[ 0,  2,  4,  6],
           [ 4,  6,  8,  10]])

    When multiple arrays are given, they do not need to have the
    same number of dimensions but they must broadcast together.
    Arrays are aligned block by block (just as in ``da.map_blocks``)
    so the blocks must have a common chunk size.  This common chunking
    is determined automatically as long as ``align_arrays`` is True.

    >>> x = da.arange(8, chunks=4)
    >>> y = da.arange(8, chunks=2)
    >>> r = da.map_overlap(func, x, y, depth=1, align_arrays=True)
    >>> len(r.to_delayed())
    4

    >>> da.map_overlap(func, x, y, depth=1, align_arrays=False).compute()
    Traceback (most recent call last):
        ...
    ValueError: Shapes do not align {'.0': {2, 4}}

    Note also that this function is equivalent to ``map_blocks``
    by default.  A non-zero ``depth`` must be defined for any
    overlap to appear in the arrays provided to ``func``.

    >>> func = lambda x: x.sum()
    >>> x = da.ones(10, dtype='int')
    >>> block_args = dict(chunks=(), drop_axis=0)
    >>> da.map_blocks(func, x, **block_args).compute()
    10
    >>> da.map_overlap(func, x, **block_args).compute()
    10
    >>> da.map_overlap(func, x, **block_args, depth=1).compute()
    12
    """
    # Look for invocation using deprecated single-array signature
    # map_overlap(x, func, depth, boundary=None, trim=True, **kwargs)
    if isinstance(func, Array) and callable(args[0]):
        warnings.warn(
            "The use of map_overlap(array, func, **kwargs) is deprecated since dask 2.17.0 "
            "and will be an error in a future release. To silence this warning, use the syntax "
            "map_overlap(func, array0,[ array1, ...,] **kwargs) instead.",
            FutureWarning,
        )
        sig = ["func", "depth", "boundary", "trim"]
        depth = get(sig.index("depth"), args, depth)
        boundary = get(sig.index("boundary"), args, boundary)
        trim = get(sig.index("trim"), args, trim)
        func, args = args[0], [func]

    if not callable(func):
        raise TypeError(
            "First argument must be callable function, not {}\n"
            "Usage:   da.map_overlap(function, x)\n"
            "   or:   da.map_overlap(function, x, y, z)".format(type(func).__name__)
        )
    if not all(isinstance(x, Array) for x in args):
        raise TypeError(
            "All variadic arguments must be arrays, not {}\n"
            "Usage:   da.map_overlap(function, x)\n"
            "   or:   da.map_overlap(function, x, y, z)".format(
                [type(x).__name__ for x in args]
            )
        )

    # Coerce depth and boundary arguments to lists of individual
    # specifications for each array argument
    def coerce(xs, arg, fn):
        if not isinstance(arg, list):
            arg = [arg] * len(xs)
        return [fn(x.ndim, a) for x, a in zip(xs, arg)]

    depth = coerce(args, depth, coerce_depth)
    boundary = coerce(args, boundary, coerce_boundary)

    # Align chunks in each array to a common size
    if align_arrays:
        # Reverse unification order to allow block broadcasting
        inds = [list(reversed(range(x.ndim))) for x in args]
        _, args = unify_chunks(*list(concat(zip(args, inds))), warn=False)

    for i, x in enumerate(args):
        for j in range(x.ndim):
            if isinstance(depth[i][j], tuple) and boundary[i][j] != "none":
                raise NotImplementedError(
                    "Asymmetric overlap is currently only implemented "
                    "for boundary='none', however boundary for dimension "
                    "{} in array argument {} is {}".format(j, i, boundary[i][j])
                )

    def assert_int_chunksize(xs):
        assert all(type(c) is int for x in xs for cc in x.chunks for c in cc)

    assert_int_chunksize(args)
    args = [overlap(x, depth=d, boundary=b) for x, d, b in zip(args, depth, boundary)]
    assert_int_chunksize(args)
    x = map_blocks(func, *args, **kwargs)
    assert_int_chunksize([x])
    if trim:
        # Find index of array argument with maximum rank and break ties by choosing first provided
        i = sorted(enumerate(args), key=lambda v: (v[1].ndim, -v[0]))[-1][0]
        # Trim using depth/boundary setting for array of highest rank
        return trim_internal(x, depth[i], boundary[i])
    else:
        return x


def coerce_depth(ndim, depth):
    default = 0
    if depth is None:
        depth = default
    if isinstance(depth, Integral):
        depth = (depth,) * ndim
    if isinstance(depth, tuple):
        depth = dict(zip(range(ndim), depth))
    if isinstance(depth, dict):
        for i in range(ndim):
            if i not in depth:
                depth[i] = 0
    return depth


def coerce_boundary(ndim, boundary):
    default = "reflect"
    if boundary is None:
        boundary = default
    if not isinstance(boundary, (tuple, dict)):
        boundary = (boundary,) * ndim
    if isinstance(boundary, tuple):
        boundary = dict(zip(range(ndim), boundary))
    if isinstance(boundary, dict):
        for i in range(ndim):
            if i not in boundary:
                boundary[i] = default
    return boundary
