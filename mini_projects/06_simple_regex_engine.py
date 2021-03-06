import unittest

ANY_SYMBOL = 'any_symbol'
START_STRING = 'start_string'
END_STRING = 'end_string'
MAX_REPETITION = 99999


def count_matching_char(regex_char: str, checked: str, start_ind: int, stop_ind: int) -> int:
    count_matching = 0
    for i in range(start_ind, stop_ind + 1):
        if (regex_char != checked[i]) and (regex_char != ANY_SYMBOL):
            break
        count_matching += 1
    return count_matching


def match_from_start(regex: list, checked: str) -> str:
    match = True
    init_index = 0
    checked_ind: int = init_index
    for reg_ind in range(len(regex)):
        reg_group: tuple = regex[reg_ind]
        regex_char: str
        count_min: int
        count_max: int
        (regex_char, (count_min, count_max)) = reg_group

        stop_ind = len(checked) - 1
        if regex_char == ANY_SYMBOL and len(regex) > (reg_ind + 1):
            next_regex_symbol = regex[reg_ind + 1][0]  # @todo if duplicate ANY_SYMBOL (*)
            found_ind = checked.find(next_regex_symbol, checked_ind)
            if found_ind > -1 and found_ind - checked_ind >= count_min:
                stop_ind = found_ind - 1

        current_count: int = count_matching_char(regex_char, checked, checked_ind, stop_ind)

        if current_count < count_min:
            match = False
            break
        if current_count > count_max:
            current_count = count_max
        checked_ind = checked_ind + current_count
    return checked[init_index:checked_ind] if match else None


def match_pure_regex(regex: list, checked: str) -> str:
    match: str = match_from_start(regex, checked)  # for empty string
    start_ind: int
    for start_ind in range(0, len(checked)):
        match = match_from_start(regex, checked[start_ind:])
        if match is not None:
            break
    return match


def regex_engine(regex: str, checked: str) -> str:
    pure_regex: list = transform_regex(regex)

    is_fixed_start: bool = pure_regex[0] == (START_STRING,) if len(pure_regex) > 0 else False
    is_fixed_end: bool = pure_regex[-1] == (END_STRING,) if len(pure_regex) > 0 else False

    if is_fixed_start and is_fixed_end:
        pure_regex = pure_regex[1:-1]

        matched = match_from_start(pure_regex, checked)
        # reverse strings and regex
        matched_reverse = match_from_start(pure_regex[::-1], checked[::-1])
        # check by length matched strings
        is_equality_mathed = matched is not None and matched_reverse is not None and len(matched) == len(
            matched_reverse)
        match = matched if is_equality_mathed else None
    elif is_fixed_start:
        pure_regex = pure_regex[1:]
        match = match_from_start(pure_regex, checked)
    elif is_fixed_end:
        pure_regex = pure_regex[:-1]
        matched = match_from_start(pure_regex[::-1], checked[::-1])
        match = matched[::-1] if matched is not None else None
    else:
        match = match_pure_regex(pure_regex, checked)
    return match


def transform_regex(regex: str) -> list:
    obj: list = []
    ind: int = -1
    if len(regex) > 0 and regex[0] == '^':
        obj.append((START_STRING,))
        ind += 1
    enable_escaping: bool = False
    while True:
        ind += 1
        if (ind + 1) > len(regex):
            break
        letter: str = regex[ind]

        # Check fix ending string
        if not enable_escaping and (ind + 1) == len(regex) and letter == '$':
            obj.append((END_STRING,))
            continue

        if not enable_escaping and letter == '\\':
            enable_escaping = True
            continue
        if not enable_escaping and letter == '.':
            letter = ANY_SYMBOL

        if enable_escaping:
            enable_escaping = False

        quantum_letter: str = regex[ind + 1] if (ind + 1) < len(regex) else ''
        if quantum_letter not in ['?', '+', '*', ]:
            quantum_letter = ''
        if quantum_letter:
            ind += 1

        quantum = (0, 1,) if quantum_letter == '?' \
            else (1, MAX_REPETITION) if quantum_letter == '+' \
            else (0, MAX_REPETITION) if quantum_letter == '*' \
            else (1, 1,)
        obj.append((letter, quantum,))
    return obj


