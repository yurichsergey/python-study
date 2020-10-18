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

    def engine(self, player_choose: str) -> str:
        computer_choose = random.choice(list(self.won_steps))
        if player_choose == computer_choose:
            answer = f'There is a draw ({player_choose})'
        elif self.won_steps[player_choose] != computer_choose:
            answer = f'Well done. The computer chose {computer_choose} and failed'
        else:
            answer = f'Sorry, but the computer chose {computer_choose}'
        return answer


def main():
    player_choose = input()
    answer = RockPaperScissorsEngine().engine(player_choose)
    print(answer)


main()
