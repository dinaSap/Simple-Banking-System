import sqlite3


class BankDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        sql = """
                        CREATE TABLE IF NOT EXISTS card 
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         number TEXT, pin TEXT, balance INTEGER DEFAULT 0)
                        """
        self.cur.execute(sql)
        self.conn.commit()

    def balance(self, acc_num):
        sql = "SELECT balance FROM card WHERE number = ?"
        self.cur.execute(sql, (acc_num,))
        self.conn.commit()
        result = self.cur.fetchall()
        if len(result) > 0:
            return result[0][0]

    def add_income(self, acc_num, income_input):
        income = self.balance(acc_num)
        income += income_input
        sql = "UPDATE card SET balance=? WHERE number=?"
        self.cur.execute(sql, (income, acc_num))
        self.conn.commit()

    def create_acc(self, card, pin):
        self.cur.execute('INSERT INTO card(number,pin) VALUES (?, ?)', (card, pin))
        self.conn.commit()

    def check_acc(self, user_card, pin):
        sql = "SELECT number, pin FROM card WHERE number = ?"
        self.cur.execute(sql, (user_card,))
        self.conn.commit()
        result = self.cur.fetchone()
        print(result)
        if result is not None:
            if result[1] == pin:
                return 'You have successfully logged in!'
            else:
                return 'Wrong card number or PIN!'
        else:
            return 'Wrong card number or PIN!'

    def get_acc_num(self):
        sql = "SELECT id FROM card ORDER BY id DESC LIMIT 1"
        self.cur.execute(sql)
        self.conn.commit()
        result = self.cur.fetchone()
        if result is not None:
            return result[0] + 1 + 100000000
        else:
            return 100000000

    def do_transfer(self, user_card, acc_num):
        sql = "SELECT number FROM card WHERE number = ?"
        self.cur.execute(sql, (acc_num,))
        self.conn.commit()
        result = self.cur.fetchone()
        print(result)
        if result is not None:
            income = int(input('Enter how much money you want to transfer'))
            balance = self.balance(user_card)
            if balance >= income:
                self.add_income(acc_num, income)
                new_amount = balance - income
                sql = "UPDATE card SET balance=? WHERE number=?"
                self.cur.execute(sql, (new_amount, user_card))
                self.conn.commit()
                return 'Success!'
            else:
                return 'Not enough money!'
        else:
            return 'Such a card does not exist.'

    def close_account(self, user_card):
        sql = "DELETE FROM card WHERE number = ?"
        self.cur.execute(sql, (user_card,))
        self.conn.commit()