class TestTransformRegex(unittest.TestCase):
    cases = [
        ('', [],),
        ('a', [('a', (1, 1,),), ],),
        ('.', [(ANY_SYMBOL, (1, 1,),), ],),
        ('cat', [('c', (1, 1,),), ('a', (1, 1,),), ('t', (1, 1,),), ],),
        ('.at_', [(ANY_SYMBOL, (1, 1,),), ('a', (1, 1,),), ('t', (1, 1,),), ('_', (1, 1,),), ],),
        ('.p.', [(ANY_SYMBOL, (1, 1,),), ('p', (1, 1,),), (ANY_SYMBOL, (1, 1,),), ],),
        ('lou?r', [('l', (1, 1,),), ('o', (1, 1,),), ('u', (0, 1,),), ('r', (1, 1,),), ],),
        ('u?r', [('u', (0, 1,),), ('r', (1, 1,),), ],),
        ('lou?', [('l', (1, 1,),), ('o', (1, 1,),), ('u', (0, 1,),), ],),
        ('lou*r', [('l', (1, 1,),), ('o', (1, 1,),), ('u', (0, MAX_REPETITION,),), ('r', (1, 1,),), ],),
        ('lou+r', [('l', (1, 1,),), ('o', (1, 1,),), ('u', (1, MAX_REPETITION,),), ('r', (1, 1,),), ],),
        ('l.*r', [('l', (1, 1,),), (ANY_SYMBOL, (0, MAX_REPETITION,),), ('r', (1, 1,),), ],),
    ]

    cases_escaping = [
        ('^\\.$', [(START_STRING,), ('.', (1, 1,)), (END_STRING,), ],),
        ('\\.$', [('.', (1, 1,)), (END_STRING,), ],),
        ('3\\+3', [('3', (1, 1,)), ('+', (1, 1,)), ('3', (1, 1,)), ],),
        ('\\?', [('?', (1, 1,)), ],),
        ('\\\\', [('\\', (1, 1,)), ],),
        ('lou\\?r', [('l', (1, 1,),), ('o', (1, 1,),), ('u', (1, 1,),), ('?', (1, 1,),), ('r', (1, 1,),), ]),
    ]

    def test(self) -> None:
        case: tuple
        cases = self.cases + self.cases_escaping
        for case in cases:
            with self.subTest(case=case):
                regex: str
                expected: bool
                (regex, expected,) = case
                actual = transform_regex(regex)
                # print(f'case: {str(case)} || actual: {str(actual)}')
                self.assertEqual(expected, actual, f'case: {str(case)}')


class TestMatchingRegex(unittest.TestCase):
    cases_pure_regex = [
        ('a', 'a', True,),
        ('.', 'a', True,),
        ('', 'a', True,),
        ('', '', True,),
        ('a', '', False,),
        ('a', 'b', False,),
        ('apple', 'apple', True,),
        ('.pple', 'apple', True,),
        ('appl.', 'apple', True,),
        ('.....', 'apple', True,),
        ('peach', 'apple', False,),
        ('apple', 'apple', True,),
        ('ap', 'apple', True,),
        ('le', 'apple', True,),
        ('a', 'apple', True,),
        ('.', 'apple', True,),
        ('apwle', 'apple', False,),
        ('peach', 'apple', False,),
        ('apple_', 'apple', False,),
    ]

    cases_quantum_only_letters = [
        ('colou?r', 'color', True,),
        ('colou?r', 'colour', True,),
        ('colou?r', 'colouur', False,),
        ('colou*r', 'color', True,),
        ('colou*r', 'colour', True,),
        ('colou*r', 'colouur', True,),
    ]

    cases_quantum_only_meta = [
        ('col.*r', 'color', True,),
        ('col.*r', 'colour', True,),
        ('col.*r', 'colr', True,),
        ('col.*r', 'collar', True,),
    ]

    cases_quantum = cases_quantum_only_letters + cases_quantum_only_meta

    cases_fixed_start_or_end = [
        ('^app', 'apple', True,),
        ('le$', 'apple', True,),
        ('^a', 'apple', True,),
        ('.$', 'apple', True,),
        ('apple$', 'tasty apple', True,),
        ('^apple', 'apple pie', True,),
        ('^apple$', 'apple', True,),
        ('^apple$', 'tasty apple', False,),
        ('^apple$', 'apple pie', False,),
        ('app$', 'apple', False,),
        ('^le', 'apple', False,),
        ('col.*r$', 'colors', False,),
    ]

    cases_escaping = [
        ('\\.$', 'end.', True),
        ('3\\+3', '3+3=6', True),
        ('\\?', 'Is this working?', True),
        ('\\\\', '\\', True),
        ('colou\\?r', 'color', False),
        ('colou\\?r', 'colour', False),
    ]

    def run_case(self, cases, fl):
        case: tuple
        for case in cases:
            with self.subTest(case=case):
                regex: str
                test_str: str
                expected: bool
                (regex, test_str, expected,) = case
                match = fl(regex, test_str)
                actual = match is not None
                # print(f'case: {str(case)}')
                self.assertEqual(expected, actual, f'case: {str(case)}')

    def test_pure_regex(self):
        cases = self.cases_pure_regex + self.cases_quantum
        # cases = self.cases_quantum_only_meta
        self.run_case(
            cases,
            lambda regex, checked: match_pure_regex(transform_regex(regex), checked)
        )

    def test_regex_engine(self):
        cases = self.cases_pure_regex + self.cases_quantum + self.cases_fixed_start_or_end + self.cases_escaping
        self.run_case(cases, lambda regex, checked: regex_engine(regex, checked))


def main():
    input_str = input()
    (regex, checked_str) = input_str.split('|')
    matched = regex_engine(regex, checked_str)
    print(matched is not None)


if __name__ == '__main__':
    main()
