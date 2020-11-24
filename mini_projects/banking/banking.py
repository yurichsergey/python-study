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

    @staticmethod
    def check_is_correct_number(number_str: str) -> bool:
        is_correct = False
        if number_str:
            is_correct = int(number_str[-1]) == LuhnAlgorithm.generate_check_sum(number_str[:-1])
        return is_correct


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

    def __init__(self, card_number: str, pin_code: str, balance: int):
        self.__card_number: str = card_number
        self.__pin_code: str = pin_code
        self.__balance: int = balance

    def set_pin(self, pin: str) -> None:
        self.__pin_code = pin

    def get_card_number(self) -> str:
        return self.__card_number

    def get_pin_code(self) -> str:
        return self.__pin_code

    def is_correct_pin(self, pin: str) -> bool:
        return self.__pin_code == pin

    def get_balance(self) -> int:
        return self.__balance

    def change_balance(self, increment: int) -> None:
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

    def find_by_card_number(self, card_number: str) -> typing.Optional[Card]:
        pass

    def find_by_card_and_pin(self, card_number: str, pin: str) -> typing.Optional[Card]:
        pass

    def close_account(self, card: Card) -> None:
        pass

    def open(self) -> None:
        pass

    def close(self) -> None:
        pass


class BankCardMemoryStorage(BankCardStorageInterface):

    def __init__(self):
        self.__storage: typing.Dict[str, Card] = {}
        self.__generator = CardGenerator()

    def create_card(self) -> typing.Optional[Card]:
        card_number = self.__generate_unique_card_number()
        pin = self.__generator.generate_pin()
        card = Card(card_number, pin, 0)
        self.__storage[card.get_card_number()] = card
        return card

    def find_by_card_number(self, card_number: str) -> typing.Optional[Card]:
        return self.__storage.get(card_number)

    def find_by_card_and_pin(self, card_number: str, pin: str) -> typing.Optional[Card]:
        card: Card = self.__storage.get(card_number)
        return card if isinstance(card, Card) and card.is_correct_pin(pin) else None

    def close_account(self, card: Card) -> None:
        self.__storage.pop(card.get_card_number())

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
        card = Card(card_number, pin, 0)
        # @todo change to insert ignore and update
        self.__execute(
            'INSERT INTO card (number, pin, balance) VALUES (?, ?, ?)',
            (card.get_card_number(), card.get_pin_code(), 0)
        )
        return card

    def find_by_card_number(self, card_number: str) -> typing.Optional[Card]:
        fetched = self.__fetchone(
            'SELECT number, pin, balance FROM card WHERE number=?',
            (card_number,)
        )
        return self.__map_fetched_data(fetched)

    def find_by_card_and_pin(self, card_number: str, pin: str) -> typing.Optional[Card]:
        fetched = self.__fetchone(
            'SELECT number, pin, balance FROM card WHERE number=? AND pin=?',
            (card_number, pin,)
        )
        return self.__map_fetched_data(fetched)

    def close_account(self, card: Card) -> None:
        self.__execute(
            'DELETE FROM card WHERE number=?',
            (card.get_card_number(),)
        )

    def fetch_all(self) -> list:
        fetchall = self.__fetchall('SELECT * FROM card')
        return fetchall

    def fetch_all_numbers(self) -> frozenset:
        fetched = self.__fetchall('SELECT number FROM card')
        return frozenset(n[0] for n in fetched)

    @staticmethod
    def __map_fetched_data(fetched: typing.Optional[tuple]) -> typing.Optional[Card]:
        card = None
        if fetched:
            number, pin, balance = fetched
            card = Card(number, pin, balance)
        return card

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
        query = '''
        CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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

    def open(self):
        self.__storage.open()

    def close(self):
        self.__storage.close()

    def create_card(self) -> Card:
        return self.__storage.create_card()

    def find_by_card_number(self, card_number: str) -> Card:
        return self.__storage.find_by_card_number(card_number)

    def find_by_card_and_pin(self, card_number: str, pin: str) -> Card:
        return self.__storage.find_by_card_and_pin(card_number, pin)

    def close_account(self, card: Card) -> None:
        return self.__storage.close_account(card)


class Menu:

    @staticmethod
    def process(menu: dict) -> None:
        greeting = '\n'.join(f'{k}: ' + menu[k][0] for k in menu.keys()) + '\n'
        while True:
            user_choice = int(input(greeting))
            if user_choice in menu:
                try:
                    menu[user_choice][1]()
                except GeneratorExit:
                    break


class ActionPersonalCabinet:

    def __init__(self, card: Card, bank: Bank):
        self.__bank: Bank = bank
        self.__card: typing.Optional[Card] = card

    def print_balance(self) -> None:
        print(f'Balance: {self.__card.get_balance()}')

    def log_out(self) -> None:
        self.__card = None
        print('You have successfully logged out!')
        raise GeneratorExit

    def add_income(self) -> None:
        value = int(input('Enter income:'))
        self.__card.change_balance(value)
        print('Income was added!')

    def do_transfer(self) -> None:
        '''
        Do transfer item allows transferring money to another account. We handle the following errors:

        If the user tries to transfer more money than he/she has, output: "Not enough money!"
        If the user tries to transfer money to the same account, output the following message: “You can't transfer money to the same account!”
        If the receiver's card number doesn’t pass the Luhn algorithm, you should output: “Probably you made a mistake in the card number. Please try again!”
        If the receiver's card number doesn’t exist, you should output: “Such a card does not exist.”
        If there is no error, ask the user how much money they want to transfer and make the transaction.

        :return:
        '''
        print('Transfer')
        card_number = input('Enter card number:')

    def close_account(self) -> None:
        self.__bank.close_account(self.__card)
        self.__card = None
        print('The account has been closed!')
        raise GeneratorExit


class Action:

    def __init__(self, bank: Bank):
        bank.open()
        self.__bank = bank

    def create_card(self):
        card = self.__bank.create_card()
        print(f'Your card has been created')
        print(f'Your card number:\n{card.get_card_number()}')
        print(f'Your card PIN:\n{card.get_pin_code()}')

    def show_info(self):
        card_number = input('Enter your card number:')
        pin = input('Enter your PIN:')

        card = self.__bank.find_by_card_and_pin(card_number, pin)
        if card is None:
            print('Wrong card number or PIN!')
        else:
            print('You have successfully logged in!')
            sub_actions = ActionPersonalCabinet(card, self.__bank)
            sub_menu = {
                1: ('Balance', sub_actions.print_balance,),
                2: ('Add income', sub_actions.add_income,),
                3: ('Do transfer',),
                4: ('Close account', sub_actions.close_account,),
                5: ('Log out', sub_actions.log_out,),
                0: ('Exit', self.close_bank,),
            }
            Menu.process(sub_menu)

    def close_bank(self):
        self.__bank.close()
        print('Bye!')
        exit()


def main():
    bank = Bank(BankCardDbStorage())
    action = Action(bank)

    main_menu = {
        1: ('Create an account', action.create_card,),
        2: ('Log into account', action.show_info,),
        0: ('Exit', action.close_bank,),
    }
    Menu.process(main_menu)


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
