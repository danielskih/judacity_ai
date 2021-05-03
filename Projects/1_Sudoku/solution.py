
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units


# TODO: Update the unit list to add the new diagonal units
diagonal_units=[['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1'],['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
unitlist=unitlist+diagonal_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    import copy
    Values=copy.deepcopy(values)
    # FIND TWINS
    # &emsp;**for each** _boxA_ in _values_ **do** 
    for box_a in Values.keys():
        if len(Values[box_a])==2:
            # &emsp;&emsp;**for each** _boxB_ of **PEERS**(_boxA_) **do** 
            for box_b in peers[box_a]:
                # &emsp;&emsp;&emsp;**if** both _values_[_boxA_] and _values_[_boxB_] exactly match and have only two feasible digits **do**  
                if Values[box_a]==Values[box_b]:
                    # &emsp;&emsp;&emsp;&emsp;**for each** _peer_ of **INTERSECTION**(**PEERS**(_boxA_), **PEERS**(_boxB_)) **do**  
                    intersect=set(peers[box_a]).intersection(peers[box_b])
                    for peer in intersect:
                    # &emsp;&emsp;&emsp;&emsp;&emsp;**for each** _digit_ of _values_[_boxA_] **do**
                        for digit in Values[box_a]:
                            Values[peer]=values[peer].replace(digit,'')
    return Values   
    import itertools
    for unit in unitlist:
        # Find all boxes with two digits remaining as possibilities
        pairs = [box for box in unit if len(values[box]) == 2]
 
        # Pairwise combinations
 
        poss_twins = [list(pair) for pair in itertools.combinations(pairs, 2)]
 
        for pair in poss_twins:
 
            box1 = pair[0]
 
            box2 = pair[1]
 
            # Find the naked twins
 
            if values[box1] == values[box2]:
 
                for box in unit:
 
                    # Eliminate the naked twins as possibilities for peers
 
                    if box != box1 and box != box2:
 
                        for digit in values[box1]:
 
                            values[box] = values[box].replace(digit,'')
 
    return values

    # create dict tuple:string.
    tweens=dict()
    import copy
    new_values=copy.deepcopy(values)
    # FIND TWEENS

    # traverse units
    for unit in unitlist:
         #for each box if box value==2 get value:
        for box in unit: 
            if len(new_values[box])==2:
                candidate=new_values[box]
                 #tarverse unit again and check if any peer has same value, if yes: 
                checklist=[peer for peer in unit if new_values[peer]==new_values[box]]
                if len(checklist)>=2:
                    #add both boxes as tuple to the dict. Map them to the value they share
                    tweens[tuple(checklist)]=new_values[box]


    # ELIMINATE TWEENS new_values FROM PEERS

    # traverse dict keys
    for key in tweens:
        dib=key
        # traverse units
        for unit in unitlist:
            #if both tweens are in unit
            if dib[0] and dib[1] in unit:
                # traverse unit
                for peer in unit:
                    #if box not in key:
                    if peer not in dib:
                        # traverse value of the key, remove value from box value in new_values
                        for digit in tweens[dib]:
                            new_values[peer]=(new_values[peer].replace(digit,''))
                            

    return new_values    
    raise NotImplementedError


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
    raise NotImplementedError


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    raise NotImplementedError


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    raise NotImplementedError


def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
        # First, reduce the puzzle using the previous function
 
    values=reduce_puzzle(values)
    if values==False:
        return False
    
    # Choose one of the unfilled squares with the fewest possibilities
    # choose smallest unsolved:    

    not_solved_lst=[box for box in values.keys() if len(values[box])>1]

    # make reverse dictionary that maps from numbers to box IDs:
    unsolved_dict=dict()
    for box in not_solved_lst:
        unsolved_dict[values[box]]=box
    if bool(unsolved_dict)==False:
        return values

    # Choose key with shortest value from reverse dictionary:
    abc=max(unsolved_dict)    
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    sudokus=[]
    for i in range(len(abc)):
        sudokus.append('values'+str(i+1))
    counter=0
    for digit in abc:
        sudokus[counter]=values.copy()
        sudokus[counter][unsolved_dict[abc]]=digit 
        counter+=1
        
    for parent in sudokus:
        child=search(parent)
        if bool(child)==True:
            return child
    raise NotImplementedError


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
