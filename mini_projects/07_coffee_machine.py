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

    def fill_water(self, water: int):
        self.__water += water

    def fill_milk(self, milk: int):
        self.__milk += milk

    def fill_beans(self, beans: int):
        self.__beans += beans

    def fill_disposable_cups(self, disposable_cups: int):
        self.__disposable_cups += disposable_cups

    def fill_money(self, money: int):
        self.__money += money

    def print_state(self) -> str:
        return f'The coffee machine has:\n' \
               + f'{self.__water} of water\n' \
               + f'{self.__milk} of milk\n' \
               + f'{self.__beans} of coffee beans\n' \
               + f'{self.__disposable_cups} of disposable cups\n' \
               + f'${self.__money} of money'

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


class ActionInterface:

    def action(self, data: str = '') -> 'OutputFormat':
        pass

    def greeting(self) -> str:
        return ''

    def interrupt_flow(self) -> bool:
        return False


class ActionChooseAction(ActionInterface):
    def __init__(self, machine: CoffeeMachine):
        self.__machine: CoffeeMachine = machine

    def greeting(self) -> str:
        return '\nWrite action (buy, fill, take, remaining, exit):'

    def action(self, data: str = '') -> 'OutputFormat':
        if data == 'buy':
            return OutputFormat('', ActionBuy(self.__machine, self))
        elif data == 'fill':
            return OutputFormat('', ActionFill(self.__machine, self))
        elif data == 'take':
            return ActionTake(self.__machine, self).action()
        elif data == 'remaining':
            return ActionPrintState(self.__machine, self).action()
        elif data == 'exit':
            return OutputFormat('', ActionExit())
        else:
            OutputFormat(f'Unknown action: "{data}"', self)

        return OutputFormat('', self)


class ActionBuy(ActionInterface):

    def __init__(self, machine: CoffeeMachine, action: ActionInterface):
        self.__action = action
        self.__machine = machine

    def greeting(self) -> str:
        return '\nWhat do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:'

    def action(self, data: str = '') -> 'OutputFormat':
        type_factory = CoffeeTypeFactory()
        coffee_type_storage = {
            '1': type_factory.create_espresso(),
            '2': type_factory.create_latte(),
            '3': type_factory.create_cappuccino(),
            'back': None
        }
        coffee_type_id: str = data
        coffee_type: CoffeeTypeRecipe = coffee_type_storage[coffee_type_id]
        if not coffee_type:
            return OutputFormat('', self.__action)  # back to main menu
        not_enough_resources = self.__machine.get_not_enough_resources(coffee_type)
        if not_enough_resources:
            return OutputFormat('Sorry, not enough ' + ', '.join(not_enough_resources) + '!', self.__action)
        self.__machine.make_coffee(coffee_type)
        return OutputFormat('I have enough resources, making you a coffee!', self.__action)


class ActionFill(ActionInterface):

    def __init__(self, machine: CoffeeMachine, action: ActionInterface):
        self.__action = action
        self.__machine = machine
        self.__ingredients = [
            (f'Write how many ml of water do you want to add:', self.__machine.fill_water,),
            (f'Write how many ml of milk do you want to add:', self.__machine.fill_milk,),
            (f'Write how many grams of coffee beans do you want to add:', self.__machine.fill_beans,),
            (f'Write how many disposable cups of coffee do you want to add:', self.__machine.fill_disposable_cups,),
        ]
        self.__current_ingredient = 0

    def greeting(self) -> str:
        greeting: str
        action: callable
        greeting, action = self.__ingredients[self.__current_ingredient]
        return greeting

    def action(self, data: str = '') -> 'OutputFormat':
        greeting: str
        action: callable
        greeting, action = self.__ingredients[self.__current_ingredient]
        action(int(data))
        if self.__current_ingredient < (len(self.__ingredients) - 1):
            self.__current_ingredient += 1
            return OutputFormat('', self)
        else:
            self.__current_ingredient = 0
            return OutputFormat('', self.__action)


class ActionTake(ActionInterface):

    def __init__(self, machine: CoffeeMachine, action: ActionInterface):
        self.__action = action
        self.__machine = machine

    def action(self, data: str = '') -> 'OutputFormat':
        return OutputFormat(f'I gave you ${self.__machine.take_money()}', self.__action)


class ActionPrintState(ActionInterface):

    def __init__(self, machine: CoffeeMachine, action: ActionInterface):
        self.__action = action
        self.__machine = machine

    def action(self, data: str = '') -> 'OutputFormat':
        return OutputFormat(self.__machine.print_state(), self.__action)


class ActionExit(ActionInterface):

    def interrupt_flow(self) -> bool:
        return True


class OutputFormat:

    def __init__(self, output_str: str, action: ActionInterface):
        self.__output_str: str = output_str
        self.__action: ActionInterface = action

    def get_output_str(self) -> str:
        return self.__output_str

    def get_action(self) -> ActionInterface:
        return self.__action


class CoffeeMachineConsole:

    def __init__(self, machine: CoffeeMachine):
        self.__machine: CoffeeMachine = machine

    def work(self) -> None:
        action: ActionInterface = ActionChooseAction(self.__machine)
        while True:
            if action.interrupt_flow():
                return  # exit
            if action.greeting():
                print(action.greeting())
            input_data: str = input()
            output: OutputFormat = action.action(input_data)
            if output.get_output_str():
                print(output.get_output_str())
            action = output.get_action()


def main():
    machine: CoffeeMachine = CoffeeMachine()
    machine.fill_state(water=400, milk=540, beans=120, disposable_cups=9, money=550)
    CoffeeMachineConsole(machine).work()


main()
