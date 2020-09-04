import math

HIT_EMPTY = '_'

HIT_O = 'O'
HIT_X = 'X'
VARIANT_IMPOSSIBLE = "Impossible"
VARIANT_O_WINS = "O wins"
VARIANT_X_WINS = "X wins"
VARIANT_DRAW = "Draw"
VARIANT_GAME_NOT_FINISHED = "Game not finished"


def convert_to_matrix(field_in_string: str) -> list:
    matrix = []
    for rowIndex in range(3):
        row = []
        for columnIndex in range(3):
            row.append(field_in_string[rowIndex * 3 + columnIndex])
        matrix.append(row)
    return matrix


def print_field_from_string(field_in_string):
    print('---------')
    for rowIndex in range(3):
        row = []
        for columnIndex in range(3):
            row.append(field_in_string[rowIndex * 3 + columnIndex])
        print(f'| ' + ' '.join(row) + ' |')
    print('---------')


def print_field_from_matrix(field_in_matrix: list):
    print('---------')
    for rowIndex in range(3):
        row = []
        for columnIndex in range(3):
            row.append(field_in_matrix[rowIndex][columnIndex])
        print(f'| ' + ' '.join(row) + ' |')
    print('---------')


def count_hits(matrix: list, hit: str) -> int:
    count = 0
    row: list
    for row in matrix:
        count += row.count(hit)
    return count


def analyze_vector(vector: list) -> str:
    result = VARIANT_IMPOSSIBLE
    has_o = HIT_O in vector
    has_x = HIT_X in vector
    if HIT_EMPTY in vector:
        result = VARIANT_GAME_NOT_FINISHED
    elif has_o and has_x:
        result = VARIANT_DRAW
    elif has_o and not has_x:
        result = VARIANT_O_WINS
    elif not has_o and has_x:
        result = VARIANT_X_WINS
    return result


def analyze_vector_in_matrix(matrix: list, vector_point: list) -> str:
    x_start: int
    y_start: int
    (x_start, y_start) = vector_point[0]
    x_stop: int
    y_stop: int
    (x_stop, y_stop) = vector_point[1]
    vector = []
    x_div = x_stop - x_start
    y_div = y_stop - y_start
    x_step = int(x_div / math.fabs(x_div)) if x_div != 0 else 0
    y_step = int(y_div / math.fabs(y_div)) if y_div != 0 else 0
    for step in range(3):
        x_coord = x_start + step * x_step
        y_coord = y_start + step * y_step
        vector.append(matrix[x_coord][y_coord])
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
        [(0, 0), (0, 2), ],
        [(1, 0), (1, 2), ],
        [(2, 0), (2, 2), ],

        [(0, 0), (2, 0), ],
        [(0, 1), (2, 1), ],
        [(0, 2), (2, 2), ],

        [(0, 0), (2, 2), ],
        [(0, 2), (2, 0), ],
    ]
    variants = []
    for vector in vectors:
        variants.append(analyze_vector_in_matrix(matrix, vector))
    # print(variants)
    return summarize_variants(variants, matrix)


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


def main():
    input_cells = input('Enter cells:')
    tic_tac_toe(input_cells)


def test_generate_simple_map_1():
    return ('TEST CASE 1', 'XXXOO__O_', '''
---------
| X X X |
| O O _ |
| _ O _ |
---------
X wins
''')


def test_generate_simple_map_2():
    return ('TEST CASE 2', 'XOXOXOXXO', '''
---------
| X O X |
| O X O |
| X X O |
---------
X wins
''')


def test_generate_simple_map_3():
    return ('TEST CASE 3', 'XOOOXOXXO', '''
---------
| X O O |
| O X O |
| X X O |
---------
O wins
''')


def test_generate_simple_map_4():
    return ('TEST CASE 4', 'XOXOOXXXO', '''
---------
| X O X |
| O O X |
| X X O |
---------
Draw
''')


def test_generate_simple_map_5():
    return ('TEST CASE 5', 'XO_OOX_X_', '''
---------
| X O   |
| O O X |
|   X   |
---------
Game not finished
''')


def test_generate_simple_map_6():
    return ('TEST CASE 6', 'XO_XO_XOX', '''
---------
| X O _ |
| X O _ |
| X O X |
---------
Impossible
''')


def test_case_runner_generate_simple_map(test_case: tuple):
    test_title: str
    test_string: str
    expected_string: str
    (test_title, test_string, expected_string) = test_case
    print(f'\n\n*************')
    print(f'{test_title}')
    print(f'Enter cells: > {test_string}')
    print('Expected:' + expected_string)
    print('$$$ REAL:')
    tic_tac_toe(test_string)


def main_test():
    # tests for generate_simple_map
    test_case_runner_generate_simple_map(test_generate_simple_map_1())
    test_case_runner_generate_simple_map(test_generate_simple_map_2())
    test_case_runner_generate_simple_map(test_generate_simple_map_3())
    test_case_runner_generate_simple_map(test_generate_simple_map_4())
    test_case_runner_generate_simple_map(test_generate_simple_map_5())
    test_case_runner_generate_simple_map(test_generate_simple_map_6())

    #


main_test()
# main()
