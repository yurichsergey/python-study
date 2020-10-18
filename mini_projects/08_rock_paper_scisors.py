PAPER = 'paper'
ROCK = 'rock'
SCISSORS = 'scissors'

won_steps = {
    PAPER: SCISSORS,
    ROCK: PAPER,
    SCISSORS: ROCK
}

player_choose = input()

print('Sorry, but the computer chose ' + won_steps[player_choose])
