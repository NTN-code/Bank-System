from class_User import User
from class_Bank import Bank
import sqlite3

def main_menu():
    user = User()
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("3. Show table")
        print("4. Show Binary Tree")
        print("5. Show Heap")
        print("0. Exit")
        user_choice = int(input('>'))
        if user_choice == 1:
            user.create_account()
        elif user_choice == 2:
            user.log_into_account()
        elif user_choice == 3:
            Bank.show_table()
        elif user_choice == 4:
            user.show_tree()
        elif user_choice == 5:
            user.show_heap()
        elif user_choice == 0:
            print('Bye!')
            user.user_disconnect()
            exit()

def main():
    main_menu()

if __name__ == '__main__':
    main()