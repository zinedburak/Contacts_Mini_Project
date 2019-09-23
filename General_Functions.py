import sqlite3
from getpass import getpass


def check_id(username, password):
    con = sqlite3.connect("/home/burak/Desktop/GitHub/Contacts_Mini_Project/contactsUaP.db")
    cursor = con.cursor()
    if username == "0":
        exit()
    query = "Select PassWord From Uap Where UserName = '{}'".format(username)
    try:
        cursor.execute(query)
        rpassWord = cursor.fetchone()

        if reformat_password(str(rpassWord)) == password:
            print("Login Successful")
            return True
        elif rpassWord is None:
            print("The Username You Have Entered is Wrong")
            return False
        else:
            print("Wrong Password Try Again")

            return False
    except sqlite3.OperationalError:
        return False


# reformat the contact line for more beautiful look
def reformat(contact):
    contact = contact.replace("'", "")
    contact = contact.replace(",", ":")
    contact = contact.replace("(", "")
    contact = contact.replace(")", "")
    contact = contact.replace(" ", ":")
    return contact


# reformat the password from tuple object to raw string of password
def reformat_password(passWord):
    passWord = passWord.replace("'", "")
    passWord = passWord.replace(",", "")
    passWord = passWord.replace("(", "")
    passWord = passWord.replace(")", "")
    return passWord


# check the username and password from UaP DataBase and then if correct connect to the user's Contacts DB
def connect_contacts(userName, passWord):
    if check_id(userName, passWord):
        print("Welcome To Your Contacts {}".format(userName))
        con = sqlite3.connect("/home/burak/Desktop/GitHub/Contacts_Mini_Project/{}Contacts.db".format(userName))
        return con
    else:
        main_menu()


# Show The Contacts Of The User
def get_contacts(cursor):
    cursor.execute("Select * From Contacts")
    contacts = cursor.fetchall()
    for contact in contacts:
        print(reformat(str(contact)))


# Add a new contact to the user
def add_contacts(con, cursor):
    attributes = input("Please Enter Name,Surname,Number,Address :: ")
    attributes = attributes.split(",")
    try:
        query = "Insert into Contacts(Name,SurName,Number,Address) VALUES ('{}','{}','{}','{}')".format(
            attributes[0], attributes[1], attributes[2], attributes[3])
    except IndexError:
        print("Not Enough Data")
        exit()

    try:
        cursor.execute(query)
        print("Executed")
    except sqlite3.IntegrityError:
        print("Duplicate Data in the data base")
        exit()
    con.commit()
    print("committed")


# Search The contact by any attribute
def search_contact(attribute_name, attribute, cursor):
    if attribute_name == "name":
        query = "Select * From Contacts Where Name = '{}'".format(attribute)
        cursor.execute(query)
        search_results = cursor.fetchall()
        for search_result in search_results:
            print(reformat(str(search_result)))
    elif attribute_name == "surname":
        query = "Select * From Contacts Where SurName = '{}'".format(attribute)
        cursor.execute(query)
        search_results = cursor.fetchall()
        for search_result in search_results:
            print(reformat(str(search_result)))
    elif attribute_name == "number":
        query = "Select * From Contacts Where Number = '{}'".format(attribute)
        cursor.execute(query)
        search_results = cursor.fetchall()
        for search_result in search_results:
            print(reformat(str(search_result)))
    elif attribute_name == "address":
        query = "Select * From Contacts Where Address = '{}'".format(attribute)
        cursor.execute(query)
        search_results = cursor.fetchall()
        for search_result in search_results:
            print(reformat(str(search_result)))
    else:
        print("Wrong Parameter")


# Delete the user you want from your contacts
def delete_contacts(con, cursor):
    number = input("Please Enter the phone number you want to delete from your contacts :: ")
    query = "Delete From Contacts Where Number = {}".format(number)
    cursor.execute(query)
    print("Executed")
    con.commit()
    print("Committed")


# Login Menu For users to put their username and password
def login_menu():
    print("Hello This Is Your Personal Contact Book")
    userName = input("Username : ")
    passWord = getpass("Password : ", stream=None)
    con = connect_contacts(userName, passWord)
    cursor = con.cursor()
    return con, cursor


# Main Menu of what User Can do
def main_menu():
    con, cursor = login_menu()
    while True:
        print("Please Select What You Want To Do")
        print("1-Show Contacts")
        print("2-Add Contact")
        print("3-Return To Login")
        print("4-Delete Contact")
        print("5-Search Contact")
        print("0- Exit")
        choice = int(input("Enter Your Choice Here : "))
        if choice == 1:
            get_contacts(cursor)
            print("**************************" + "\n"
                                                 "**************************" + "\n"
                                                                                "**************************" + "\n")

        elif choice == 2:
            add_contacts(con, cursor)
            print("**************************" + "\n"
                                                 "**************************" + "\n"
                                                                                "**************************" + "\n")
        elif choice == 3:
            con, cursor = login_menu()
            print("**************************" + "\n"
                                                 "**************************" + "\n"
                                                                                "**************************" + "\n")
        elif choice == 4:
            delete_contacts(con, cursor)
            print("**************************" + "\n"
                                                 "**************************" + "\n"
                                                                                "**************************" + "\n")

        elif choice == 5:
            attribute_name = input("Please Enter Search Criteria (name,surname,number or address) : ")
            attribute = input("Please Enter the value you want to search : ")
            search_contact(attribute_name, attribute, cursor)
            print("**************************" + "\n"
                                                 "**************************" + "\n"
                                                                                "**************************" + "\n")

        elif choice == 0:
            exit()
