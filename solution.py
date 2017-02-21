import itertools


rows = 'ABCDEFGHI'
cols = '123456789'


def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonals_units = [[a[0]+a[1] for a in zip(rows, cols)],        # diagonal 1
                   [a[0]+a[1] for a in zip(rows, cols[::-1])]]  # diagonal 2
unitlist = row_units + column_units + square_units + diagonals_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return dict([(k, v if v != '.' else '123456789') for k, v in zip(boxes, grid)])


def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    for box in [key for key, value in values.items() if len(value) == 1]:
        for n in peers[box]:
            values = assign_value(values, n, values[n].replace(values[box], ''))
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unitlist:
        for digit in '123456789':
            d_places = [box for box in unit if digit in values[box]]
            if len(d_places) == 1:
                values = assign_value(values, d_places[0], digit)
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    for unit in unitlist:
        # Find all the groups with 2 elements in the group key and having > 1 elements in it
        two_elements_only = sorted([values[b] for b in unit if len(values[b]) == 2])
        twins = [k for k, g in itertools.groupby(two_elements_only) if len(list(g)) > 1]
        for t in twins:
            # Remove group key elements from all the elements inside the unit
            for box in [b for b in unit if values[b] != t]:
                for digit in t:
                    assign_value(values, box, values[box].replace(digit, ''))
    return values


def reduce_puzzle(values):
    """Repeatedly eliminates values using the 3 strategies: single value/only choice/naked twins.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the values dictionary with elements eliminated (according to 3 strategies) from peers.
    """
    while True:
        before = values.copy()
        values = naked_twins(only_choice(eliminate(values)))

        # Check if any change occurs in board state
        if len(set(before.items()) ^ set(values.items())) == 0:
            break
    return values


def solved(values):
    """Check if sudoku solved.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the boolean value indicates if sudoku solved or not.
    """
    return all([len(v) == 1 for v in values.values()])


def wrong_way(values):
    """Check if sudoku can't be solved following this way.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        the boolean value indicates if we can continue to solve this board configuration.
    """
    return any([len(v) == 0 for v in values.values()])


def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    values = reduce_puzzle(values)

    # Check if we can continue
    if wrong_way(values):
        return None

    if not solved(values):
        # Find element with minimum possible elements in it
        box, possible_values = next(iter(sorted([(k,v) for k,v in values.items() if len(v) > 1], key=lambda pair: len(pair[1]))))
        for v in possible_values:
            copied = values.copy()
            # Trying every possible value one by one and continue to search solution with a new configuration
            copied = assign_value(copied, box, v)
            solution = search(copied)
            # If solution found return it
            if solution:
                return solution
        # No solution found
        return None
    else:
        return values


def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
