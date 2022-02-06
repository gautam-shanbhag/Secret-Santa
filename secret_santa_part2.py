import re
import random
import ast



def append_value(dict_obj, key, value):
    # Check if key exist in dict or not
    if key in dict_obj:
        # Key exist in dict.
        # Check if type of value of key is list or not
        if not isinstance(dict_obj[key], list):
            # If type is not list then make it list
            dict_obj[key] = [dict_obj[key]]
        # Append the value in list
        dict_obj[key].append(value)
    else:
        # As key is not in dict,
        # so, add key-value pair
        dict_obj[key] = value


sender_address = 'email'
sender_pass = 'password'

names = []
emails = []
recipient = []
budget = 50

count = 0

print("""Welcome to the secret santa decision-maker!
How would you like to enter the information?
     1. give a text (.txt) file with format of:
         name, email address
     2. manually enter information""")

# info entry method choice
x = 0
while (x == 0):
    try:
        option = int(input("Info entry method (1 or 2): "))
        if (option > 2 or option < 1):
            print("ERROR: You can only input 1 or 2!")
            print("""How would you like to enter the information?
                  1. give a text (.txt) file
                  2. manually enter information""")
        else:
            x = 1
    except ValueError:
        print("ERROR: Please input 1 or 2!")
        print("""How would you like to enter the information?
        1. give a text (.txt) file
        2. manually enter information""")

# number of participants
x = 0
while (x == 0):
    try:
        count = int(input("Enter number of participants: "))
        if (count < 2):
            print("ERROR: Number of participants must be 2 or more!")
        else:
            x = 1
    except ValueError:
        print("ERROR: Please input a valid integer number!")

# option 1: read the file (assumes file format is correct)
if (option == 1):
    x = 0
    while (x == 0):
        filename = str(input("Name of text file (must end in .txt): "))
        if (filename[-4:] == '.txt'):
            x = 1
        else:
            print("ERROR: Please input a file name which ends with .txt")
    text = open(filename, "r")
    for i in range(0, count):
        info = text.readline().split(', ')
        names.append(info[0])
        emails.append(info[1])
    text.close()
# option 2: manually get info
elif (option == 2):

    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'

    print("Ok! It's time for you to input the participants' information!")
    for i in range(1, count + 1):
        name = str(input(f'Enter participant the name of participant {i}: '))
        names.append(name)
        x = 0
        while (x == 0):
            email = str(input(f'Enter the email of participant {i}: '))
            if (re.search(regex, email)):
                emails.append(email)
                x = 1
            else:
                print("ERROR: invalid email!")

possible_santa = names.copy()


filename = "SantaHistory.txt"
mapExists = False
try:
    text = open(filename, "r")
    info = text.read()
    map = ast.literal_eval(info)
    text.close()
    print(map)
    if bool(map):
        mapExists = True
except :
    print("File does not exist !")


cont = 0

while (cont == 0):

    redo = False
    possible_santa = names.copy()

    for i in range(0, len(names)):
        recip = random.randint(0, len(possible_santa) - 1)
        x = 0
        while (x == 0):
            if (names[i] == possible_santa[recip] or (mapExists and possible_santa[recip] in map [names[i]])):
                if (len(possible_santa) == 1):
                    redo = True
                    x = 1
                else:
                    recip = random.randint(0, len(possible_santa) - 1)
            else:
                x = 1
        if (redo != True):
            recipient.append(possible_santa[recip])
            possible_santa.pop(recip)
            cont = 1
        else:
            cont = 0

# Sending the emails to the participants

import smtplib

import random

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# this code must run for each name
# for i in range(0, count):
#     # the message which will be sent in the email
#     mail_content = f'''Hello {names[i]},
#
# You are the secret santa of {recipient[i]}!
#
# Remember the budget is ${budget}
#     '''
#
#     # sets the email address the email will be sent to
#     receiver_address = emails[i]
#
#     # sets up the MIME2
#     message = MIMEMultipart()
#     message['From'] = sender_address  # your email address
#     message['To'] = receiver_address  # Secret Santa's email address
#     message['Subject'] = 'Secret Santa'  # subject of the
#
#     # sets the body of the mail
#     message.attach(MIMEText(mail_content, 'plain'))
#
#     # creates the SMTP session for sending the mail
#     session = smtplib.SMTP('smtp.gmail.com', 587)
#     session.connect("smtp.gmail.com", 587)
#     session.ehlo()
#     session.starttls()
#     session.login(sender_address, sender_pass)
#     text = message.as_string()
#     session.sendmail(sender_address, receiver_address, text)
#     session.quit()

allocations = open("SantaAllocations.txt", "w+")
history = open("SantaHistory.txt", "w+")
map_temp={}
for i in range(0, len(names)):
    print(f'\n\n{names[i]} is the secret santa of {recipient[i]}\n')

    allocations.write(f'{names[i]} is the secret santa of {recipient[i]}\n')
    if mapExists:
        for key, val in map.items():
            if names[i] == key:
                if isinstance(map[key], list) and len(map[key]) == 3:
                    del (map[key][0])
                append_value(map, key, recipient[i])
    else:
        map_temp[names[i]] = recipient[i]

if mapExists:
    history.write(str(map))
else:
    history.write(str(map_temp))
history.close
allocations.close()