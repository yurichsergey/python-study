import random
import os.path


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


class RatingsStorage:

    def __init__(self, filename: str):
        self.filename = filename

    def read_score(self, name: str) -> int:
        if not os.path.exists(self.filename):
            return 0
        storage = self.__read_from_storage()
        return storage[name] if name in storage else 0

    def __read_from_storage(self):
        storage = {}
        f = open(self.filename, 'rt')
        for line in f.readlines():
            line_name, line_score = line.strip().split(' ')
            storage[line_name] = int(line_score)
        f.close()
        return storage

    def write_score(self, name: str, score: int) -> None:
        if os.path.exists(self.filename):
            storage = self.__read_from_storage()
        else:
            storage = {}

        f = open(self.filename, 'wt')
        if name not in storage:
            storage[name] = 0
        storage[name] += score
        f.writelines([k + ' ' + str(storage[k]) + '\n' for k in storage])
        f.close()


def main():
    name = input('Enter your name:')
    print(f'Hello, {name}')
    rating_storage = RatingsStorage('rating.txt')

    engine = RockPaperScissorsEngine()
    while True:
        player_choice = input()
        if player_choice == '!exit':
            print('Bye!')
            break
        if player_choice == '!rating':
            print(f'Your rating: {rating_storage.read_score(name)}')
            continue
        if not engine.is_valid_choice(player_choice):
            print('Invalid input')
            continue
        answer = engine.action(player_choice)
        rating_storage.write_score(name, answer.get_player_score())
        print(answer.get_result_str())


main()
