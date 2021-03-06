# Simple Chatty Bot
# Here, at the beginning of your programmer’s path, creating a simple console
#   chat bot will do wonders to guide you through the basics of coding. During this
#   journey you will also play some word and number games that you are going to implement
#   all on your own. Pack up and let’s hit the road, my friend!<br/><br/>Learn more
#   at <a href="https://hyperskill.org">https://hyperskill.org/projects/97</a>

def greet(bot_name, birth_year):
    print('Hello! My name is ' + bot_name + '.')
    print('I was created in ' + birth_year + '.')


def remind_name():
    print('Please, remind me your name.')
    name = input()
    print('What a great name you have, ' + name + '!')


def guess_age():
    print('Let me guess your age.')
    print('Enter remainders of dividing your age by 3, 5 and 7.')

    rem3 = int(input())
    rem5 = int(input())
    rem7 = int(input())
    age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105

    print("Your age is " + str(age) + "; that's a good time to start programming!")


def count():
    print('Now I will prove to you that I can count to any number you want.')

    num = int(input())
    curr = 0
    while curr <= num:
        print(curr, '!')
        curr = curr + 1


def test():
    print("Let's test your programming knowledge.")
    question = '''Why do we use methods?
1. To repeat a statement multiple times.
2. To decompose a program into several small subroutines.
3. To determine the execution time of a program.
4. To interrupt the execution of a program.'''
    print(question)
    correct_answer = 2
    while True:
        answer = int(input())
        if answer == correct_answer:
            print('Completed, have a nice day!')
            break
        print('Please, try again.')


def end():
    print('Congratulations, have a nice day!')


greet('Flash-bot', '2020')
remind_name()
guess_age()
count()
test()
end()
