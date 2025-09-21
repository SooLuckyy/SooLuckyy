import requests
from random import randint
#import rich

def main():

    word = gen_5lw()
    welcome()
    wl = start_game(word)
    end_game(wl, word)

def start_game(target):
    attempts = 5
    print("Attempts remaining:", attempts)
    user_guess = check_word(input("Guess: ").lower())
    print("********************************************************************************")
    letter_set_original = letter_count(target) # Grab unique set of letters and its count.
    l = ["_", "_", "_", "_", "_"]

    while True:
        letter_set = letter_set_original.copy() # This is to "fix" the contents in a new loop while I "modify" during the loop
        if user_guess == target:
            return "W"
        for index, letter in enumerate(user_guess):
            if letter in target:
                if user_guess[index] == target[index]:
                    l[index] = letter.upper()
                    # If User word has more than 1 letter and the first is placed in wrong position but second is correct in "target", remove the first
                    if letter_set[letter] <= 0:
                        l[l.index(letter)] = "_"
                    letter_set[letter] -= 1
                    continue

                if letter_set[letter] <= 0: # Ensuring letters from User word doesn't appear more times than it should
                    continue
                else:
                    l[index] = letter
                    letter_set[letter] -= 1
        attempts -= 1
        if attempts == -1: # Checks if all lives are gone
            return "L"
        print("Attempts remaining:", attempts)
        print("Target:"," ".join(l))
        l = ["_", "_", "_", "_", "_"]
        user_guess = check_word(input("Guess: ").lower())
        print("********************************************************************************")


def end_game(wl, word):
    if wl == "W":
        print(f"You got it! The word was \"{word}\"! Thanks for playing!")
        print("********************************************************************************")
    else:
        print(f"Unlucky! The word was \"{word}\"! Thanks for playing!")
        print("********************************************************************************")


def check_word(s):
    # Sees if the word the User entered is within the list of words available
    url = "https://darkermango.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    while True:
        if len(s) != 5 or s not in words["words"]:
            print("********************************************************************************")
            print(f"The word \"{s}\" is not in list, please try again.")
            s = input("Guess: ")

        else:
            return s

def letter_count(word):
    # letter_count returns a dict of unique letters in target and the count of each letter
    word_dict = {}
    for letter in word:
        if letter in word_dict:
            word_dict[f"{letter}"] += 1
        else:
            word_dict[f"{letter}"] = 1
    return word_dict


def welcome():
    print("********************************************************************************")
    print("Welcome to wordel :)\n" \
    "A UPPERCASE letter means the letter appears in the word and CORRECT position")
    print("A LOWERCASE letter means the letter appears in the word and DIFFERNT position")
    print("For a full list of available words, please visit\n" \
    "https://darkermango.github.io/5-Letter-words/words.txt")
    print("********************************************************************************")
    print("Target:", "_ " * 5)

def gen_5lw():
    # Choose a random 5-letter word
    url = "https://darkermango.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    # Generates a random number to pick a random word from the list
    rand_int = randint(0,len(words["words"]))
    return words["words"][rand_int]


if __name__ == "__main__":
    main()
