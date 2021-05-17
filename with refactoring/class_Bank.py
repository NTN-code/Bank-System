from random import randint
import sqlite3


class Bank():
    conn = sqlite3.connect('card.s3db')
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
    except sqlite3.OperationalError:
        print("Table card already exists")

    @classmethod
    def create_account(cls):
        card_number = '400000' + str(randint(1000000000, 9999999999))
        card_number = cls.get_luna_card(card_number)
        pin = str(randint(1000, 10000))
        cls.add_card_to_db(card_number, pin)
        print('Your card has been created')
        print(f'Your card number:\n{card_number}')
        print(f'Your card PIN:\n{pin}')
        return card_number, pin

    @classmethod
    def add_card_to_db(cls, card_number, pin):
        cls.cur.execute("""INSERT INTO card(number,pin,balance) VALUES (?,?,?)""", (card_number, pin, 0))
        cls.conn.commit()

    @staticmethod
    def get_luna_card(card_number):
        origin_number = list(card_number)
        lst_card = list(card_number)
        lst_card = lst_card[:-1]
        for i in range(len(lst_card)):
            lst_card[i] = int(lst_card[i])
            if i % 2 == 0:
                lst_card[i] = lst_card[i] * 2
                if lst_card[i] > 9:
                    divied_digit = list(str(lst_card[i]))
                    lst_card[i] = int(divied_digit[0]) + int(divied_digit[1])

        last_digit = 10 - sum(lst_card) % 10
        if last_digit == 10:
            lst_card.append(0)
        else:
            lst_card.append(last_digit)
        origin_number[-1] = str(lst_card[-1])
        card_number = ''.join(origin_number)
        return card_number

    @classmethod
    def check_balance_from_db(cls, card_number):
        cls.cur.execute("""SELECT balance FROM card where number =?""", [card_number])
        balance = int(cls.cur.fetchone()[0])
        print(f"Balance: {balance}")
        return balance

    @classmethod
    def disconnect_to_db(cls):
        cls.conn.close()

    @classmethod
    def log_into_db(cls, card_number, pin):
        cls.cur.execute("""SELECT number FROM card WHERE number = ? and pin = ?""", [card_number, pin])
        card_number = cls.cur.fetchone()
        if card_number == None:
            return False
        return True

    @classmethod
    def add_income(cls, card_number, value):
        cls.cur.execute("""SELECT balance FROM card where number =?""", [card_number])
        balance = cls.cur.fetchone()[0]
        balance += value
        balance = int(balance)
        cls.cur.execute("""UPDATE card SET balance=? WHERE number= ?""", [balance, card_number])
        cls.conn.commit()
        print('Income was added!')
        return balance

    @classmethod
    def close_account_from_db(cls, card_number):
        cls.cur.execute("""DELETE FROM card  where number = ?""", [card_number])
        cls.conn.commit()
        print('The account has been closed!')

    @classmethod
    def check_luna(cls, card_number):
        luna_card = cls.get_luna_card(card_number)
        if luna_card == card_number:
            return True
        else:
            return False

    @classmethod
    def check_card_in_db(cls, card_number):
        cls.cur.execute("""SELECT number FROM card WHERE number = ?""", [card_number])
        card_number = cls.cur.fetchone()
        if card_number == None:
            return False
        return True

    @classmethod
    def get_balance_from_db(cls, card_number):
        cls.cur.execute("""SELECT balance FROM card where number =?""", [card_number])
        balance = cls.cur.fetchone()[0]
        return balance

    @classmethod
    def update_balance(cls, balance, card_number):
        cls.cur.execute(""" UPDATE card SET balance=? where number=?""", [balance, card_number])
        cls.conn.commit()

    @classmethod
    def show_table(cls):
        print("Table card")
        print("ID\tcard \t\t\t\t PIN\tbalance")
        for row in cls.cur.execute("""SELECT * FROM card"""):
            print(row)

    @classmethod
    def get_data_from_table_to_binary_tree(cls):
        numbers = []
        balance = []
        try:
            for row in cls.cur.execute("""SELECT number,balance FROM card"""):
                numbers.append(row[0])
                balance.append(int(row[1]))
            return numbers, balance
        except:
            return None, None

    @classmethod
    def get_data_from_table_to_heap(cls):
        numbers = []
        balance = []
        try:
            for row in cls.cur.execute("""SELECT number,balance FROM card ORDER BY balance DESC """):
                numbers.append(row[0])
                balance.append(int(row[1]))
            return numbers, balance
        except:
            return None,None
