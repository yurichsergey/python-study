# Bank system
import random
import sqlite3
import typing
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
    def __generate_digit_str(count: int) -> str:
        # return ''.join([str(random.randint(0, 9)) for i in range(count)])
        return ('{:0' + str(count) + '}').format(random.randint(0, int('9' * count)))


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

    def to_dict(self) -> dict:
        return {
            'number': self.__card_number,
            'pin': self.__pin_code,
            'balance': self.__balance,
        }


class BankCardStorageInterface:

    def create_card(self) -> typing.Optional[Card]:
        pass

    def find_by_card_and_pin(self, card_number: str, pin: str) -> Card:
        pass

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass


class BankCardMemoryStorage(BankCardStorageInterface):

    def __init__(self):
        self.__storage: typing.Dict[Card] = {}
        self.__generator = CardGenerator()

    def create_card(self) -> typing.Optional[Card]:
        card_number = self.__generate_unique_card_number()
        pin = self.__generator.generate_pin()
        card = Card(card_number, pin)
        self.__storage[card.get_card_number()] = card
        return card

    def find_by_card_and_pin(self, card_number: str, pin: str) -> typing.Optional[Card]:
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


class BankCardDbStorage(BankCardStorageInterface):

    def __init__(self):
        self.__generator = CardGenerator()
        self.__conn: typing.Optional[sqlite3.Connection] = None

    def open(self) -> None:
        self.__conn: typing.Optional[sqlite3.Connection] = sqlite3.connect('card.s3db')  # @todo move to the factory
        self.__create_table()  # @todo move to init method

    def close(self) -> None:
        self.__conn.close()

    def create_card(self) -> typing.Optional[Card]:
        card_number = self.__generate_unique_card_number()
        pin = self.__generator.generate_pin()
        card = Card(card_number, pin)
        # @todo change to insert ignore and update
        self.__execute(
            f'INSERT INTO card (number, pin) VALUES (?, ?)',
            (card.get_card_number(), card.get_pin_code(),)
        )
        return card

    def find_by_card_and_pin(self, card_number: str, pin: str) -> typing.Optional[Card]:
        fetched = self.__fetchone(
            f'SELECT number, pin FROM card WHERE number=? AND pin=?',
            (card_number, pin,)
        )
        card = None
        if fetched:
            print(fetched)
            print(type(fetched))
            number, pin = fetched
            card = Card(number, pin)
        return card

    def fetch_all(self):
        fetchall = self.__fetchall(f'SELECT * FROM card')
        return fetchall

    def fetch_all_numbers(self) -> frozenset:
        fetched = self.__fetchall(f'SELECT number FROM card')
        return frozenset(n[0] for n in fetched)

    def __generate_unique_card_number(self) -> str:
        card_number = None
        all_numbers = self.fetch_all_numbers()
        for i in range(100):
            card_number = self.__generator.generate_card_number()
            if card_number not in all_numbers:
                break
            else:
                card_number = None
        if card_number is None:
            raise RuntimeError('cannot generate unique card number')
        return card_number

    def __create_table(self) -> None:
        # PRIMARY KEY AUTOINCREMENT,
        query = '''
        CREATE TABLE IF NOT EXISTS card (
            id INTEGER,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        )
        '''
        self.__execute(query)

    def __fetchone(self, query, values) -> tuple:
        cur = self.__conn.cursor()
        cur.execute(query, values)
        fetched = cur.fetchone()
        cur.close()
        return fetched

    def __fetchall(self, query) -> list:
        cur = self.__conn.cursor()
        cur.execute(query)
        fetched = cur.fetchall()
        cur.close()
        return fetched

    def __execute(self, query, values=tuple()) -> None:
        cur = self.__conn.cursor()
        cur.execute(query, values)
        self.__conn.commit()
        cur.close()


class Bank:

    def __init__(self, storage: BankCardStorageInterface):
        self.__storage = storage
        self.__generator = CardGenerator()

    def create_card(self) -> Card:
        return self.__storage.create_card()

    def find_by_card_and_pin(self, card_number: str, pin: str) -> Card:
        return self.__storage.find_by_card_and_pin(card_number, pin)


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
    storage = BankCardDbStorage()
    storage.open()
    action = Action(Bank(storage))
    while True:
        user_choice = int(input(greeting))
        if user_choice == 1:  # 1. Create an account
            action.create_card()
        elif user_choice == 2:  # 2. Log into account
            card_number = input('Enter your card number:')
            pin = input('Enter your PIN:')
            action.show_info(card_number, pin)
        elif user_choice == 0:  # 0. Exit
            storage.close()
            print('Bye!')
            break
        else:
            continue


class TestLunchAlgorithm(unittest.TestCase):

    def test_checksum(self):
        self.assertEqual(7, LuhnAlgorithm.generate_check_sum('400000342979508'))
        self.assertEqual(3, LuhnAlgorithm.generate_check_sum('400000844943340'))
        self.assertEqual(6, LuhnAlgorithm.generate_check_sum('400000493832089'))


def manual_test_db():
    s = BankCardDbStorage()
    s.open()
    card = s.create_card()
    print(s.fetch_all())
    fetched_card = s.find_by_card_and_pin(card.get_card_number(), card.get_pin_code())
    print(fetched_card)
    print(fetched_card.to_dict())
    print(s.fetch_all_numbers())


if __name__ == '__main__':
    main()
    # manual_test_db()
