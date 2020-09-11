"""
File: hangman.py
Name: Ian Kuo
-----------------------------
This program plays hangman game.
Users sees a dashed word, trying to
correctly figure the un-dashed word out
by inputting one character each round.
If the user input is correct, show the
updated word on console. Players have N_TURNS
to try in order to win this game.
"""


import random


# This constant controls the number of guess the player has
N_TURNS = 7


def main():
    """
    The objective of this program is to create a hangman game. Based on the given randomized word, the user guesses
    one character at a time. Should the guess be right, the program reveals the character within the randomized
    word. Otherwise, the number of guesses minuses one, with the total guesses being determined by a constant N_TURNS,
    and once the guesses are tried out, the game is set to be over.
    """
    ran = random_word()
    turns = N_TURNS
    current = dash(ran)
    print('Welcome to Hangman! The word you will be guessing looks like ' + dash(ran) +
          ' and you have ' + str(turns) + ' turns left!')
    while turns >= 0 and current != ran:
        ans = ''
        guess = input('What is your guess? ')
        guess = guess.upper()
        if guess.isalpha() and len(guess) == 1:
            if guess in ran:
                for i in range(len(ran)):
                    ch = ran[i]
                    if guess == ch:
                        ans += guess
                    else:
                        ans += current[i]
                print('That is correct! The word now looks like ' + ans)
                current = ans
                if current == ran:
                    print('You win! The word is ' + ran)

            else:
                turns -= 1
                print('Wrong guess! You have ' + str(turns) + ' turns left!')
                if turns == 0:
                    print('You are completely hung! The word is ' + ran)
        else:
            print('Illegal format!')


def dash(ran):
    """
    :param ran: str, a random word created by random_word()
    :return: str, characters not revealed being covered by dash
    """
    word_hash = ''
    for i in range(len(ran)):
        ch = ran[i]
        ch = '-'
        word_hash += ch
    return word_hash


def random_word():
    num = random.choice(range(9))
    if num == 0:
        return "NOTORIOUS"
    elif num == 1:
        return "GLAMOROUS"
    elif num == 2:
        return "CAUTIOUS"
    elif num == 3:
        return "DEMOCRACY"
    elif num == 4:
        return "BOYCOTT"
    elif num == 5:
        return "ENTHUSIASTIC"
    elif num == 6:
        return "HOSPITALITY"
    elif num == 7:
        return "BUNDLE"
    elif num == 8:
        return "REFUND"


#####  DO NOT EDIT THE CODE BELOW THIS LINE  #####
if __name__ == '__main__':
    main()
