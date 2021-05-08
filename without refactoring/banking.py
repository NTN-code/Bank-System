from random import randint
import sqlite3

class Bank_user:
    conn = sqlite3.connect("card.s3db")
    cur = conn.cursor()
    try:
        cur.execute("""
            CREATE TABLE card(
             id integer PRIMARY KEY AUTOINCREMENT,
             number text,
             pin text,
             balance integer  default 0
            );
        """)
    except :
        pass

    def __init__(self):
        card_number = '400000' + str(randint(1000000000, 9999999999))
        card_number = self.get_check_luna(card_number)
        PIN = randint(1000, 10000)
        Bank_user.cur.execute("INSERT INTO card(number,pin,balance) VALUES (?,?,?)", (card_number,PIN,0))
        Bank_user.conn.commit()
        print('Your card has been created')
        print(f'Your card number:\n{card_number}')
        self.card_number = str(card_number)
        print(f'Your card PIN:\n{PIN}')
        self.PIN = str(PIN)
        self.balance = 0

    def get_check_luna(self, card_number):
        save_num = list(card_number)
        lst = list(card_number)
        lst = lst[:-1]
        for i in range(len(lst)):
            lst[i] = int(lst[i])
            if i % 2 == 0:
                digit = lst[i] * 2
                lst[i] = digit
                if digit > 9:
                    lst1 = list(str(digit))
                    lst[i] = int(lst1[0]) + int(lst1[1])
        last_digit = 10 - sum(lst) % 10
        if last_digit == 10:
            lst.append(0)
        else:
            lst.append(last_digit)
        save_num[-1] = str(lst[-1])

        card_number = ''.join(save_num)
        return card_number

    def check_balance(self):
        Bank_user.cur.execute("""SELECT balance FROM card where number =?""",[self.card_number])
        balance = int(Bank_user.cur.fetchone()[0])
        self.balance = balance
        print(f"Balance: {self.balance}")

    def db_card_log(self):
        Bank_user.cur.execute("""SELECT number FROM card WHERE number = ?""",[self.card_number])
        card_number = Bank_user.cur.fetchone()
        Bank_user.cur.execute("""SELECT pin FROM card WHERE pin= ?""",[self.PIN])
        check_pin = Bank_user.cur.fetchone()
        if check_pin == None:
            return False
        if card_number == None:
            return False
        return True

    def add_income(self):
        print("Enter income:")
        value = int(input('>'))
        Bank_user.cur.execute("""SELECT balance FROM card where number =?""", [self.card_number])
        balance = Bank_user.cur.fetchone()[0]
        balance += value
        balance = int(balance)
        Bank_user.cur.execute("""UPDATE card SET balance=? WHERE number= ?""",[balance,self.card_number])
        Bank_user.conn.commit()
        print('Income was added!')

    def check_luna(self,card_number):
        save_num = list(card_number)
        lst = list(card_number)
        lst = lst[:-1]
        for i in range(len(lst)):
            lst[i] = int(lst[i])
            if i % 2 == 0:
                digit = lst[i] * 2
                lst[i] = digit
                if digit > 9:
                    lst1 = list(str(digit))
                    lst[i] = int(lst1[0]) + int(lst1[1])
        last_digit = 10 - sum(lst) % 10
        if last_digit == 10:
            lst.append(0)
        else:
            lst.append(last_digit)
        save_num[-1] = str(lst[-1])

        card_number_1 = ''.join(save_num)

        if card_number_1 == card_number:
            return True
        else:
            return False

    def check_db_card_log(self,card_number_1):
        Bank_user.cur.execute("""SELECT number FROM card WHERE number = ?""",[card_number_1])
        card_number = Bank_user.cur.fetchone()
        # print(card_number)
        # print(check_pin)
        if card_number == None:
            return False
        return True

    def do_transfer(self):
        print("Transfer")
        print("Enter card number:")
        card_number = input(">")
        if card_number == self.card_number:
            print("You can't transfer money to the same account!")
            return False
        if self.check_luna(card_number) == False:
            print('Probably you made a mistake in the card number. Please try again!')
            return False
        if self.check_db_card_log(card_number_1=card_number) == False:
            print('Such a card does not exist.')
            return False

        print('Enter how much money you want to transfer:')
        money = int(input('>'))
        Bank_user.cur.execute("""SELECT balance FROM card where number =?""",[self.card_number])
        balance_1 = Bank_user.cur.fetchone()[0]
        if balance_1 < money:
            print("Not enough money!")
            return False
        else:
            balance_1 -= money
            Bank_user.cur.execute(""" UPDATE card SET balance=? where number=?""",[balance_1,self.card_number])
            Bank_user.conn.commit()
            Bank_user.cur.execute("""SELECT balance FROM card where number =?""",[card_number])
            balance_card = int(Bank_user.cur.fetchone()[0])
            balance_card += money
            Bank_user.conn.commit()
            Bank_user.cur.execute(""" UPDATE card SET balance=? where number=?""",[balance_card,card_number])
            Bank_user.conn.commit()
            print('Success!')

    def close_account(self):
        Bank_user.cur.execute("""DELETE FROM card  where number = ?""",[self.card_number])
        Bank_user.conn.commit()
        print('The account has been closed!')

    def log_into_account(self):
        print('Enter your card number:')
        verify_card_number = input('>')
        self.card_number = verify_card_number
        print('Enter your PIN:')
        verify_card_PIN = input('>')
        self.PIN = verify_card_PIN
        if self.db_card_log():
            print('You have successfully logged in!')
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
                    break
                elif user_choice == 0:
                    exit()
        else:
            print('Wrong card number or PIN!')


def main():
    bank_user = ''
    while True:
        print("1. Create an account")
        print("2. Log into account")
        print("0. Exit")
        user_choice = int(input('>'))
        if user_choice == 1:
            bank_user = Bank_user()
        elif user_choice == 2:
            if bank_user:
                bank_user.log_into_account()
            else:
                bank_user = Bank_user()
                bank_user.log_into_account()
        elif user_choice == 0:
            print('Bye!')
            Bank_user.conn.close()
            exit()


if __name__ == '__main__':
    main()

