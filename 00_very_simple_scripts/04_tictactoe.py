import math

HIT_EMPTY_UNDERSCORE: str = '_'
HIT_EMPTY: str = ' '
HIT_O: str = 'O'
HIT_X: str = 'X'
VARIANT_IMPOSSIBLE: str = "Impossible"
VARIANT_O_WINS: str = "O wins"
VARIANT_X_WINS: str = "X wins"
VARIANT_DRAW: str = "Draw"
VARIANT_GAME_NOT_FINISHED: str = "Game not finished"


def convert_to_matrix(map_str: str) -> list:
    return [[map_str[row_ind * 3 + column_ind] for column_ind in range(3)] for row_ind in range(3)]


def str_to_str_map(map_str: str) -> str:
    rows = [' '.join(['|'] + [process_cell(map_str[row * 3 + column]) for column in range(3)] + ['|']) for row in
            range(3)]
    return '\n'.join([get_horizontal_line()] + rows + [get_horizontal_line()])


def matrix_to_str_map(map_matrix: list) -> str:
    rows = [' '.join(['|'] + [process_cell(map_matrix[row][column]) for column in range(3)] + ['|']) for row in
            range(3)]
    return '\n'.join([get_horizontal_line()] + rows + [get_horizontal_line()])


def get_horizontal_line() -> str:
    return '-' * 9


def process_cell(cell_val: str) -> str:
    return ' ' if cell_val == HIT_EMPTY_UNDERSCORE else cell_val


def count_hits(matrix: list, hit: str) -> int:
    row: list
    return sum([row.count(hit) for row in matrix])


def analyze_vector(vector: list) -> str:
    has_o = HIT_O in vector
    has_x = HIT_X in vector
    return VARIANT_GAME_NOT_FINISHED if HIT_EMPTY_UNDERSCORE in vector \
        else VARIANT_DRAW if has_o and has_x \
        else VARIANT_O_WINS if has_o and not has_x \
        else VARIANT_X_WINS if not has_o and has_x \
        else VARIANT_IMPOSSIBLE


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
    # when the field has three Xs in a row as well as three Os in a row.
    count_o_wins = variants.count(VARIANT_O_WINS)
    count_x_wins = variants.count(VARIANT_X_WINS)
    # Comment about third impossible variant: the field has a lot more Xs that Os or vice versa
    # (if the difference is 2 or more, should be 1 or 0)
    return VARIANT_IMPOSSIBLE if count_o_wins > 0 and count_x_wins > 0 \
        else VARIANT_IMPOSSIBLE if count_o_wins > 1 or count_x_wins > 1 \
        else VARIANT_IMPOSSIBLE if math.fabs(count_hits(matrix, HIT_X) - count_hits(matrix, HIT_O)) > 1 \
        else VARIANT_O_WINS if count_o_wins \
        else VARIANT_X_WINS if count_x_wins \
        else VARIANT_GAME_NOT_FINISHED if VARIANT_GAME_NOT_FINISHED in variants \
        else VARIANT_DRAW


def analyze_map(matrix: list):
    vectors = [
        [(0, 0), (0, 2), ], [(1, 0), (1, 2), ], [(2, 0), (2, 2), ],  # horizontal
        [(0, 0), (2, 0), ], [(0, 1), (2, 1), ], [(0, 2), (2, 2), ],  # vertical
        [(0, 0), (2, 2), ], [(0, 2), (2, 0), ],  # diagonals
    ]
    return summarize_variants([analyze_vector_in_matrix(matrix, vector) for vector in vectors], matrix)


def parse_input_coord(input_str: str) -> list:
    return [int(n) if n.isnumeric() else None for n in input_str.split(' ')]


def is_only_numbers(list_numbers: list) -> bool:
    only_numbers = True
    n: str
    for n in list_numbers:
        if type(n) is not int:
            only_numbers = False
            break
    return only_numbers


def is_occupied_cell(matrix: list, coord: list) -> bool:
    val = matrix[coord[0]][coord[1]]
    return val != HIT_EMPTY and val != HIT_EMPTY_UNDERSCORE


def is_valid_range_input_coord(coord: list) -> bool:
    is_valid_range = True
    n: int
    for n in coord:
        if n < 1 or 3 < n:
            is_valid_range = False
            break
    return is_valid_range


def convert_input_coord_to_inner(input_coord: list) -> list:
    row_input: int = input_coord[1]
    column_input: int = input_coord[0]

    row_inner: int = - row_input + 3
    column_inner: int = column_input - 1

    inner_coord = [row_inner, column_inner]
    return inner_coord


def validate_input_coord(input_coord: list, matrix: list) -> bool:
    # only two coordinates
    error = "You should enter numbers!" if len(input_coord) != 2 \
        else "You should enter numbers!" if not is_only_numbers(input_coord) \
        else "Coordinates should be from 1 to 3!" if not is_valid_range_input_coord(input_coord) \
        else "This cell is occupied! Choose another one!" \
        if is_occupied_cell(matrix, convert_input_coord_to_inner(input_coord)) \
        else ""
    if len(error) > 0:
        print(error)
    return len(error) == 0


def hit_cell_in_matrix(matrix: list, inner_coord: list, val: str) -> list:
    row_inner: int = inner_coord[0]
    column_inner: int = inner_coord[1]
    matrix[row_inner][column_inner] = val
    return matrix


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


