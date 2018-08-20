import itertools


def every_combo(items):
    """
        Given a list of n items, return every combination of length 1 .. n.

        list(every_combo([1, 2, 3]))
        [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    return itertools.chain(*[
        itertools.combinations(items, i)
        for i in range(1, len(items) + 1)
    ])


def dict_combo(params):
    """
    params = {
        "a": ["A","B","C"],
        "b": [0, 1],
        "c": [True, False, None],
    }
    for x in dict_combo(params):
        print x

    Returns:
        {'a': 'A', 'c': True, 'b': 0}
        {'a': 'A', 'c': True, 'b': 1}
        {'a': 'A', 'c': False, 'b': 0}
        {'a': 'A', 'c': False, 'b': 1}
        {'a': 'A', 'c': None, 'b': 0}
        {'a': 'A', 'c': None, 'b': 1}
        {'a': 'B', 'c': True, 'b': 0}
        {'a': 'B', 'c': True, 'b': 1}
        {'a': 'B', 'c': False, 'b': 0}
        {'a': 'B', 'c': False, 'b': 1}
        {'a': 'B', 'c': None, 'b': 0}
        {'a': 'B', 'c': None, 'b': 1}
        {'a': 'C', 'c': True, 'b': 0}
        {'a': 'C', 'c': True, 'b': 1}
        {'a': 'C', 'c': False, 'b': 0}
        {'a': 'C', 'c': False, 'b': 1}
        {'a': 'C', 'c': None, 'b': 0}
        {'a': 'C', 'c': None, 'b': 1}
    """
    # We don't want the key-->value paring to get mismatched.
    # Convert a dictionary to (key, value) tuples,
    # Then convert to a list of keys and a list of values
    # The index of the key will be the index of the value.
    keys, values = zip(*[
        (key, value)
        for key, value in params.items()
    ])
    # Take the cartesian product of all the sets.
    # This will return an iterator with one item from each set,
    # We take this an pack it back into a dictionary.
    for y in itertools.product(*values):
        out_dict = {}
        for i in range(len(y)):
            out_dict[keys[i]] = y[i]
        yield out_dict
