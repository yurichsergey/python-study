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
        print(f'${self.__money} of money')

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

    def get_not_enough_resources(self, recipe: CoffeeTypeRecipe) -> list:
        not_enough_resources = []
        if recipe.get_water() > self.__water:
            not_enough_resources.append('water')
        if recipe.get_milk() > self.__milk:
            not_enough_resources.append('milk')
        if recipe.get_beans() > self.__beans:
            not_enough_resources.append('bean')
        return not_enough_resources


class CoffeeTypeFactory:

    def create_espresso(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=250, milk=0, beans=16, cost=4)

    def create_latte(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=350, milk=75, beans=20, cost=7)

    def create_cappuccino(self) -> CoffeeTypeRecipe:
        return CoffeeTypeRecipe(water=200, milk=100, beans=12, cost=6)


class CoffeeMachineActions:

    def __init__(self, machine: CoffeeMachine):
        self.__machine = machine

    def action_buy(self) -> None:
        type_factory = CoffeeTypeFactory()
        coffee_type_storage = {
            '1': type_factory.create_espresso(),
            '2': type_factory.create_latte(),
            '3': type_factory.create_cappuccino(),
            'back': None
        }
        coffee_type_id = input('What do you want to buy?'
                               ' 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:')
        coffee_type = coffee_type_storage[coffee_type_id]
        if not coffee_type:
            return  # back to main menu
        not_enough_resources = self.__machine.get_not_enough_resources(coffee_type)
        if not_enough_resources:
            print('Sorry, not enough ' + ', '.join(not_enough_resources) + '!')
            # for resource in not_enough_resources:
            #     print(f'Sorry, not enough {resource}!')
            return
        print('I have enough resources, making you a coffee!')
        self.__machine.make_coffee(coffee_type)

    def action_fill(self) -> None:
        water: int = int(input(f'Write how many ml of water do you want to add:'))
        milk: int = int(input(f'Write how many ml of milk do you want to add:'))
        beans: int = int(input(f'Write how many grams of coffee beans do you want to add:'))
        cups: int = int(input(f'Write how many disposable cups of coffee do you want to add:'))
        self.__machine.fill_state(water=water, milk=milk, beans=beans, disposable_cups=cups, money=0)

    def action_take(self) -> None:
        print(f'I gave you ${self.__machine.take_money()}')


def main():
    machine: CoffeeMachine = CoffeeMachine()
    machine.fill_state(water=400, milk=540, beans=120, disposable_cups=9, money=550)
    actions = CoffeeMachineActions(machine)

    while True:
        action: str = input('Write action (buy, fill, take, remaining, exit):')
        if action == 'buy':
            actions.action_buy()
        elif action == 'fill':
            actions.action_fill()
        elif action == 'take':
            actions.action_take()
        elif action == 'remaining':
            machine.print_state()
        elif action == 'exit':
            break
        else:
            print('Unknown action')


main()
