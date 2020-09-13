import unittest

ANY_SYMBOL = 'any_symbol'
MAX_REPETITION = 99999


def count_matching_char_forward(regex_char: str, checked_ind: int, checked: str) -> int:
    count_matching = 0
    for i in range(checked_ind, len(checked)):
        if (regex_char != checked[i]) and (regex_char != ANY_SYMBOL):
            break
        count_matching += 1
    return count_matching


def match_from_start_string(regex: list, checked: str) -> bool:
    match = True
    checked_ind: int = 0
    for reg_group in regex:
        regex_char: str
        count_min: int
        count_max: int
        (regex_char, (count_min, count_max)) = reg_group

        current_count: int = count_matching_char_forward(regex_char, checked_ind, checked)
        if current_count < count_min:
            match = False
            break
        if current_count > count_max:
            current_count = count_max
        checked_ind += current_count
    return match


def match_pure_regex_forward(regex: list, checked: str) -> bool:
    match: bool = match_from_start_string(regex, checked)  # for empty string
    start_ind: int
    for start_ind in range(len(checked)):
        match = match_from_start_string(regex, checked[start_ind:])
        if match is True:
            break
    return match


def match_with_meta_start_and_end_string(regex: list, checked: str) -> bool:
    pure_regex: str = regex
    pure_checked: str = checked
    is_fixed_start: bool = pure_regex.startswith('^')
    is_fixed_end: bool = pure_regex.endswith('$')
    is_equal_match = is_fixed_start or is_fixed_end
    if is_fixed_start and is_fixed_end:
        pure_regex = pure_regex[1:-1]
    elif is_fixed_start:
        pure_regex = pure_regex[1:]
        pure_checked = checked[:len(pure_regex)]
    elif is_fixed_end:
        pure_regex = pure_regex[:-1]
        pure_checked = checked[-len(pure_regex):]
    match = match_from_start_string(pure_regex, pure_checked) if is_equal_match \
        else match_pure_regex(pure_regex, pure_checked)
    return match


def transform_regex(regex: str) -> list:
    obj: list = []
    ind: int = -1
    while True:
        ind += 1
        if (ind + 1) > len(regex):
            break
        letter: str = regex[ind]
        if letter == '.':
            letter = ANY_SYMBOL
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

    def test(self) -> None:
        case: tuple
        for case in self.cases:
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

    cases_quantium = [
        ('colou?r', 'color', True,),
        ('colou?r', 'colour', True,),
        ('colou?r', 'colouur', False,),
        ('colou*r', 'color', True,),
        ('colou*r', 'colour', True,),
        ('colou*r', 'colouur', True,),
        ('col.*r', 'color', True,),
        ('col.*r', 'colour', True,),
        ('col.*r', 'colr', True,),
        ('col.*r', 'collar', True,),
    ]

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

    def run_case(self, cases, fl):
        case: tuple
        for case in cases:
            with self.subTest(case=case):
                regex: str
                test_str: str
                expected: bool
                (regex, test_str, expected,) = case
                actual = fl(regex, test_str)
                # print(f'case: {str(case)}')
                self.assertEqual(expected, actual, f'case: {str(case)}')

    def test_pure_regex(self):
        cases = self.cases_pure_regex + self.cases_pure_regex
        print('+++++++++++++++++++++++++++++++++++')
        self.run_case(cases, lambda regex, checked: match_pure_regex_forward(transform_regex(regex), checked))

    def test_meta_start_and_end_strings(self):
        cases = self.cases_pure_regex + self.cases_pure_regex \
                + self.cases_fixed_start_or_end
        self.run_case(cases, lambda regex, checked: match_with_meta_start_and_end_string(regex, checked))


def main():
    input_str = input()
    (regex, checked_str) = input_str.split('|')
    print(match_with_meta_start_and_end_string(regex, checked_str))


if __name__ == '__main__':
    main()
