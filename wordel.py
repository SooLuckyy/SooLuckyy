import requests
from random import randint
from rich.console import Console

console = Console()

def main():
    word = gen_5lw()
    welcome()
    wl = start_game(word)
    end_game(wl, word)

def start_game(target):
    print(target) # Can uncomment to see the chosen word that the User must guess
    attempts = 5
    print_attempts(attempts)
    # Help visualise the "keyboard"
    alphabet = "QWERTYUIOPASDFGHJKLZXCVBNM"
    alphabet_dict = {"Q": "dodger_blue1", "W": "dodger_blue1", "E": "dodger_blue1", "R": "dodger_blue1", "T": "dodger_blue1",
              "Y": "dodger_blue1", "U": "dodger_blue1", "I": "dodger_blue1", "O": "dodger_blue1", "P": "dodger_blue1",
              "A": "dodger_blue1", "S": "dodger_blue1", "D": "dodger_blue1", "F": "dodger_blue1", "G": "dodger_blue1",
              "H": "dodger_blue1", "J": "dodger_blue1", "K": "dodger_blue1", "L": "dodger_blue1", "Z": "dodger_blue1",
              "X": "dodger_blue1", "C": "dodger_blue1", "V": "dodger_blue1", "B": "dodger_blue1", "N": "dodger_blue1", "M": "dodger_blue1"}
    # Blank template for list of letter/colour pair
    letters_output = [[" ", "grey50"], [" ", "grey50"], [" ", "grey50"], [" ", "grey50"], [" ", "grey50"]]

    alphabet, alphabet_dict = keyboard_visual(alphabet, alphabet_dict, letters_output)
    user_guess = check_word(input("Guess: ").lower()).upper()
    print("********************************************************************************")
    letter_set_original = letter_count(target) # Grab unique set of letters and its count.

    while True:
        letter_set = letter_set_original.copy() # This is to "fix" the contents in a new loop while I "modify" during the loop
        if user_guess == target:
            return "W"
        for index, letter in enumerate(user_guess):
            if letter in target: # Checks if letter is part of "target"
                if user_guess[index] == target[index]: # If letter is in the right position
                    letters_output[index][0] = letter
                    letters_output[index][1] = "green1"
                    letter_set[letter] -= 1
                    continue

                else: # Correct letter, wrong position
                    letters_output[index][0] = letter
                    letters_output[index][1] = "yellow3"
                    letter_set[letter] -= 1
            else: # Populates incorrect letter
                letters_output[index][0] = letter
        attempts -= 1
        if attempts == 0: # Checks if all lives are gone
            return "L"

        print_attempts(attempts)
        print_letters(letters_output)
        alphabet, alphabet_dict = keyboard_visual(alphabet, alphabet_dict, letters_output)
        
        # Resets letters_output and User guess
        letters_output = [[" ", "grey50"], [" ", "grey50"], [" ", "grey50"], [" ", "grey50"], [" ", "grey50"]]
        user_guess = check_word(input("Guess: ").lower()).upper()
        print("********************************************************************************")


def end_game(wl, word):
    # Prints end game message
    if wl == "W":
        console.print(f"[bold green]You got it![/] The word was [bold turquoise2]\"{word}\"[/]! Thanks for playing!")
        print("********************************************************************************")
    else:
        console.print(f"[bold red]Unlucky![/] The word was [bold turquoise2]\"{word}\"[/]! Thanks for playing!")
        print("********************************************************************************")


def check_word(word):
    # Sees if the word the User entered is within the list of words available
    url = "https://darkermango.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    while True:
        if len(word) != 5 or word not in words["words"]: # Checks for length of word as well but this may not be needed
            print("********************************************************************************")
            console.print(f"The word [bold turquoise2]\"{word.upper()}\"[/] is not in the list, please try again.")
            word = input("Guess: ")

        else:
            return word


def letter_count(word):
    # Returns a dict of unique letters in target and the count of each letter
    word_dict = {}
    for letter in word:
        if letter in word_dict:
            word_dict[f"{letter}"] += 1
        else:
            word_dict[f"{letter}"] = 1
    return word_dict


def print_letters(letters_output):
    # Takes in a list of list of letters and their respective colour
    print("Target:", end = " ")
    for i in range(5):
        console.print(f"[underline {letters_output[i][1]}]{letters_output[i][0]}[/]", end = " ")
    # Adds back a new line
    print("")


def print_attempts(attempts_left):
    # Colours the number in "Attemps remaining: x"
    attempts_colour = {5:"bold green", 4: "bold sea_green1", 3: "bold yellow", 2: "bold orange1", 1: "bold red1"}
    for key, value in attempts_colour.items():
        if attempts_left == key:
            console.print(f"Attempts remaining: [{value}]{attempts_left}[/]")
            break


def keyboard_visual(alphabet, alphabet_dict, letters_output):
    # Prints the keyboard with the respective colour of the letter
    for letter, colour in letters_output:
        if letter not in alphabet:
            continue
        elif colour != "yellow3":
            alphabet = alphabet.replace(letter, "") # Removes letter to for "faster" computation
            alphabet_dict[letter] = colour # Colours the letter accordingly
        else:
            alphabet_dict[letter] = colour # Colours the letter accordingly

    top_kb = "QWERTYUIOP"
    middle_kb = "ASDFGHJKL"
    bot_kb = "ZXCVBNM"

    # Prints "top" section keyboard
    for letter in top_kb:
        console.print(f"[{alphabet_dict[letter]}]{letter}[/] ", end="")
    print("") # New line
    print(" ", end="") # For "visual" keyboard placement
    # Prints "middle" section of keyboard
    for letter in middle_kb:
        console.print(f"[{alphabet_dict[letter]}]{letter}[/] ", end="")
    print("") # New line
    print("  ", end="") # For "visual" keyboard placement
    # Prints "bottom" section of keyboard
    for letter in bot_kb:
        console.print(f"[{alphabet_dict[letter]}]{letter}[/] ", end="")
    print("") # For new line
    return alphabet, alphabet_dict


def welcome():
    print("********************************************************************************")
    print("Welcome to wordel :)")
    console.print("A [bold green]GREEN[/] letter means the letter appears in the word and [bold green]CORRECT[/] position")
    console.print("A [bold yellow]YELLOW[/] letter means the letter appears in the word and [bold yellow]DIFFERNT[/] position")
    console.print("For a full list of available words, please visit\n" \
    "[bold blue]https://darkermango.github.io/5-Letter-words/words.txt[/]")
    print("********************************************************************************")
    print("Target:", "_ " * 5)


def gen_5lw():
    # Choose a random 5-letter word
    url = "https://darkermango.github.io/5-Letter-words/words.json"
    response = requests.get(url)
    words = response.json()
    # Generates a random number to pick a random word from the list
    rand_int = randint(0,len(words["words"]))
    return words["words"][rand_int].upper()


if __name__ == "__main__":
    main()
