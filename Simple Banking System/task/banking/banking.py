import random
import database

db = database.BankDatabase()


class CardSystem:
    def __init__(self):
        self.iin = 400000

    @staticmethod
    def menu1():
        print('''
        1. Create an account
        2. Log into account
        0. Exit''')

    def menu2(self, user_card):
        print("""
                1. Balance
                2. Add income
                3. Do transfer
                4. Close account
                5. Log out
                0. Exit""")

        user_opt = int(input())

        if user_opt == 1:
            balance = db.balance(user_card)
            print('Balance:', balance)

        elif user_opt == 2:
            income = int(input())
            db.add_income(user_card, income)
            print('Income was added!')
            self.menu2(user_card)

        elif user_opt == 3:
            print('Transfer')
            acc_num = input('Enter card number:')
            check_sum = acc_num[-1]
            checksum = str(self.luhn(acc_num[:-1]))

            if check_sum == checksum:
                output = db.do_transfer(user_card, acc_num)
                print(output)
                self.menu2(user_card)
            else:
                print('Probably you made a mistake in the card number. Please try again!')
                self.menu2(user_card)
        elif user_opt == 4:
            db.close_account(user_card)
            print('The account has been closed!')
            self.system_on()

        elif user_opt == 5:
            self.logout()

        else:
            self.bye()

    @staticmethod
    def logout():
        print('You have successfully logged out!')

    @staticmethod
    def bye():
        print('Bye!')

    @staticmethod
    def luhn(card):
        card_num = list(card)
        card_num = [int(x) for x in card_num[::-1]]
        card_num[::2] = [x * 2 for x in card_num[::2]]
        card_num[::2] = [list(str(x)) for x in card_num[::2]]
        for i in card_num:
            if isinstance(i, list):
                idx = card_num.index(i)
                x = sum([int(each) for each in i])
                card_num[idx] = x
        summary = sum(card_num) * 9
        return summary % 10

    def create_account(self):
        print('Your card has been created')
        print('Your card number:')
        acc_num = str(db.get_acc_num())
        card = str(self.iin) + acc_num
        checksum = self.luhn(card)
        card += str(checksum)
        pin = str(random.randint(1000, 9999))
        print(card)
        print('Your card PIN:')
        print(pin)
        db.create_acc(card, pin)

    def login(self):
        print('Enter your card number:')
        user_card = input()
        print('Enter your PIN:')
        user_pin = input()
        output = db.check_acc(user_card, user_pin)
        if output == 'You have successfully logged in!':
            print(output)
            self.menu2(user_card)
        else:
            print(output)
            self.system_on()

    def system_on(self):
        while True:
            self.menu1()
            user_opt = int(input())
            if user_opt == 1:
                self.create_account()
            elif user_opt == 2:
                self.login()
                break
            else:
                self.bye()
                break


new_bank = CardSystem()
new_bank.system_on()
