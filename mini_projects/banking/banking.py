# Bank system
import random
import unittest


class LuhnAlgorithm:

    @staticmethod
    def generate_check_sum(numbers_str: str) -> int:
        numbers_int = [int(x) for x in numbers_str]

        sum_digits = sum(
            [n - 9 if n > 9 else n for n in
             [2 * numbers_int[i] if (i + 1) % 2 else numbers_int[i] for i in range(len(numbers_int))]
             ]
        )
        rest_of_divider = sum_digits % 10
        return 10 - rest_of_divider if rest_of_divider else 0


class CardGenerator:

    def generate_pin(self) -> str:
        return self.__generate_digit_str(4)

    def generate_card_number(self) -> str:
        number = '400' + '000' + self.__generate_digit_str(9)
        return number + str(LuhnAlgorithm.generate_check_sum(number))

    @staticmethod
    def __generate_digit_str(count: int):
        return ''.join([str(random.randint(0, 9)) for i in range(count)])


class Card:

    def __init__(self, card_number: str, pin_code: str):
        self.__card_number = card_number
        self.__pin_code = pin_code
        self.__balance: float = 0.

    def set_pin(self, pin: str) -> None:
        self.__pin_code = pin

    def get_card_number(self) -> str:
        return self.__card_number

    def get_pin_code(self) -> str:
        return self.__pin_code

    def is_correct_pin(self, pin: str) -> bool:
        return self.__pin_code == pin

    def get_balance(self) -> float:
        return self.__balance

    def change_balance(self, increment: float) -> None:
        self.__balance += increment


class Bank:

    def __init__(self):
        # Card[]
        self.__storage = {}
        self.__generator = CardGenerator()

    def create_card(self) -> Card:
        card_number = self.__generate_unique_card_number()
        pin = self.__generator.generate_pin()
        card = Card(card_number, pin)
        self.__storage[card.get_card_number()] = card
        return card

    def find_by_card_and_pin(self, card_number: str, pin: str) -> Card:
        card: Card = self.__storage[card_number] if card_number in self.__storage else None
        return card if isinstance(card, Card) and card.is_correct_pin(pin) else None

    def __generate_unique_card_number(self) -> str:
        card_number = None
        for i in range(100):
            card_number = self.__generator.generate_card_number()
            if card_number not in self.__storage:
                break
            else:
                card_number = None
        if card_number is None:
            raise RuntimeError('cannot generate unique card number')
        return card_number


class Action:

    def __init__(self, bank: Bank):
        self.__bank = bank

    def create_card(self):
        card = self.__bank.create_card()
        print(f'Your card has been created')
        print(f'Your card number:\n{card.get_card_number()}')
        print(f'Your card PIN:\n{card.get_pin_code()}')

    def show_info(self, card_number, pin):
        card = self.__bank.find_by_card_and_pin(card_number, pin)
        if card is None:
            print('Wrong card number or PIN!')
        else:
            print('You have successfully logged in!')
            greeting = '\n'.join([
                '1. Balance',
                '2. Log out',
                '0. Exit',
            ])
            while True:
                user_choice = int(input(greeting))
                if user_choice == 1:  # 1. Balance
                    print(f'Balance: {card.get_balance()}')
                elif user_choice == 2:  # 2. Log out
                    print('You have successfully logged out!')
                    break
                elif user_choice == 0:  # 0. Exit
                    print('Bye!')
                    exit()
                else:
                    continue


def main():
    greeting = '\n'.join([
        '1. Create an account',
        '2. Log into account',
        '0. Exit',
    ])
    action = Action(Bank())
    while True:
        user_choice = int(input(greeting))
        if user_choice == 1:  # 1. Create an account
            action.create_card()
        elif user_choice == 2:  # 2. Log into account
            card_number = input('Enter your card number:')
            pin = input('Enter your PIN:')
            action.show_info(card_number, pin)
        elif user_choice == 0:  # 0. Exit
            print('Bye!')
            break
        else:
            continue


class TestLunchAlgorithm(unittest.TestCase):

    def test_checksum(self):
        self.assertEqual(7, LuhnAlgorithm.generate_check_sum('400000342979508'))
        self.assertEqual(3, LuhnAlgorithm.generate_check_sum('400000844943340'))
        self.assertEqual(6, LuhnAlgorithm.generate_check_sum('400000493832089'))


if __name__ == '__main__':
    main()
