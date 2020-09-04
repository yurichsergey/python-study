import math

HIT_EMPTY: str = '_'
HIT_O: str = 'O'
HIT_X: str = 'X'
VARIANT_IMPOSSIBLE: str = "Impossible"
VARIANT_O_WINS: str = "O wins"
VARIANT_X_WINS: str = "X wins"
VARIANT_DRAW: str = "Draw"
VARIANT_GAME_NOT_FINISHED: str = "Game not finished"


def convert_to_matrix(map_str: str) -> list:
    return [[map_str[row_ind * 3 + column_ind] for column_ind in range(3)] for row_ind in range(3)]


def print_field_from_string(map_str: str) -> None:
    rows = [' '.join(['|'] + [process_cell(map_str[row * 3 + column]) for column in range(3)] + ['|']) for row in
            range(3)]
    print('\n'.join([get_horizontal_line()] + rows + [get_horizontal_line()]))


def print_field_from_matrix(map_matrix: list) -> None:
    rows = [' '.join(['|'] + [process_cell(map_matrix[row][column]) for column in range(3)] + ['|']) for row in
            range(3)]
    print('\n'.join([get_horizontal_line()] + rows + [get_horizontal_line()]))


def get_horizontal_line() -> str:
    return '-' * 9


def process_cell(cell_val: str) -> str:
    return ' ' if cell_val == HIT_EMPTY else cell_val


def count_hits(matrix: list, hit: str) -> int:
    row: list
    return sum([row.count(hit) for row in matrix])


def analyze_vector(vector: list) -> str:
    has_o = HIT_O in vector
    has_x = HIT_X in vector
    return VARIANT_GAME_NOT_FINISHED if HIT_EMPTY in vector else \
        VARIANT_DRAW if has_o and has_x else \
            VARIANT_O_WINS if has_o and not has_x else \
                VARIANT_X_WINS if not has_o and has_x else \
                    VARIANT_IMPOSSIBLE


def analyze_vector_in_matrix(matrix: list, vector_point: list) -> str:
    x_start: int
    y_start: int
    (x_start, y_start) = vector_point[0]
    x_stop: int
    y_stop: int
    (x_stop, y_stop) = vector_point[1]
    x_div = x_stop - x_start
    y_div = y_stop - y_start
    x_step = int(x_div / math.fabs(x_div)) if x_div != 0 else 0
    y_step = int(y_div / math.fabs(y_div)) if y_div != 0 else 0
    vector = [matrix[x_start + step * x_step][y_start + step * y_step] for step in range(3)]
    # print([vector_point, vector, analyze_vector(vector), ])
    return analyze_vector(vector)


def summarize_variants(variants: list, matrix: list):
    result = VARIANT_DRAW
    # when the field has three Xs in a row as well as three Os in a row.
    count_o_wins = variants.count(VARIANT_O_WINS)
    count_x_wins = variants.count(VARIANT_X_WINS)
    if count_o_wins > 0 and count_x_wins > 0:
        result = VARIANT_IMPOSSIBLE
    elif count_o_wins > 1 or count_x_wins > 1:
        result = VARIANT_IMPOSSIBLE
    # the field has a lot more Xs that Os or vice versa
    # (if the difference is 2 or more, should be 1 or 0)
    elif math.fabs(count_hits(matrix, HIT_X) - count_hits(matrix, HIT_O)) > 1:
        result = VARIANT_IMPOSSIBLE
    elif count_o_wins:
        result = VARIANT_O_WINS
    elif count_x_wins:
        result = VARIANT_X_WINS
    elif VARIANT_GAME_NOT_FINISHED in variants:
        result = VARIANT_GAME_NOT_FINISHED
    return result


def analyze_field(matrix: list):
    vectors = [
        [(0, 0), (0, 2), ], [(1, 0), (1, 2), ], [(2, 0), (2, 2), ],  # horizontal
        [(0, 0), (2, 0), ], [(0, 1), (2, 1), ], [(0, 2), (2, 2), ],  # vertical
        [(0, 0), (2, 2), ], [(0, 2), (2, 0), ],  # diagonals
    ]
    return summarize_variants([analyze_vector_in_matrix(matrix, vector) for vector in vectors], matrix)


def tic_tac_toe_generate_simple_map(input_cells: str):
    # print_field_from_string(input_cells)
    matrix = convert_to_matrix(input_cells)
    print_field_from_matrix(matrix)
    print(analyze_field(matrix))


def tic_tac_toe(input_cells: str):
    # print_field_from_string(input_cells)
    matrix = convert_to_matrix(input_cells)
    print_field_from_matrix(matrix)
    print(analyze_field(matrix))


def test_case_generate_simple_map_1():
    return ('TEST CASE 1', 'XXXOO__O_', '''
---------
| X X X |
| O O _ |
| _ O _ |
---------
X wins
''')


def test_case_generate_simple_map_2():
    return ('TEST CASE 2', 'XOXOXOXXO', '''
---------
| X O X |
| O X O |
| X X O |
---------
X wins
''')


