
# * Import statements
import os
import mysql.connector as database

# ? What's in this? contains the main execution of the program

# connect to database
connection = database.connect(
    user="root",                                        # Uses root user
    password="poi",                                     # ! Change this to your password
    host="127.0.0.1",
    database="projectdb"                                # ! Change this to the name of project database you use
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

# --- Login functions ---
def login():
    print("\n")
    print(" Log in  ")
    
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    return username, password


def get_data(username):
    try:
        # ? Changed to access user table from locally created projectdb
        statement = "SELECT username, password FROM user WHERE username=%s"
        data = (username,)
        cursor.execute(statement, data)
        for(username, password) in cursor:
            # print(f"Successfully retrieved {ename}, {job}")
            print("Successfully retrieved!")
            # return found info
            return username, password
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
        
# --- Sign up functions ---
def signup():
    print("\n")
    print("You're one step closer")
    print(" Sign Up ")
    
    name = input("Enter name: ")
    email = input("Enter email: ")
    username = input("Enter username: ")
    password = input("Enter password: ")

    return username, name, email, password


def addToUserTable(signup_tuple):
    
    username = signup_tuple[0]
    name = signup_tuple[1]
    email = signup_tuple[2]
    password = signup_tuple[3]

    try:
        statement = "INSERT INTO user (username, name, email, password) VALUES (%s, %s, %s, %s)"
        data = (username, name, email, password)
        cursor.execute(statement, data)
        connection.commit()
        print("Successfully signed you up!")
        return 1
    except database.Error as e:
        print(f"Error signing up: {e}")
        return 0



# * Main Loop
while True:
    userchoice = mainOuterMenu()

    if userchoice == 1:
        # print login screen
        data = login()
        # verify login details from database
        loginsuccessFlag = verifyLogin(data[0], data[1])

        if(loginsuccessFlag == 1):
            print("Login success!")
            # proceed to next view
        else:
            print("Error! Invalid username or password")
        
        
    elif userchoice == 2:
        # TODO: Add input validation
        # print sign in screen
        signup_details = signup()
        # add the user credentials to database
        signupsuccessFlag = addToUserTable(signup_details)

        if(signupsuccessFlag == 1):
            print("Please log in to continue")
        else:
            print("An error ocurred. Please try again")

        
    elif userchoice == 0:
        print("Goodbye!")
        connection.close()
        break


    else:
        # Catches other int inputs
        print("Invalid choice. Please try again.")

    

