import random

PAPER = 'paper'
ROCK = 'rock'
SCISSORS = 'scissors'

won_steps = {
    PAPER: SCISSORS,
    ROCK: PAPER,
    SCISSORS: ROCK
}

player_choose = input()
computer_choose = random.choice(list(won_steps))

if player_choose == computer_choose:
    print(f'There is a draw ({player_choose})')
elif won_steps[player_choose] != computer_choose:
    print(f'Well done. The computer chose {computer_choose} and failed')
else:
    print(f'Sorry, but the computer chose {computer_choose}')
