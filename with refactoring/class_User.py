from class_Bank import Bank
from class_BinaryTree import *

class User(Bank):
    def __init__(self):
        self.number = ''
        self.pin = ''
        self.balance = 0

    def create_account(self):
        self.number,self.pin = Bank.create_account()

    def check_balance(self):
        self.balance = Bank.check_balance_from_db(self.number)

    def user_disconnect(self):
        Bank.disconnect_to_db()

    def log_into_account(self):
        print('Enter your card number:')
        card_number = input('>')
        self.number = card_number
        print('Enter your PIN:')
        card_pin = input('>')
        self.pin = card_pin
        if Bank.log_into_db(self.number,self.pin):
            print('You have successfully logged in!')
            self.user_menu()
        else:
            print('Wrong card number or PIN!')

    def add_income(self):
        print("Enter income:")
        value = int(input('>'))
        self.balance = Bank.add_income(self.number, value)

    def close_account(self):
        Bank.close_account_from_db(self.number)

    def transfer_check(self,card_number):
        if card_number == self.number:
            print("You can't transfer money to the same account!")
            return False

        if Bank.check_luna(card_number) == False:
            print('Probably you made a mistake in the card number. Please try again!')
            return False

        if Bank.check_card_in_db(card_number) == False:
            print('Such a card does not exist.')
            return False
        return True

    def do_transfer(self):
        print("Transfer")
        print("Enter card number:")
        card_number = input(">")
        if self.transfer_check(card_number) == False:
            return False

        print('Enter how much money you want to transfer:')
        money = int(input('>'))
        self.balance = Bank.get_balance_from_db(self.number)
        if self.balance < money:
            print("Not enough money!")
            return False
        else:
            self.balance -= money
            Bank.update_balance(self.balance,self.number)
            Bank.add_income(card_number,money)
            print('Success!')

    def user_menu(self):
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')
            user_choice = int(input('>'))
            if user_choice == 1:
                self.check_balance()
            elif user_choice == 2:
                self.add_income()
            elif user_choice == 3:
                self.do_transfer()
            elif user_choice == 4:
                self.close_account()
                break
            elif user_choice == 5:
                print('You have successfully logged out!')
                self.number = ''
                self.pin = ''
                self.balance = 0
                break
            elif user_choice == 0:
                self.user_disconnect()
                exit()

    def show_tree(self):
        numbers,balance = Bank.get_data_from_table_to_binary_tree()
        tree = Node(numbers[0],balance[0])
        for i in range(1,len(numbers)):
            tree.add(numbers[i],balance[i])
        printTree(tree)

    def show_heap(self):
        numbers,balance = Bank.get_data_from_table_to_heap()
        tree = Node(numbers[0],balance[0])
        for i in range(1,len(numbers)):
            tree.add(numbers[i],balance[i])
        printTree(tree)