# username = os.environ.get("username")
# password = os.environ.get("password")

# connection = database.connect(
#     user=username,                                        # Uses root user
#     password=password,                                     # ! Change this to your password
#     host="127.0.0.1",
#     database="cmsc127project"                                # ! Change this to the name of project database you use
# )

def userMenu():
    print("\n")
    print("Choose an action")
    print("[1] Search for a Food Establishment")
    print("[2] View Food Establishments")
    print("[3] View filtered food establishments by high average rating")
    print("[4] Search a food item  (from any establishment) by price range AND/OR food type")
    print("[0] Exit")

    choice = int(input("I want to... "))

    return choice


def getFoodEstabId(name):
        print("\n")
        try:
            statement = "SELECT establishmentId from foodestablishment WHERE name=%s"
            data = (name,)
            cursor.execute(statement, data)
            for(establishmentId) in cursor:
                # print(f"{establishmentId} - {name} - {location}")
                return establishmentId
                # loop = 0
                #successful
            print(name + " not found!")
            return 0

        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")

def searchFoodEstab():
        print("\n")
        try:
            name = input("Which establishment do you want to view?: ")
            result = getFoodEstabId(name)
            return result

        except database.Error as e:
            print(f"Error retrieving entry from database: {e}")

def viewAllFoodEstab():
    try:
        print("***** View Food Establishments ******")
        statement = "SELECT * from foodestablishment;"
        cursor.execute(statement)
        for(establishmentId, name, location) in cursor:
            print(f"[{establishmentId}] {name} - {location}")
        choice = input("Which establishment do you want to view?: ")
        result = getFoodEstabId(choice)
        if result != 0:
            return result
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def viewByHighRating():
    try:
        print("***** View Food Establishments By High Rating ******")
        statement = "SELECT fe.establishmentId, name, location, AVG(rating) FROM foodestablishment fe JOIN review r on fe.establishmentId= r.establishmentId GROUP BY fe.establishmentId HAVING AVG(rating) >= 4"
        cursor.execute(statement)
        for(establishmentId, name, location, rating) in cursor:
            print(f"[{establishmentId}] {name} - {location} - {rating} ")
        choice = input("Which establishment do you want to view?: ")
        result = getFoodEstabId(choice)
        if result != 0:
            return result
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")

def searchFoodItem():
    try:
        print("\n")
        print("***** Search Food Items By Fields ******")
        print("How do you want to search?")
        print("[1] Search by price range")
        print("[2] Search by food type")

        searchChoice = int(input("I want to... "))

        if searchChoice == 1:
            print("\n")
            print("***** Search Food Items By Price Range ******")
            #Gets ranges
            lowRange = input("Input lowest price of price range: ")
            highRange = input("Input highest price of price range: ")
            #Executes search
            statement = "SELECT * FROM fooditem WHERE price BETWEEN %s AND %s"
            data = (lowRange, highRange,)
            cursor.execute(statement, data)
            for(itemId, name, price, description, establishmentId) in cursor:
                print(f"[{itemId}] {name} - {price} - {description} - {establishmentId}")

        elif searchChoice == 2:
            print("\n")
            print("***** Search Food Items By Food Type ******")
            #Displays options for foodtype
            print("- FOOD TYPES -")
            statement = "SELECT * from foodtype"
            cursor.execute(statement)
            for(foodtypeId, foodType) in cursor:
                print(f"[{foodtypeId}] {foodType}")
            searchChoice = int(input(("Which food type would you like to search? ")))
            print("\n")
            
            #Executes search
            statement = "SELECT * from fooditem WHERE itemid in (SELECT itemid from fooditemtype WHERE foodtypeId = %s)"
            data = (searchChoice,)
            cursor.execute(statement, data)
            for(itemId, name, price, description, establishmentId) in cursor:
                print(f"[{itemId}] {name} - {price} - {description} - {establishmentId}")

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        
def userActionsLoop():
    while True:
        userMenuChoice = userMenu()

        if userMenuChoice == 1:
            #result =
            print(searchFoodEstab())
        elif userMenuChoice == 2:
            #result =
            print(viewAllFoodEstab())
        elif userMenuChoice == 3:
            #result =
            print(viewByHighRating())
        elif userMenuChoice == 4:
            #result =
            searchFoodItem()
        elif userMenuChoice == 0:
            break
        else:
            print("Option does not exist. Please try again!")