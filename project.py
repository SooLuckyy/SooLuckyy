import os.path

class Account:

    def __init__(self, money, amount=0):
        self.money = money
        self.amount = amount
        self.previous = 0

    def deposit(self):
        amount = input("How much would you like to deposit? ")
        while True:
            try:
                amount = float(amount)
                break
            except:
                print("Please enter a number")
                amount = input("How much would you like to deposit? ")
        self.previous = amount
        self.money += amount
        self.amount = amount
        print(f"Current balance: £{self.money:,.2f}")

    def withdraw(self):
        amount = input("How much would you like to withdraw? ")
        while True:
            try:
                amount = float(amount)
                break
            except:
                print("Please enter a number")
                amount = input("How much would you like to withdraw? ")
        if amount > self.money:
            self.amount = amount
            print("Cannot withdraw more than you have")
        else:
            self.previous = amount
            self.money -= amount
            self.amount = amount
            print(f"Current balance: £{self.money:,.2f}")

    def delete(self):
        self.money = -1

def main():
    user = first_time_setup()
    what_does_user_want(user)
    aftermath(user)

def aftermath(user):
    # Updates account.txt file
    if user.money == -1:
        print("Are you sure you want to permanently terminate your account? ")
        while True:
            y_n = input("Y/N: ").lower()
            if y_n == "y":
                os.remove("account.txt")
                print("Your account has been successfully terminated")
                break
            elif y_n == "n":
                print("Your account is safe and still with us!")
                break
            else:
                pass
    else:
        # Grabs how much money the user currently has
        with open("account.txt") as file:
            lines = file.readlines()
            lines[1] = f"Amount: {user.money:.2f}\n"
        # Creates new file so new amount can be stored
        with open("account.txt","w") as new_file:
            for line in lines:
                new_file.write(line)

def record(user, action):
    # Opens up current file and saves each line of text in variable called lines
    with open("account.txt") as file:
        lines = file.readlines()
    # Rewrites account.txt with history of deposits/withdraws
    with open("account.txt","w") as new_file:
        for line in lines:
            new_file.write(line)
        if action == "d":
            new_file.write(f"Deposited: {user.amount:.2f}\n")
        elif user.amount > user.previous:
            pass
        else:
            new_file.write(f"Withdrew: {user.amount:.2f}\n")


def what_does_user_want(user):
    print("What would you like to do? Please type one of the below")
    ask = input("Deposit // Withdraw // History // Delete Account: ").lower()
    # Asks user for their action
    while True:
        if ask in ["deposit", "d"]:
            user.deposit()
            record(user, "d")
            break
        elif ask in ["withdraw", "w"]:
            user.withdraw()
            record(user, "w")
            break
        elif ask in ["history", "h"]:
            with open("account.txt") as file:
                file_contents = file.read()
            print(file_contents,end="")
            break
        elif ask in ["delete account", "delete", "del"]:
            user.delete()
            break
        else:
            print("Invalid function, please try again")
            ask = input("Deposit // Withdraw // Delete Account: ")

def first_time_setup():
    # Checks if user already has an account by seeing if their account.txt exists. If not, creates new account
    if os.path.isfile("account.txt"):
        with open("account.txt") as file:
            # Grabs how much money the user currently has
            username = file.readline()
            amount = file.readline()

        username = username.replace("Username: ", "")
        amount = float(amount.replace("Amount: ", ""))
        print(f"Welcome back {username}",end="")
        print(f"You currently have £{amount:,.2f}")
        return Account(amount)

    else:
        # Creates new account with 0 amount
        print("No account deleted")
        username = input("What is your name? ").title()
        with open("account.txt", "a") as file:
            file.write(f"Username: {username}\n")
            file.write(f"Amount: 0\n")
            file.write(f"--------------------\n")
        print(f"Welcome {username}")
        print(f"You currently have £0.00")
        return Account(0)

if __name__ == "__main__":
    main()
