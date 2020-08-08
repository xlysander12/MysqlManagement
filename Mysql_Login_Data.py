import argparse
import sys

import mysql.connector as mysql
from tabulate import tabulate
import pyautogui
import tkinter as tk
from tkinter import filedialog
from xlsxwriter.workbook import Workbook
import os.path
from os import path

# Create execution arguments
parser = argparse.ArgumentParser(description="Mysql hacking data reader and writer")
parser.add_argument('-r', '--retrieve', help="Retrieves data", action="store_true")
parser.add_argument('-u', '--upload', help="Uploads data", action="store_true")
parser.add_argument('-d', '--delete', help="Deletes entries in the database", action="store_true")
parser.add_argument('-a', '--add', help="Adds data manually in database", action="store_true")
parser.add_argument('-g', '--gui', help="Opens GUI", action="store_true")
parser.add_argument('-e', '--export', help="Opens GUI", action="store_true")


# Created --------------------------


# Creating function to create mysql.cfg file
def createmysqlconfig(host, user, password, database):
    with open('mysql.cfg', 'w') as conf:
        conf.write("Host: " + host + "\n")
        conf.write("User: " + user + "\n")
        conf.write("Password: " + password + "\n")
        conf.write("Database: " + database)
        conf.close()


# Created -----------------------------------


# Checking if there is a present "mysql.cfg"
if not path.exists('mysql.cfg'):
    print("There isn't any 'mysql.cfg' file in directory. Creating one to connect to mysql")
    host = input("Host of DB: ")
    user = input("User to log in: ")
    password = input("Password to authenticate with " + user + ": ")
    database = input("Database name to connect to: ")
    createmysqlconfig(host, user, password, database)

# Checked and created if didn't exist -------------------------

# Initializing mysql variables
dbHost = ""
dbUser = ""
dbPass = ""
dbDB = ""

# Creating MySQL connection variables
with open('mysql.cfg') as f:
    for line in f:
        foundDbIP = line.find('Host:')
        foundDbUser = line.find('User:')
        foundDbPass = line.find('Password:')
        foundDB = line.find('Database:')
        if foundDbIP != -1:
            dbHost = line.split(": ")
        if foundDbUser != -1:
            dbUser = line.split(": ")
        if foundDB != -1:
            dbDB = line.split(": ")
        if foundDbPass != -1:
            dbPass = line.split(": ")
        elif foundDbPass == -1:
            dbPass = ""
# Created ---------------------------------


# Connect to database
try:
    check = dbPass[1]
    dbPass = check
except IndexError:
    dbPass = ""
try:
    mydb = mysql.connect(
        host=dbHost[1],
        user=dbUser[1],
        password=dbPass,
        database=dbDB[1]
    )
except mysql.Error:
    sys.exit("Couldn't connect to the database")

mycursor = mydb.cursor()

# Connected

# Create main GUI instance
# main = tk.Tk()


# Created --------------


# Creating function to retrieve
def retrieve(id="", website=""):  # Function to retrieve data from the sql server
    if id == "" and website == "":  # Fetch Everything in database
        sqlcommand = "SELECT * FROM login_data"
        mycursor.execute(sqlcommand)
        myresult = mycursor.fetchall()
        if not myresult:
            print("Não foram encontrados resultados!")
            sys.exit()
        else:
            print(tabulate(myresult, headers=['ID', 'URL', 'User', 'Password'], tablefmt="psql"))
            sys.exit()
    elif id == "" and website != "":  # Fetch every entry with specified website in database
        website_like = "%" + website + "%"
        sqlcommand = "SELECT * FROM login_data WHERE URL LIKE %s"
        args = (website_like,)
        mycursor.execute(sqlcommand, args)
        myresult = mycursor.fetchall()
        if not myresult:
            print("Não foram encontrados resultados!")
            sys.exit()
        else:
            print(tabulate(myresult, headers=['ID', 'URL', 'User', 'Password'], tablefmt="psql"))
            sys.exit()
    elif id != "" and website == "":  # Fecth every entry with specified id in databse
        sqlcommand = "SELECT * FROM login_data WHERE Id = %s"
        args = (id,)
        mycursor.execute(sqlcommand, args)
        myresult = mycursor.fetchall()
        if not myresult:
            print("Não foram encontrados resultados!")
            sys.exit()
        else:
            print(tabulate(myresult, headers=['ID', 'URL', 'User', 'Password'], tablefmt="psql"))
            sys.exit()
    else:  # Fetch every entry with specified id and website in database
        sqlcommand = "SELECT * FROM login_data WHERE Id = %s AND URL LIKE %s"
        website_like = "%" + website + "%"
        args = (id, website_like)
        mycursor.execute(sqlcommand, args)
        myresult = mycursor.fetchall()
        if not myresult:
            print("Não foram encontrados resultados!")
            sys.exit()
        else:
            print(tabulate(myresult, headers=['ID', 'URL', 'User', 'Password'], tablefmt="psql"))
            sys.exit()


# Function to retrieve data created ----------------------------------

