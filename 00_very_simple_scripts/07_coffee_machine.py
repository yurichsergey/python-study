import unittest

# print('''
# Starting to make a coffee
# Grinding coffee beans
# Boiling water
# Mixing boiled water with crushed coffee beans
# Pouring coffee into the cup
# Pouring some milk into the cup
# Coffee is ready!
# ''')

water_one_cup: int = 200  # ml of water
milk_one_cup: int = 50  # ml of milk
beans_one_cup: int = 15  # g of coffee beans.

water_has: int = int(input(f'Write how many ml of water the coffee machine has:'))
milk_has: int = int(input(f'Write how many ml of milk the coffee machine has:'))
beans_have: int = int(input(f'Write how many grams of coffee beans the coffee machine has:'))
cups_need: int = int(input('Write how many cups of coffee you will need:'))

water_needs: int = cups_need * water_one_cup
milk_needs: int = cups_need * milk_one_cup
beans_need: int = cups_need * beans_one_cup

# print(f'For {cups_need} cups of coffee you will need:')
# print(f'{water_needs} ml of water')
# print(f'{milk_needs} ml of milk')
# print(f'{beans_need} g of coffee beans')

cups_by_water_allow: int = water_has // water_one_cup
cups_by_milk_allow: int = milk_has // milk_one_cup
cups_by_beans_allow: int = beans_have // beans_one_cup
cups_result_allow: int = min([cups_by_water_allow, cups_by_milk_allow, cups_by_beans_allow, ])

if cups_need <= cups_result_allow:
    cups_reminder: int = cups_result_allow - cups_need
    additional_info: str = f' (and even {cups_reminder} more than that)' if cups_reminder > 0 else ''
    print(f'Yes, I can make that amount of coffee' + additional_info)
else:
    print(f'No, I can make only {cups_result_allow} cups of coffee')
