# import unittest


# print('''
# Starting to make a coffee
# Grinding coffee beans
# Boiling water
# Mixing boiled water with crushed coffee beans
# Pouring coffee into the cup
# Pouring some milk into the cup
# Coffee is ready!
# ''')

class CoffeeTypeRecipe:
    __water: int = 0
    __milk: int = 0
    __beans: int = 0
    __cost: int = 0

    def __init__(self, water: int, milk: int, beans: int, cost: int):
        self.__water = water
        self.__milk = milk
        self.__beans = beans
        self.__cost = cost

    def get_water(self) -> int:
        return self.__water

    def get_milk(self) -> int:
        return self.__milk

    def get_beans(self) -> int:
        return self.__beans

    def get_cost(self) -> int:
        return self.__cost


class CoffeeMachine:
    __water: int = 0
    __milk: int = 0
    __beans: int = 0
    __disposable_cups: int = 0
    __money: int = 0

    def fill_state(self, water: int, milk: int, beans: int, disposable_cups: int, money: int):
        self.__water += water
        self.__milk += milk
        self.__beans += beans
        self.__disposable_cups += disposable_cups
        self.__money += money

    def print_state(self) -> None:
        print(f'The coffee machine has:')
        print(f'{self.__water} of water')
        print(f'{self.__milk} of milk')
        print(f'{self.__beans} of coffee beans')
        print(f'{self.__disposable_cups} of disposable cups')
        print(f'{self.__money} of money')

    def make_coffee(self, recipe: CoffeeTypeRecipe) -> None:
        self.__water -= recipe.get_water()
        self.__milk -= recipe.get_milk()
        self.__beans -= recipe.get_beans()
        self.__disposable_cups -= 1
        self.__money += recipe.get_cost()

    def take_money(self) -> int:
        took_money: int = self.__money if self.__money > 0 else 0
        self.__money -= took_money
        return took_money


def init_machine(machine: CoffeeMachine) -> None:
    machine.fill_state(water=400, milk=540, beans=120, disposable_cups=9, money=550)


class CoffeeTypeFactory:

    def create_espresso(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=250, milk=0, beans=16, cost=4)

    def create_latte(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=350, milk=75, beans=20, cost=7)

    def create_cappuccino(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=200, milk=100, beans=12, cost=6)


#
# water_one_cup: int = 200  # ml of water
# milk_one_cup: int = 50  # ml of milk
# beans_one_cup: int = 15  # g of coffee beans.
#
# water_has: int = int(input(f'Write how many ml of water the coffee machine has:'))
# milk_has: int = int(input(f'Write how many ml of milk the coffee machine has:'))
# beans_have: int = int(input(f'Write how many grams of coffee beans the coffee machine has:'))
# cups_need: int = int(input(f'Write how many cups of coffee you will need:'))
#
# water_needs: int = cups_need * water_one_cup
# milk_needs: int = cups_need * milk_one_cup
# beans_need: int = cups_need * beans_one_cup
#
# # print(f'For {cups_need} cups of coffee you will need:')
# # print(f'{water_needs} ml of water')
# # print(f'{milk_needs} ml of milk')
# # print(f'{beans_need} g of coffee beans')
#
# cups_by_water_allow: int = water_has // water_one_cup
# cups_by_milk_allow: int = milk_has // milk_one_cup
# cups_by_beans_allow: int = beans_have // beans_one_cup
# cups_result_allow: int = min([cups_by_water_allow, cups_by_milk_allow, cups_by_beans_allow, ])
#
# if cups_need <= cups_result_allow:
#     cups_reminder: int = cups_result_allow - cups_need
#     additional_info: str = f' (and even {cups_reminder} more than that)' if cups_reminder > 0 else ''
#     print(f'Yes, I can make that amount of coffee' + additional_info)
# else:
#     print(f'No, I can make only {cups_result_allow} cups of coffee')


def action_buy(machine: CoffeeMachine) -> None:
    type_factory = CoffeeTypeFactory()
    coffee_type_storage = {
        1: type_factory.create_espresso(),
        2: type_factory.create_latte(),
        3: type_factory.create_cappuccino()
    }
    coffee_type_id = int(input('What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino:'))
    coffee_type = coffee_type_storage[coffee_type_id]
    machine.make_coffee(coffee_type)


def action_fill(machine: CoffeeMachine) -> None:
    water: int = int(input(f'Write how many ml of water do you want to add:'))
    milk: int = int(input(f'Write how many ml of milk do you want to add:'))
    beans: int = int(input(f'Write how many grams of coffee beans do you want to add:'))
    cups: int = int(input(f'Write how many disposable cups of coffee do you want to add:'))
    machine.fill_state(water=water, milk=milk, beans=beans, disposable_cups=cups, money=0)


def action_take(machine: CoffeeMachine) -> None:
    print(f'I gave you ${machine.take_money()}')


def main():
    machine: CoffeeMachine = CoffeeMachine()
    init_machine(machine)
    machine.print_state()

    action: str = input('Write action (buy, fill, take):')
    if action == 'buy':
        action_buy(machine)
    elif action == 'fill':
        action_fill(machine)
    elif action == 'take':
        action_take(machine)
    else:
        print('Unknown action')
    machine.print_state()


main()
