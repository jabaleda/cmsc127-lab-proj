# * Import statements
import mdb_connector as mdbc
from customerActions import userActionsLoop
from adminActions import adminActionsLoop

# functions --------
def mainOuterMenu():
    print("\n")
    print("Welcome to SwiftBites! It's been waitin' for you")
    print("")
    print("Choose an action to start Taylor's Taste Tour!")
    print("[You Belong With Me] -   Login ")
    print("[Begin Again]    -   Sign Up")
    print("[All Too Well]   -   Exit")

    while True:
        try:
            choice = str(input("I want to... "))
            return choice
        except ValueError:
            print("Invalid input! Please enter a number.")

# --- Login functions ---
def login():
    print("\n")
    print(" Log in ")
    
    username = input("Enter username/email: ")
    password = input("Enter password: ")

    return username, password

def get_user_data(username):
    try:
        mdbc.reconnect() 
        statement = "SELECT username, password FROM user WHERE username=%s OR email=%s"
        data = (username, username)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result:
            return result
        return None
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return None

def is_admin(username):
    try:
        mdbc.reconnect()
        statement = "SELECT COUNT(*) FROM adminUser WHERE username=%s"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        count = mdbc.cursor.fetchone()[0]
        return count > 0
    except mdbc.database.Error as e:
        print(f"Error checking admin status: {e}")
        return False

def verifyLogin(username, password):
    # get login details from db
    correctdetails = get_user_data(username)
    if correctdetails is None:
        # no user found with that username
        return False
    else:
        # check if passwords match
        return password == correctdetails[1]

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
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()
        print("Successfully signed you up!")
        return True
    except mdbc.database.Error as e:
        print(f"Error signing up: {e}")
        return False

# * Main Loop
while True:
    userchoice = mainOuterMenu()

    if userchoice == 'You Belong With Me':
        # print login screen
        data = login()
        # verify login details from database
        loginsuccessFlag = verifyLogin(data[0], data[1])

        if loginsuccessFlag:
            print("Login success!")
            username = data[0]
            if is_admin(username):
                adminActionsLoop()
            else:
                userActionsLoop(username)
        else:
            print("Error! Invalid credentials")
            print("Now we got problems And I don't think we can solve 'em")

    elif userchoice == 'Begin Again':
        # To do: Add input validation
        # print sign in screen
        signup_details = signup()
        # add the user credentials to database
        signupsuccessFlag = addToUserTable(signup_details)

        if signupsuccessFlag:
            print("Please log in to continue")
        else:
            print("Please try again 'This Love'")

    elif userchoice == 'All Too Well':
        print("")
        print("And I remember it All Too Well... Goodbye...")
        mdbc.connection.close()
        break

    else:
        # Catches other int inputs
        print("Invalid choice. Please try again. 'I Knew You Were Trouble'")

mdbc.connection.close()
