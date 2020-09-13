import unittest

ANY_SYMBOL = 'any_symbol'
MAX_REPETITION = 99999


def match_char(regex_char: str, checked_char: str) -> bool:
    return (regex_char == checked_char) or \
           (regex_char == '.') or \
           (regex_char == '')


def match_equal_strings(regex: str, checked: str) -> bool:
    if len(regex) != len(checked):
        return False
    match = True
    ind: int
    for ind in range(len(regex)):
        regex_char: str = regex[ind]
        checked_char: str = checked[ind] if len(checked) > ind else ''
        match = match_char(regex_char, checked_char)
        if match is False:
            break
    return match


def match_substr(regex: str, checked: str, diff_length: int) -> bool:
    match: bool = True
    start_ind: int
    for start_ind in range(diff_length + 1):
        end_ind: int = len(checked) - diff_length + start_ind
        # print(f'{str(regex)} || {str(checked[start_ind:end_ind])}')
        match = match_equal_strings(regex, checked[start_ind:end_ind])
        if match is True:
            break
    return match


def match_different_strings(regex: str, checked: str) -> bool:
    diff_length: int = len(checked) - len(regex)
    if diff_length < 0:
        return False
    return match_substr(regex, checked, diff_length)


def match_with_meta_start_and_end_string(regex: str, checked: str) -> bool:
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
    match = match_equal_strings(pure_regex, pure_checked) if is_equal_match \
        else match_different_strings(pure_regex, pure_checked)
    return match


def transform_regex(regex: str) -> list:
    obj: list = []
    ind: int = -1
    while True:
        ind += 1
        # print('+++++++++++')
        # print(regex)
        # print(ind)
        # print((ind + 1) >= len(regex))
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
                print(f'case: {str(case)} || actual: {str(actual)}')
                self.assertEqual(expected, actual, f'case: {str(case)}')


class TestMatchingRegex(unittest.TestCase):
    cases_one_character = [
        ('a', 'a', True,),
        ('.', 'a', True,),
        ('', 'a', True,),
        ('', '', True,),
        ('a', '', False,),
        ('a', 'b', False,),
    ]

    cases_equal_length = [
        ('apple', 'apple', True,),
        ('.pple', 'apple', True,),
        ('appl.', 'apple', True,),
        ('.....', 'apple', True,),
        ('peach', 'apple', False,),
    ]

    cases_different_length = [
        ('apple', 'apple', True,),
        ('ap', 'apple', True,),
        ('le', 'apple', True,),
        ('a', 'apple', True,),
        ('.', 'apple', True,),
        ('apwle', 'apple', False,),
        ('peach', 'apple', False,),
        ('apple_', 'apple', False,),
    ]

    cases_start_and_end_strings = [
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
    ]

    cases_controlling_repetition = [
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
                print(f'case: {str(case)}')
                self.assertEqual(expected, actual, f'case: {str(case)}')

    def test_one_character_cases(self):
        cases = self.cases_one_character
        self.run_case(cases, lambda regex, checked: match_char(regex, checked))

    def test_equal_length(self):
        cases = self.cases_equal_length
        self.run_case(cases, lambda regex, checked: match_equal_strings(regex, checked))

    def test_different_length(self):
        cases = self.cases_one_character + self.cases_equal_length + self.cases_different_length
        self.run_case(cases, lambda regex, checked: match_different_strings(regex, checked))

    def test_meta_start_and_end_strings(self):
        cases = self.cases_one_character + self.cases_equal_length + self.cases_different_length \
                + self.cases_start_and_end_strings
        self.run_case(cases, lambda regex, checked: match_with_meta_start_and_end_string(regex, checked))


def main():
    input_str = input()
    (regex, checked_str) = input_str.split('|')
    print(match_with_meta_start_and_end_string(regex, checked_str))


if __name__ == '__main__':
    main()