import random


class AnswerStep:

    def __init__(self, player_score: int, result_str: str):
        self.player_score = player_score
        self.result_str = result_str

    def get_player_score(self) -> int:
        return self.player_score

    def get_result_str(self) -> str:
        return self.result_str


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

    def action(self, player_choice: str) -> AnswerStep:
        if not self.is_valid_choice(player_choice):
            return AnswerStep(0, 'Invalid input')
        computer_choice = random.choice(self.valid_steps)
        if player_choice == computer_choice:
            answer = AnswerStep(50, f'There is a draw ({player_choice})')
        elif self.won_steps[player_choice] != computer_choice:
            answer = AnswerStep(100, f'Well done. The computer chose {computer_choice} and failed')
        else:
            answer = AnswerStep(0, f'Sorry, but the computer chose {computer_choice}')
        return answer


def main():
    engine = RockPaperScissorsEngine()
    while True:
        player_choice = input()
        if player_choice == '!exit':
            print('Bye!')
            break
        if player_choice == '!rating':
            print('Bye!')
            continue
        if not engine.is_valid_choice(player_choice):
            print('Invalid input')
            continue
        answer = engine.action(player_choice)
        print(answer.get_result_str())


main()
