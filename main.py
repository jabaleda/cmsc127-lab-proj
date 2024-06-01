
# * Import statements
import os
import mysql.connector as database

# ? What's in this? contains the main execution of the program

# connect to database
connection = database.connect(
    user="root",
    password="poi",
    host="127.0.0.1",
    database="scott"                                # ! Change this to the name of project database you use
)

# instantiate cursor
cursor = connection.cursor()

# functions --------
def mainOuterMenu():
    print("\n")
    print("Choose an action")
    print("[1] Login")
    print("[2] Sign Up")
    print("[0] Exit")

    choice = int(input("I want to... "))

    return choice


def login():
    print("\n")
    print(" Log in  ")
    
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    return username, password


def signup():
    print("\n")
    print("You're one step closer")
    print(" Sign Up ")
    
    name = input("Enter name: ")
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    return name, email, username , password


def get_data(ename):
    try:
        # ? I used the scott database for testing 
        # ? ename as username and job as password 
        statement = "SELECT ename, job FROM emp WHERE ename=%s"
        data = (ename,)
        cursor.execute(statement, data)
        for(ename, job) in cursor:
            print(f"Successfully retrieved {ename}, {job}")
            # return found info
            return ename, job
        # return not found
        return 0 
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def verifyLogin(username, password):
    # get login details from db
    correctdetails = get_data(username)

    if (correctdetails == 0):
        # no user found with that username
        return 0
    else:
        # check if passwords match
        if(password == correctdetails[1]):
            return 1
        else:
            return 0




# * Main Loop

while True:
    userchoice = mainOuterMenu()

    if userchoice == 1:
        # * print login screen
        data = login()
        # * verify login details from database
        successFlag = verifyLogin(data[0], data[1])

        if(successFlag == 1):
            print("Login success!")
            # proceed to next view
        else:
            print("Error! Invalid username or password")
        
    elif userchoice == 2:
        # * print sign in screen
        signup_details = signup()
        # * add the user credentials to database
        
    
    elif userchoice == 0:
        print("Goodbye!")
        connection.close()
        break

    

