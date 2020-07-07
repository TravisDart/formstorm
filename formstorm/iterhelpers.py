import itertools
import copy


def every_combo(items):
    """
        Given a list of n items, return every combination of length 1 .. n.

        list(every_combo([1, 2, 3]))
        [(1,), (2,), (3,), (1, 2), (1, 3), (2, 3), (1, 2, 3)]
    """
    x = [itertools.combinations(items, i) for i in range(1, len(items) + 1)]
    y = list(itertools.chain(*x))
    return y


def dict_combo(params, base_dict={}):
    """
    params = {
        "a": ["A","B","C"],
        "b": [0, 1],
        "c": [True, False, None],
    }
    for x in dict_combo(params):
        print(x)

    Returns:
        {'a': 'A', 'b': 0, 'c': True}
        {'a': 'A', 'b': 0, 'c': False}
        {'a': 'A', 'b': 0, 'c': None}
        {'a': 'A', 'b': 1, 'c': True}
        {'a': 'A', 'b': 1, 'c': False}
        {'a': 'A', 'b': 1, 'c': None}
        {'a': 'B', 'b': 0, 'c': True}
        {'a': 'B', 'b': 0, 'c': False}
        {'a': 'B', 'b': 0, 'c': None}
        {'a': 'B', 'b': 1, 'c': True}
        {'a': 'B', 'b': 1, 'c': False}
        {'a': 'B', 'b': 1, 'c': None}
        {'a': 'C', 'b': 0, 'c': True}
        {'a': 'C', 'b': 0, 'c': False}
        {'a': 'C', 'b': 0, 'c': None}
        {'a': 'C', 'b': 1, 'c': True}
        {'a': 'C', 'b': 1, 'c': False}
        {'a': 'C', 'b': 1, 'c': None}
    """
    # We don't want the key-->value paring to get mismatched.
    # Convert a dictionary to (key, value) tuples,
    # Then convert to a list of keys and a list of values
    # The index of the key will be the index of the value.
    keys, values = zip(*[(key, value) for key, value in params.items()])
    # Take the cartesian product of all the sets.
    # This will return an iterator with one item from each set,
    # We take this an pack it back into a dictionary.
    for y in itertools.product(*values):
        out_dict = copy.copy(base_dict)
        for i in range(len(y)):
            out_dict[keys[i]] = y[i]
        yield out_dict
