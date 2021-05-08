from class_User import User
import class_Bank
import sqlite3

def main_menu():
    user = User()
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_choice = int(input('>'))
        if user_choice == 1:
            user.create_account()
        elif user_choice == 2:
            user.log_into_account()
        elif user_choice == 0:
            print('Bye!')
            user.user_disconnect()
            exit()

def main():
    main_menu()

if __name__ == '__main__':
    main()