def test_case_full_game():
    input_strs = [
        '2 2',
        '2 2',
        'two two',
        '1 4',
        '1 3',
        '3 1',
        '1 2',
        '1 1',
        '3 2',
        '2 1',
    ]
    return ('TEST CASE FULL GAME 1', input_strs, f'''
---------
|       |
|       |
|       |
---------
Enter the coordinates: > {input_strs[0]}
---------
|       |
|   X   |
|       |
---------
Enter the coordinates: > {input_strs[1]}
This cell is occupied! Choose another one!
Enter the coordinates: > {input_strs[2]}
You should enter numbers!
Enter the coordinates: > {input_strs[3]}
Coordinates should be from 1 to 3!
Enter the coordinates: > {input_strs[4]}
---------
| O     |
|   X   |
|       |
---------
Enter the coordinates: > {input_strs[5]}
---------
| O     |
|   X   |
|     X |
---------
Enter the coordinates: > {input_strs[6]}
---------
| O     |
| O X   |
|     X |
---------
Enter the coordinates: > {input_strs[7]}
---------
| O     |
| O X   |
| X   X |
---------
Enter the coordinates: > {input_strs[8]}
---------
| O     |
| O X O |
| X   X |
---------
Enter the coordinates: > {input_strs[9]}
---------
| O     |
| O X O |
| X X X |
---------
X wins    
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
    matrix = convert_to_matrix(test_string)
    print(matrix_to_str_map(matrix))
    print(analyze_map(matrix))


def test_runner_first_move(test_case: tuple):
    test_title: str
    init_map_str: str
    try_coords: list
    expected_string: str
    (test_title, init_map_str, try_coords, expected_string) = test_case
    print(f'\n\n\n')
    print(f'|||||||||||||||||||||||||||||||')
    print(f'*******************************')
    print(f'{test_title}')
    print('$$$ Expected: $$$\n' + expected_string)
    print('$$$ REAL:')
    print(f'Enter cells: {init_map_str}')
    # print(str_to_str_map(init_map_str))
    matrix = convert_to_matrix(init_map_str)
    print(matrix_to_str_map(matrix))
    print(analyze_map(matrix))

    parse_coord = []
    try_count = 0
    while True:
        try_count += 1
        try_index = try_count - 1
        if try_index >= len(try_coords):
            print(f'We reached end try counts. try_counts = {try_count}')
            break
        try_coord = try_coords[try_index]
        print(f'Enter the coordinates: {try_coord}')
        parse_coord = parse_input_coord(try_coord)
        if validate_input_coord(parse_coord, matrix):
            break

    if len(parse_coord) > 0:
        hit_cell_in_matrix(matrix, convert_input_coord_to_inner(parse_coord), HIT_X)
        print(matrix_to_str_map(matrix))


def test_runner_full_game(test_case: tuple):
    test_title: str
    try_coords: list
    expected_string: str
    (test_title, try_coords, expected_string) = test_case
    print(f'\n\n\n')
    print(f'|||||||||||||||||||||||||||||||')
    print(f'*******************************')
    print(f'{test_title}')
    print('$$$ Expected: $$$\n' + expected_string)
    print('$$$ REAL:')
    init_map_str = '_' * 9
    matrix = convert_to_matrix(init_map_str)
    print(matrix_to_str_map(matrix))
    # print(analyze_field(matrix))

    parse_coord = []
    try_count = 0
    hit_val = None
    while True:
        hit_val = HIT_X if hit_val == HIT_O or hit_val is None else HIT_O

        while True:
            try_count += 1
            try_index = try_count - 1
            if try_index >= len(try_coords):
                print(f'We reached end try counts. try_counts = {try_count}')
                break
            try_coord = try_coords[try_index]
            print(f'Enter the coordinates: {try_coord}')
            parse_coord = parse_input_coord(try_coord)
            if validate_input_coord(parse_coord, matrix):
                break

        if len(parse_coord) == 0:
            break

        hit_cell_in_matrix(matrix, convert_input_coord_to_inner(parse_coord), hit_val)
        print(matrix_to_str_map(matrix))
        result = analyze_map(matrix)
        if result in [VARIANT_X_WINS, VARIANT_O_WINS, VARIANT_DRAW, VARIANT_IMPOSSIBLE]:
            print(result)
            break


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

    test_runner_full_game(test_case_full_game())


def main():
    init_map_str = '_' * 9
    matrix = convert_to_matrix(init_map_str)
    print(matrix_to_str_map(matrix))

    hit_val = None
    while True:
        hit_val = HIT_X if hit_val == HIT_O or hit_val is None else HIT_O

        while True:
            input_coord = input('Enter the coordinates:')
            parse_coord = parse_input_coord(input_coord)
            if validate_input_coord(parse_coord, matrix):
                break

        hit_cell_in_matrix(matrix, convert_input_coord_to_inner(parse_coord), hit_val)
        print(matrix_to_str_map(matrix))
        result = analyze_map(matrix)
        if result in [VARIANT_X_WINS, VARIANT_O_WINS, VARIANT_DRAW, VARIANT_IMPOSSIBLE]:
            print(result)
            break


# main_test()
main()
