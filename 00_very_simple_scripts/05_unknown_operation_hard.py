"""
The decision for very hard task from hyperskill.
I decided it with test-driven development (TDD).
Without TDD, I or couldn't decide or could decide it very long time.
And of course with understanding of Conversion to boolean in Python.

Run test with command: python -m unittest file.py (or in PyCharm or manually called function)

@link: https://hyperskill.org/learn/step/10335

Anyway many students decided it with only 10 strings - very short program!!!
(not as my...!!!)
But, as said someone (M૯ᄃmb I水I - https://hyperskill.org/learn/step/10335#hint-533829):
> Yeah this was hard and I still have no clue how I've come up with this solution

In contrast with them I can say how to reproduce my decision.
And maybe I know how to reproduce their short decision.
We need to do test cases or the paper (they) or in the PC (I).
And when we write some test cases we can show regularity.

But anyway, I don't understand their pretty-short decision clearly((((
Because for me it is very difficult keep in mind all sides of this task.
And I don't wanted to spend time for this understanding.

Task:

There is a function hidden_operation() which in every test case
performs one of the logical operations: and, or and not.

def hidden_operation(operand):
    if oper == "and":
        return operand and hidden_operand
    elif oper == "or":
        return operand or hidden_operand
    elif oper == "not":
        return not operand

You don't have access to oper and hidden_operand variables, but
you can call the hidden_operation() function any number of times
and pass any objects to it. Your task is to find out which logical
operation this function performs and what the hidden_operand is
equal to (if the function performs the not operation, you don't
have to find the hidden_operand).

Write your code inside the solve() function. In the first line print
the name of the logical operation. If the logical operation is and
or or, print hidden_operand in the second line.

Your program shouldn't read any input or call the function, just implement it.
"""

import unittest

OPERAND_TRULY_TRUE = True
OPERAND_TRULY_5 = 5
OPERAND_TRULY_3 = 3
OPERAND_TRULY_7 = 7
OPERAND_TRULY_STR_1 = 'fd'
OPERAND_TRULY_LIST_1 = [1, 2, 3]

OPERAND_FALTHY_FALSE = False
OPERAND_FALTHY_EMPTY_STR = ''
OPERAND_FALTHY_0_INT = 0
OPERAND_FALTHY_EMPTY_LIST = []

OPERATION_NOT = "not"
OPERATION_OR = "or"
OPERATION_AND = 'and'

DELIMETER = '\n'


def debug_data(fun: callable) -> None:
    truly0 = fun(OPERAND_TRULY_TRUE)
    truly1 = fun(OPERAND_TRULY_3)
    truly2 = fun(OPERAND_TRULY_5)
    truly3 = fun(OPERAND_TRULY_7)
    truly4 = fun(OPERAND_TRULY_STR_1)
    truly5 = fun(OPERAND_TRULY_LIST_1)

    falthy0 = fun(OPERAND_FALTHY_FALSE)
    falthy1 = fun(OPERAND_FALTHY_0_INT)
    falthy2 = fun(OPERAND_FALTHY_EMPTY_LIST)
    falthy3 = fun(OPERAND_FALTHY_EMPTY_STR)

    print([
        (OPERAND_TRULY_TRUE, truly0),
        (OPERAND_TRULY_3, truly1),
        (OPERAND_TRULY_5, truly2),
        (OPERAND_TRULY_7, truly3),
        (OPERAND_TRULY_STR_1, truly4),
        (OPERAND_TRULY_LIST_1, truly5),

        (OPERAND_FALTHY_FALSE, falthy0),
        (OPERAND_FALTHY_0_INT, falthy1),
        (OPERAND_FALTHY_EMPTY_LIST, falthy2),
        (OPERAND_FALTHY_EMPTY_STR, falthy3),
    ])


def define_vars(fun: callable) -> str:
    # debug_data(fun)
    oper = define_operation(fun)

    hidden_operand = None
    if oper == OPERATION_AND:
        hidden_operand = fun(OPERAND_TRULY_TRUE)
    elif oper == OPERATION_OR:
        hidden_operand = fun(OPERAND_FALTHY_FALSE)
    result = oper
    result += (DELIMETER + str(hidden_operand)) if oper != OPERATION_NOT else ''
    return result


def define_operation(fun) -> str:
    truly0 = fun(OPERAND_TRULY_TRUE)
    truly1 = fun(OPERAND_TRULY_3)
    truly2 = fun(OPERAND_TRULY_5)
    truly4 = fun(OPERAND_TRULY_STR_1)
    falthy1 = fun(OPERAND_FALTHY_0_INT)
    falthy2 = fun(OPERAND_FALTHY_EMPTY_LIST)
    if truly1 == truly2 and falthy1 == falthy2 \
            and truly1 is False and falthy1 is True \
            and isinstance(truly1, bool) and isinstance(truly2, bool) \
            and isinstance(falthy1, bool) and isinstance(falthy2, bool):
        return OPERATION_NOT
    elif truly1 == truly2 \
            and truly1 == truly0 \
            and truly0 == truly4 \
            and isinstance(truly1, type(truly2)) \
            and isinstance(truly2, type(truly0)) \
            and isinstance(truly2, type(truly4)):
        return OPERATION_AND
    else:
        return OPERATION_OR


def tester(oper: str, hidden_operand: str):
    def hidden_operation_duplicate(operand):
        if oper == OPERATION_AND:
            return operand and hidden_operand
        elif oper == OPERATION_OR:
            return operand or hidden_operand
        elif oper == OPERATION_NOT:
            return not operand
        return None

    return define_vars(hidden_operation_duplicate)


class TestDefineMethods(unittest.TestCase):

    def test_base_cases(self):
        cases = [
            ('Test case 00', OPERATION_NOT, None,),
            ('Test case 01', OPERATION_AND, OPERAND_TRULY_TRUE,),
            ('Test case 02', OPERATION_AND, OPERAND_TRULY_3,),
            ('Test case 03', OPERATION_AND, OPERAND_TRULY_STR_1,),
            ('Test case 04', OPERATION_AND, OPERAND_FALTHY_FALSE,),
            ('Test case 05', OPERATION_AND, OPERAND_FALTHY_0_INT,),
            ('Test case 06', OPERATION_AND, OPERAND_TRULY_LIST_1,),
            ('Test case or 01', OPERATION_OR, OPERAND_TRULY_TRUE,),
            ('Test case or 02', OPERATION_OR, OPERAND_TRULY_3,),
            ('Test case or 03', OPERATION_OR, OPERAND_TRULY_STR_1,),
            ('Test case or 04', OPERATION_OR, OPERAND_FALTHY_FALSE,),
            ('Test case or 05', OPERATION_OR, OPERAND_FALTHY_0_INT,),
        ]
        for case in cases:
            title: str
            oper: str
            hidden_operand: str
            (title, oper, hidden_operand) = case
            print("\n+++++++++++++++++++++")
            # self.subTest(title)

            # print(f'oper={oper}; hidden_operand={hidden_operand}')
            expected: str = f'{oper}'
            expected += f'{DELIMETER}{hidden_operand}' if oper in [OPERATION_AND, OPERATION_OR, ] else ''
            print(f'{title}. EXPECTED: "{expected}"')

            actual = tester(oper, hidden_operand)
            print(f'ACTUAL: "{actual}"')

            self.assertEqual(expected, actual)


# def solve():
#     print(define_vars(hidden_operation))

# if __name__ == '__main__':
#     unittest.main()
