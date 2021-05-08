import sqlite3

def show_table():
    conn = sqlite3.connect('card.s3db')
    cur = conn.cursor()
    for row in cur.execute("""SELECT * FROM card"""):
        print(row)

def test_str_to_list():
    line = '3123124124124'
    list_digits = list(line)
    print(list_digits)

def main():
    # test_str_to_list()
    show_table()

if __name__ == '__main__':
    main()