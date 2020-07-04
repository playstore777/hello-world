# Write your code here
# Starting from scratch again!!
# first * 2 to the odd positions
# subtract by 9 to the > 9
import os
import random
# sql modules
import sqlite3

database = 'card.s3db'


class CreditCard:
    """generates card number and card pin"""

    def __init__(self):
        """initialization and database creation and also data insertion"""
        self.database_create()
        self.card_number = str(400000) + str(self.random_number_generator(9))
        self.card_number += str(self.checksum(self.card_number))
        self.card_number = int(self.card_number)
        self.card_pin = self.random_number_generator(4)
        self.balance = 0
        self.insert_data()

    @staticmethod
    def random_number_generator(max_number):
        """random number generator for card number (15digits) and for PIN number (4digits)"""
        return ''.join(['{}'.format(random.randint(0, 9)) for _ in range(0, max_number)])

    @staticmethod
    def checksum(card_number):
        """checksum number creator/generator"""
        card_number = list(map(int, card_number))
        for index in range(0, len(card_number), 2):
            card_number[index] *= 2
        for num in range(0, len(card_number)):
            if card_number[num] > 9:
                card_number[num] -= 9
        for number in range(0, 10):
            card_number.append(number)
            if sum(card_number) % 10 == 0:
                break
            else:
                card_number.pop(-1)
        return number

    @staticmethod
    def database_create():
        """database and table creator if not exists"""
        if os.path.exists('card.s3db'):
            connection = sqlite3.connect(database)
            with connection:
                cursor = connection.cursor()
                # card table
                cursor.execute("""CREATE TABLE IF NOT EXISTS card(
                id INTEGER PRIMARY KEY,
                number TEXT,
                pin TEXT,
                balance INTEGER DEFAULT 0)""")

                connection.commit()

    def insert_data(self):
        """data insertion in the tables"""
        if os.path.exists('card.s3db'):
            connection = sqlite3.connect(database)
            with connection:
                cursor = connection.cursor()
                cursor.execute("INSERT INTO card VALUES (?, ?, ?, ?)",
                               (None, self.card_number, self.card_pin, self.balance))
                connection.commit()
        else:
            self.database_create()


# functions
def main_menu():
    """main function"""
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        menu_input = int(input())
        if menu_input == 1:
            create_card()
        elif menu_input == 2:
            account_login()
        else:
            print("\nBye!")
            exit()


def create_card():
    """Credit card object creator function"""
    card = CreditCard()
    print("Your card has been created")
    print("Your card number:")
    print(card.card_number)
    print("Your card PIN:")
    print(card.card_pin)
    return card


def open_database(database_name):
    if os.path.exists(database_name):
        connection = sqlite3.connect(database_name)
        with connection:
            cursor = connection.cursor()
            return connection, cursor
    print("The 'card.s3db' does not exists")


def account_login():
    """login checker function"""
    connection, cursor = open_database(database)
    cursor.execute("Select number, pin from card")
    card = cursor.fetchall()
    print("Enter your card number:")
    input_card_number = str(input())
    print("Enter your PIN:")
    input_card_pin = str(input())
    if (input_card_number, input_card_pin,) in card:
        print("You have successfully logged in!")
        logged_menu(input_card_number)
    else:
        print("Wrong card number or PIN!")


def add_income(card, adding_amount):
    """add money"""
    connection, cursor = open_database(database)
    cursor.execute(f"Select balance from card Where number = {card}")
    balance = cursor.fetchall()[-1][-1]
    adding_amount = balance + adding_amount
    cursor.execute(f"UPDATE card SET balance = {adding_amount} WHERE number = ({card})")
    connection.commit()
    print("income was added!")
    logged_menu(card)


def check(number):
    card_number = list(map(int, number))
    last_digit = card_number.pop(-1)
    for index in range(0, len(card_number), 2):
        card_number[index] *= 2
    for num in range(0, len(card_number)):
        if card_number[num] > 9:
            card_number[num] -= 9
    card_number.append(last_digit)
    if sum(card_number) % 10 == 0:
        return "Such a card does not exist."
    return 'Probably you made mistake in card number. Please try again!'


def transfer(card):
    """transfer money"""
    connection, cursor = open_database(database)
    print("Transfer")
    print("Enter card number:")
    # input card number
    card_number = str(input())
    cursor.execute("Select number from card")
    # Database card number
    res = cursor.fetchall()
    cursor.execute(f"Select balance from card Where number = ({card})")
    balance = cursor.fetchall()[-1]
    if card_number == card:
        print("You can't transfer money to the same account!")
        logged_menu(card)
    # if the input card number in the database list then allowed to enter the amount
    elif (card_number,) in res:
        print("Enter how much money you want to transfer: ")
        amount_transfer = int(input())
        if amount_transfer > balance[0]:
            print("Not enough money!")
            logged_menu(card)
        else:
            cursor.execute(f'Select balance From card Where number = {card_number}')
            amount = int(cursor.fetchone()[-1])
            amount = amount + amount_transfer
            cursor.execute(f'Update card SET balance = {amount} Where number = {card_number}')
            amount_transfer = balance[0] - amount_transfer
            cursor.execute(f"Update card Set balance = {amount_transfer} Where number = {card}")
            print("Success!")
            connection.commit()
            logged_menu(card)
    else:
        # to check whether the number satisfies the Luhn algorithm or not
        result = check(card_number)
        print(result)
        logged_menu(card)
    connection.commit()
    logged_menu(card)


def logged_menu(card_number):
    """logged menu display function"""
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    input_log = int(input())
    if input_log == 1:
        connection, cursor = open_database(database)
        cursor.execute(f"Select balance from card Where number = ({card_number})")
        print(cursor.fetchone()[-1])
        logged_menu(card_number)
    elif input_log == 2:
        print("Enter income: ")
        amount = int(input())
        add_income(card_number, amount)
    elif input_log == 3:
        transfer(card_number)
    elif input_log == 4:
        # 4000008849123562
        connection, cursor = open_database(database)
        cursor.execute(f"DELETE FROM card WHERE number = {card_number}")
        connection.commit()
        print("The account has been closed!")
        main_menu()
    elif input_log == 5:
        print("You have successfully logged out!")
        main_menu()
    else:
        exit()


# main
main_menu()
