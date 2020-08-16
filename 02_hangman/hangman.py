import random


def get_hint(correct_word, guessed_letters):
    hint = ''
    for letter in correct_word:
        hint += letter if letter in guessed_letters else '-'
    return hint


def is_guessed_word(correct_word, guessed_letters):
    is_guessed = True
    for letter in correct_word:
        if letter not in guessed_letters:
            is_guessed = False
            break
    return is_guessed


# Write your code here
print('H A N G M A N')


def hangman():
    words = ['python', 'java', 'kotlin', 'javascript']
    # 'correct_word' is a string
    correct_word = random.choice(words)  # type: str
    guessed_letters = set()
    lives = 8
    while True:
        print("")
        print(get_hint(correct_word, guessed_letters))
        letter = input('Input a letter:')
        has_input_error = False
        if len(letter) != 1:
            has_input_error = True
            print("You should input a single letter")
        if letter < 'a' or letter > 'z':
            has_input_error = True
            print("It is not an ASCII lowercase letter")
        if letter in guessed_letters:
            has_input_error = True
            print("You already typed this letter")
        if not has_input_error:
            if letter not in correct_word:
                lives -= 1
                print("No such letter in the word")
            guessed_letters.add(letter)

        if is_guessed_word(correct_word, guessed_letters):
            print(correct_word)
            print('You guessed the word!')
            print('You survived!')
            break
        if lives < 1:
            print('You are hanged!')
            break


while True:
    command = input('Type "play" to play the game, "exit" to quit:')
    if command == 'play':
        hangman()
    elif command == 'exit':
        break

# print("")
# print("Thanks for playing!")
# print("We'll see how well you did in the next stage")