# Creating function to export to file
def export(file, id="", website=""):
    if file:
        if not file.__contains__(".xlsx"):
            file = file + ".xlsx"
        workbook = Workbook(file)
        sheet = workbook.add_worksheet("Login Data")
        if not id and not website:
            sqlcommand = "SELECT * FROM login_data"
            mycursor.execute(sqlcommand)
            result = mycursor.fetchall()
            with open(file, 'w') as f:
                for r, row in enumerate(result):
                    for c, col in enumerate(row):
                        sheet.write(r, c, col)
                workbook.close()
        if not id and website:
            sqlcommand = "SELECT * FROM login_data WHERE URL LIKE %s"
            website_like = "%" + website + "%"
            vals = (website_like,)
            mycursor.execute(sqlcommand, vals)
            result = mycursor.fetchall()
            with open(file, 'w') as f:
                for r, row in enumerate(result):
                    for c, col in enumerate(row):
                        sheet.write(r, c, col)
                workbook.close()
        if id and not website:
            sqlcommand = "SELECT * FROM login_data WHERE Id = %s"
            vals = (id,)
            mycursor.execute(sqlcommand, vals)
            result = mycursor.fetchall()
            with open(file, 'w') as f:
                for r, row in enumerate(result):
                    for c, col in enumerate(row):
                        sheet.write(r, c, col)
                workbook.close()
        if id and website:
            sqlcommand = "SELECT * FROM login_data WHERE Id = %s AND URL LIKE %s"
            website_like = "%" + website + "%"
            vals = (id, website_like)
            mycursor.execute(sqlcommand, vals)
            result = mycursor.fetchall()
            with open(file, 'w') as f:
                for r, row in enumerate(result):
                    for c, col in enumerate(row):
                        sheet.write(r, c, col)
                workbook.close()
    else:
        sys.exit("No file specified")


# Creating function to upload
def upload(id, file):
    url = None
    user = None
    password = None
    with open(file) as f:
        for line in f:
            foundUrl = line.find('URL:')
            foundUser = line.find('Login:')
            foundPass = line.find('Password:')
            if foundUrl != -1:
                url = line.split(": ")
                print(url[1])
            if foundUser != -1:
                user = line.split(": ")
                print(user[1])
            if foundPass != -1:
                password = line.split(": ")
                print(password[1])
            if url is not None and user is not None and password is not None:
                sqlcommand = "INSERT INTO login_data(Id, URL, User, Password) VALUES (%s, %s, %s, %s)"
                vals = (id, url[1], user[1], password[1])
                mycursor.execute(sqlcommand, vals)
                mydb.commit()
                print("URL '" + url[1] + "' adicionado com sucesso")
                url = None
                user = None
                password = None
        print("Ficheiro importado com sucesso")


# Function created ------------------------------------------------------

# Create function to delete entries
def delete(id):
    if not id:
        sys.exit("No id specified")
    else:
        sqlcommand = "DELETE FROM login_data WHERE Id = %s"
        vals = (id,)
        mycursor.execute(sqlcommand, vals)
        mydb.commit()
        print("Registos apagados com sucesso")


# Function created -------------------------------------------------------

# Create function to add entries manually
def add(id, url, username, password):
    sqlcommand = "INSERT INTO login_data(Id, URL, User, Password) VALUES (%s, %s, %s, %s)"
    vals = (id, url, username, password)
    mycursor.execute(sqlcommand, vals)
    mydb.commit()
    print("Registo adicionado com sucesso")


# Create function to open main GUI window
"""def maingui():
    canvasmain = tk.Canvas(main, width=300, height=300)
    canvasmain.pack()
    logindataButton = tk.Button(text='Login Data', command=logindatagui, bg='red', fg='white', font=10)
    canvasmain.create_window(150, 150, window=logindataButton)
    main.mainloop()"""


# Created ------------------------

# Create function to open logindata GUI window
"""def logindatagui():
    main.destroy()
    logindata = tk.Tk()
    canvaslogindata = tk.Canvas(logindata, width=300, height=300)
    canvaslogindata.pack()
    retrievedataButton = tk.Button(text='Retrieve Data', command=None, bg='green', fg='white', font=10)
    retrievedataButton.pack()
    uploaddataButton = tk.Button(text='Upload Data', command=None, bg='green', fg='white', font=10)
    uploaddataButton.pack()
    deletedataButton = tk.Button(text='Delete Data', command=None, bg='green', fg='white', font=10)
    deletedataButton.pack()
    canvaslogindata.create_window(150, 150, window=retrievedataButton)
    canvaslogindata.create_window(150, 150, window=uploaddataButton)
    canvaslogindata.create_window(150, 150, window=deletedataButton)
    logindata.mainloop()"""


#  Checking for options and executing accordingly
args = parser.parse_args(sys.argv[1:])
if args.retrieve:
    # Asking for user input
    id = input("Ver dados de login de (Deixar em branco para todos): ")
    website = input("Em qual website (Deixar em branco para todos): ")
    # Needed input asked -----------------------------

    # Calling retrieve function with info gave by user
    retrieve(id, website)
    # Function Called ------------------------------------
elif args.upload:
    filepath = input("Path to file: ")
    id = input("Data owner: ")
    if not id:
        sys.exit("No id specified")
    else:
        upload(id, filepath)
elif args.delete:
    id = input("De quem queres apagar os dados: ")
    delete(id)
elif args.add:
    id = input("Dono dos dados: ")
    url = input("URL: ")
    user = input("Username: ")
    password = input("Password: ")
    add(id, url, user, password)
# elif args.gui:
elif args.export:
    id = input("De quem queres exportar os dados (Deixa em branco para todos): ")
    website = input("De qual website queres os dados (Deixa em branco para todos): ")
    file = input("Caminho do ficheiro onde queres os dados exportados (.csv): ")
    export(file, id, website)
else:
    sys.exit()
# Checked and executed ---------------------------------