def test_case_generate_simple_map_3():
    return ('TEST CASE 3', 'XOOOXOXXO', '''
---------
| X O O |
| O X O |
| X X O |
---------
O wins
''')


def test_case_generate_simple_map_4():
    return ('TEST CASE 4', 'XOXOOXXXO', '''
---------
| X O X |
| O O X |
| X X O |
---------
Draw
''')


def test_case_generate_simple_map_5():
    return ('TEST CASE 5', 'XO_OOX_X_', '''
---------
| X O   |
| O O X |
|   X   |
---------
Game not finished
''')


def test_case_generate_simple_map_6():
    return ('TEST CASE 6', 'XO_XO_XOX', '''
---------
| X O _ |
| X O _ |
| X O X |
---------
Impossible
''')


def test_runner_generate_simple_map(test_case: tuple):
    test_title: str
    test_string: str
    expected_string: str
    (test_title, test_string, expected_string) = test_case
    print(f'\n\n\n')
    print(f'|||||||||||||||||||||||||||||||')
    print(f'*******************************')
    print(f'{test_title} FOR GENERATE_SIMPLE_MAP')
    print(f'Enter cells: > {test_string}')
    print('Expected:' + expected_string)
    print('$$$ REAL:')
    tic_tac_toe_generate_simple_map(test_string)


def test_case_first_move_1():
    init_map = 'X_X_O____'
    try_coords = ['1 1', ]
    return ('TEST CASE FIRST MOVE 1', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
| X   X |
|   O   |
|       |
---------
Enter the coordinates: > {try_coords[0]}
---------
| X   X |
|   O   |
| X     |
---------
''')


def test_case_first_move_2():
    init_map = '_XXOO_OX_'
    try_coords = ['1 3', ]
    return ('TEST CASE FIRST MOVE 2', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
---------
| X X X |
| O O   |
| O X   |
---------
''')


def test_case_first_move_3():
    init_map = '_XXOO_OX_'
    try_coords = ['3 1', ]
    return ('TEST CASE FIRST MOVE 3', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
---------
|   X X |
| O O   |
| O X X |
---------
''')


def test_case_first_move_4():
    init_map = '_XXOO_OX_'
    try_coords = ['3 2', ]
    return ('TEST CASE FIRST MOVE 4', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
---------
|   X X |
| O O X |
| O X   |
---------
''')


def test_case_first_move_5():
    init_map = '_XXOO_OX_'
    try_coords = ['1 1', '1 3', ]
    return ('TEST CASE FIRST MOVE 5', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
This cell is occupied! Choose another one!
Enter the coordinates: > {try_coords[1]}
---------
| X X X |
| O O   |
| O X   |
---------
''')


def test_case_first_move_6():
    init_map = '_XXOO_OX_'
    try_coords = ['one', 'one three', '1 3', ]
    return ('TEST CASE FIRST MOVE 6', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
You should enter numbers!
Enter the coordinates: > {try_coords[1]}
You should enter numbers!
Enter the coordinates: > {try_coords[2]}
---------
| X X X |
| O O   |
| O X   |
---------
''')


def test_case_first_move_7():
    init_map = '_XXOO_OX_'
    try_coords = ['4 1', '1 4', '1 3', ]
    return ('TEST CASE FIRST MOVE 7', init_map, try_coords, f'''
Enter cells: > {init_map}
---------
|   X X |
| O O   |
| O X   |
---------
Enter the coordinates: > {try_coords[0]}
Coordinates should be from 1 to 3!
Enter the coordinates: > {try_coords[1]}
Coordinates should be from 1 to 3!
Enter the coordinates: > {try_coords[2]}
---------
| X X X |
| O O   |
| O X   |
---------    
''')


def test_runner_first_move(test_case: tuple):
    test_title: str
    init_map_str: str
    try_coords: str
    expected_string: str
    (test_title, init_map_str, try_coords, expected_string) = test_case
    print(f'\n\n\n')
    print(f'|||||||||||||||||||||||||||||||')
    print(f'*******************************')
    print(f'{test_title}')
    print('$$$ Expected: $$$\n' + expected_string)
    print('$$$ REAL:')
    tic_tac_toe_generate_simple_map(init_map_str)


def main_test():
    # tests for generate_simple_map
    test_runner_generate_simple_map(test_case_generate_simple_map_1())
    test_runner_generate_simple_map(test_case_generate_simple_map_2())
    test_runner_generate_simple_map(test_case_generate_simple_map_3())
    test_runner_generate_simple_map(test_case_generate_simple_map_4())
    test_runner_generate_simple_map(test_case_generate_simple_map_5())
    test_runner_generate_simple_map(test_case_generate_simple_map_6())

    # tests for first move
    test_runner_first_move(test_case_first_move_1())
    test_runner_first_move(test_case_first_move_2())
    test_runner_first_move(test_case_first_move_3())
    test_runner_first_move(test_case_first_move_4())
    test_runner_first_move(test_case_first_move_5())
    test_runner_first_move(test_case_first_move_6())
    test_runner_first_move(test_case_first_move_7())


def main():
    input_cells = input('Enter cells:')
    tic_tac_toe(input_cells)


main_test()
# main()
