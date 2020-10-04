# Write your code here
# print('''
# Starting to make a coffee
# Grinding coffee beans
# Boiling water
# Mixing boiled water with crushed coffee beans
# Pouring coffee into the cup
# Pouring some milk into the cup
# Coffee is ready!
# ''')

waterOneCup = 200  # ml of water
milkOneCup = 50  # ml of milk
coffeeBeansOneCup = 15  # g of coffee beans.

cups = int(input('Write how many cups of coffee you will need:'))
print(f'For {cups} cups of coffee you will need:')
print(f'{cups * waterOneCup} ml of water')
print(f'{cups * milkOneCup} ml of milk')
print(f'{cups * coffeeBeansOneCup} g of coffee beans')
