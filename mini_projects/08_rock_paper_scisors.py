import random


class RockPaperScissorsEngine:
    PAPER = 'paper'
    ROCK = 'rock'
    SCISSORS = 'scissors'

    won_steps = {
        PAPER: SCISSORS,
        ROCK: PAPER,
        SCISSORS: ROCK
    }

    valid_steps = list(won_steps)

    def is_valid_choice(self, choice: str) -> bool:
        return choice in self.valid_steps

    def action(self, player_choice: str) -> str:
        if not self.is_valid_choice(player_choice):
            return 'Invalid input'
        computer_choice = random.choice(self.valid_steps)
        if player_choice == computer_choice:
            answer = f'There is a draw ({player_choice})'
        elif self.won_steps[player_choice] != computer_choice:
            answer = f'Well done. The computer chose {computer_choice} and failed'
        else:
            answer = f'Sorry, but the computer chose {computer_choice}'
        return answer


def main():
    engine = RockPaperScissorsEngine()
    while True:
        player_choice = input()
        if player_choice == '!exit':
            print('Bye!')
            break
        if not engine.is_valid_choice(player_choice):
            print('Invalid input')
            continue
        answer = engine.action(player_choice)
        print(answer)


main()
