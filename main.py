
# ? What's in this? contains the main execution of the program
# * Import statements
from estab_page import *                            # ? Test import for estab_page.py. Simply remove this as its functions are not needed immediately in Section 1
import mdb_connector as mdbc
# TODO: group functions by purpose (in separate files) then import them here



# functions --------
# ? DB Functions
def get_data(username):
    try:
        # ? Changed to access user table from locally created projectdb
        statement = "SELECT username, password FROM user WHERE username=%s"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        for(username, password) in mdbc.cursor:
            # print(f"Successfully retrieved {ename}, {job}")
            # print("Successfully retrieved!")
            # return found info
            return username, password
        # return not found
        return 0 
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def addToUserTable(signup_tuple):
    
    username = signup_tuple[0]
    name = signup_tuple[1]
    email = signup_tuple[2]
    password = signup_tuple[3]

    try:
        statement = "INSERT INTO user (username, name, email, password) VALUES (%s, %s, %s, %s)"
        data = (username, name, email, password)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()
        print("Successfully signed you up!")
        return 1
    except mdbc.database.Error as e:
        print(f"Error signing up: {e}")
        return 0


# --- Login functions ---
def login():
    print("\n")
    print(" Log in  ")
    
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    return username, password


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


# Others
def mainOuterMenu():
    print("\n")
    print("Choose an action")
    print("[1] Login")
    print("[2] Sign Up")
    print("[0] Exit")

    choice = int(input("I want to... "))

    return choice





# * Main Loop
# * 1. Login / Sign up
while True:
    userchoice = mainOuterMenu()

    if userchoice == 1:
        # print login screen
        data = login()
        # verify login details from database
        loginsuccessFlag = verifyLogin(data[0], data[1])

        if(loginsuccessFlag == 1):
            print("Login success!")
            print("\n")
            foodEstablishmentPage()                             # ? Testing purposes of Section 3. Section 2 should be called here instead. Please comment out
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
        mdbc.connection.close()
        break


    else:
        # Catches other int inputs
        print("Invalid choice. Please try again.")

    

