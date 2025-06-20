import requests
from random import randint

def main():

    gen_5lw()
    welcome()
    start_game(gen_5lw())
    end_game()

def start_game(target):
    print(target)
    user_guess = input("Guess: ")
    check_word(user_guess)
    attempts = 5
    l = ["_", "_", "_", "_", "_"]
    while True:
        if user_guess == target:
            break
        for index, letter in enumerate(user_guess):
            if letter in target:
                if index == target.index(letter):
                    l[index] = letter
                    continue
                l[index] = f"{letter}*"

        attempts -= 1
        print("Attempts remaining:", attempts)
        print(" ".join(l))
        l = ["_", "_", "_", "_", "_"]
        user_guess = input("Guess: ")
        check_word(user_guess)

def end_game():
    print("You got it! Thanks for playing")

def check_word(s):
    url = "https://cheaderthecoder.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    while True:
        if len(s) != 5 or s not in words["words"]:
            s = input("Guess: ")
        else:
            return s

def welcome():
    print("Welcome to wordel :) \nA letter with * means the letter appears in the word but different position")
    print("For a full list of available words, please visit\nhttps://cheaderthecoder.github.io/5-Letter-words/words.txt")
    print("_ " * 5)

def gen_5lw():
    # Generate a random 5 letter word
    url = "https://cheaderthecoder.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    rand_int = randint(0,len(words))
    return words["words"][rand_int]


if __name__ == "__main__":
    main()
