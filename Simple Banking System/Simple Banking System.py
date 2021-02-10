#!/usr/bin/env python
# coding: utf-8

# In[10]:


import sqlite3
from random import randint

conn = sqlite3.connect('card.s3db') # creating connection object to represent db ('filename')
cur = conn.cursor() # creating Cursor object

# creating a table in our database if it doesn't exist
cur.execute('''CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT,
number TEXT, 
pin TEXT, 
balance INTEGER DEFAULT 0)''')

# creating a card number + pin 
# Luhn Algorithm applied to generate card number
def create_account():
     # creating a random 15-digit number with a pre-defined Issuer Identification number
    account = [4,0,0,0,0,0] # Issuer Identification number is 400000
    random_num= [randint(0,9) for i in range(0,9)]
    account.extend(random_num)
    account_num_by2 = [account[i] * 2 if i % 2 == 0 else account[i] for i in range(len(account))]
    account_num_minus9 = [num - 9 if num > 9 else num for num in account_num_by2]
    sum_of_numbers = sum(account_num_minus9) # summing numbers

    # finding the last digit(our checksum)
    # if the received number is divisible by 10 with the remainder equal to zero, then this number is valid
    last_digit = 0
    for i in range(10):
        if (sum_of_numbers + i) % 10 == 0:
            last_digit = i
    account.append(last_digit) # adding checksum

    account_str = ''.join([str(i) for i in account])
    pin = [str(randint(0,9)) for i in range(0,4)] #creating the pin 
    pin = ''.join(pin)
    
    # adding the card number and pin to the database
    cur.execute("INSERT INTO card (number,pin) VALUES (?,?)",(account_str,pin))
    conn.commit()
    print(f'''Your card has been created
    Your card number: {account_str}
    Your card PIN: {pin}\n''')
    
# checking card number to pass Luhn algorithm
def check_sum(card):  # input format string
    lst_to_check = list(card[:-1])  # taking only first 15 digits
    account_num = []  #
    account_num.extend([int(i) for i in lst_to_check])

    # applying Luhn Algorithm to check the number and produce a check sum
    # multiply every odd digits by 2
    account_num_by2 = [account_num[i] * 2 if i % 2 == 0 else account_num[i] for i in range(len(account_num))]
    # subtract 9 to numbers over 9
    account_num_minus9 = [num - 9 if num > 9 else num for num in account_num_by2]
    # summing numbers
    sum_of_numbers = sum(account_num_minus9)

    # finding the last digit(our checksum)
    # if the received number is divisible by 10 with the remainder equal to zero, then this number is valid
    last_digit = 0
    for i in range(10):
        if (sum_of_numbers + i) % 10 == 0:
            last_digit = i
    account_num.append(last_digit)
    account_num_str = ''.join([str(i) for i in account_num])

    if account_num_str != card:  # evaluating entered card number and the one should be according to Luhn algo
        return 0

# Checking the input data with data in database
def log_in():
    print('Enter your card number:')
    log_account = input()
    print('Enter your PIN:')
    log_password = input()
    
    # Fetching the card number and pin from the database
    cur.execute("SELECT number, pin  FROM card WHERE number=?", (log_account,))
    records = cur.fetchall()
    conn.commit()
    print('')
    if records == []: #empty records
        print('Wrong card number or PIN!\n')
    else:
        if log_account == records[0][0] and log_password == records[0][1]:
            print('You have successfully logged in!\n')
            AccountManagement(log_account)
        else:
            print('Wrong card number or PIN!\n')

# Menu
def start():
    global balance_logout
    balance_logout = 1
    while True:
        print("1. Create an account \n2. Log into account \n0. Exit""")
        
        choice = int(input())
        print('')
        if choice == 1:  # Create card number  
            create_account()
        elif choice == 2: # Log in 
            log_in()
        elif choice == 0: # Exit
            break
        if balance_logout == 0:
            break

def AccountManagement(log_account):
    while True:
        global balance_logout
        print('''1. Balance \n2. Add income \n3. Do transfer \n4. Close account \n5. Log out \n0. Exit''')
        balance_logout = int(input())
        print('')
        if balance_logout == 1: # Check balance
            cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
            balance = cur.fetchone()[0]
            conn.commit()
            print(f'Balance: {balance}\n')
        if balance_logout == 2: # Adding income 
            add_income(log_account)
        if balance_logout == 3: # Transferring the amount
            Transference(log_account)
        if balance_logout == 4: # Closing the account
            CloseAccount(log_account)
            break
        if balance_logout == 5: #Logout
            print('\nYou have successfully logged out!\n')
            break
        if balance_logout == 0:
            break


def add_income(log_account):
    print('Enter income:')
    income = int(input())
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    new_balance = (cur.fetchall()[0][0]) + income
    cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance, log_account,))
    conn.commit()
    print('Income was added!\n')


def Transference(log_account):
    print("\n Transfer")
    print("Enter card number of transferree:")
    transfer_account = input()
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    balance = (cur.fetchall())[0][0]
    if log_account == transfer_account:
        print("You can't transfer money to the same account!")
    elif check_sum(transfer_account) == 0:
        print("Probably you made mistake in the card number. Please try again!\n")
    else:
        cur.execute("SELECT number FROM card") 
        accounts = (cur.fetchall())
        accounts = [i[0] for i in accounts] # fetching all the card number from the database
        if transfer_account not in accounts: # checking for card number existency
            print("Such a card does not exist.")
        else:
            print("Enter how much money you want to transfer:")
            transfer_money = int(input())
            if (balance - transfer_money) <= 0:
                print('Not enough money!')
            else:
                new_balance = balance - transfer_money
                cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance, log_account,))
                conn.commit()
                cur.execute("SELECT balance FROM card WHERE number=?", (transfer_account,))
                new_balance2 = (cur.fetchall())[0][0] + transfer_money
                cur.execute("UPDATE card SET balance = ? WHERE number=?", (new_balance2, transfer_account,))
                conn.commit()
                print('Success!\n')
                
# Closing the account
def CloseAccount(log_account):
    cur.execute("SELECT balance FROM card WHERE number=?", (log_account,))
    cur.execute("DELETE FROM card WHERE number=?", (log_account,))
    conn.commit()
    print('The account has been closed!\n')


start()
print('Bye!!')


# In[ ]:




