import mdb_connector as mdbc
from customerActions import getFoodEstabId

def getFoodItemId(foodItemName):
    try:
        statement = "SELECT itemId FROM fooditem WHERE name=%s"
        data = (foodItemName,)
        mdbc.cursor.execute(statement, data)
        foodItemId = mdbc.cursor.fetchone()
        if foodItemId:
            return foodItemId[0]
        else:
            return None
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return None
    
def addFoodEstab():
    try:
        print("\n")
        print("***** Add A Food Establishment *****")
        print("\nJust a few things...")

        name = input("Enter your establishment name (max. 30 characters): ")
        if len(name) > 30:
            print("Invalid establishment name! Exceeded 30 characters.")
            return

        location = input("Enter your establishment location (max. 30 characters): ")
        if len(location) > 30:
            print("Invalid establishment location! Exceeded 30 characters.")
            return

        statement = "INSERT INTO foodestablishment (name, location) VALUES (%s, %s)"
        data = (name, location)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()

        print("Establishment added successfully!")
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    except ValueError:
        print("Invalid input! Please enter the correct data types.")

def getFoodTypeId(foodTypeName):
    try:
        statement = "SELECT foodtypeId FROM foodtype WHERE foodType=%s"
        data = (foodTypeName,)
        mdbc.cursor.execute(statement, data)
        foodTypeId = mdbc.cursor.fetchone()
        if foodTypeId:
            return foodTypeId[0]
        else:
            # print("Establishment not found!")
            return None
        
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return None

def addFoodType(foodTypeName):
    try:
        statement = "INSERT INTO foodtype (foodType) VALUES (%s)"
        data = (foodTypeName,)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()
        # print success
    except mdbc.database.Error as e:
        print(f"Error adding entry to database: {e}")

def addtoFoodItemTypeTable(itemId, itemName, foodTypeId, foodType):
    try:
        statement = "INSERT INTO fooditemtype (itemId, name, foodtypeId, foodType) VALUES (%s, %s,%s, %s)"
        data = (itemId, itemName, foodTypeId, foodType,)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()
        # print success
    except mdbc.database.Error as e:
        print(f"Error adding entry to database: {e}")

def tagFoodItemwithType(foodItemId, foodItemName):
    while True:
        # ask to enter a food type
        foodType = input("Enter a food type for your food item: ")
        # check if food type name exists in foodtype table
        foodTypeId = getFoodTypeId(foodType)
        # if it does not exist: add to foodtype table first
        if not foodTypeId:
            addFoodType(foodType)
            # redefine foodTypeId
            foodTypeId = getFoodTypeId(foodType)
        
        # then add to fooditemtypetable
        addtoFoodItemTypeTable(foodItemId, foodItemName, foodTypeId, foodType)

        # prompt if admin wants to add another type to item
        print("\n")
        print("Add another type for your item?")
        print("[1] Yes")
        print("[2] No")

        choice = int(input("Select an action: "))

        if choice == 2:
            print("Finished adding food types. Returning...")
            break
    
    return 1

def addFoodItem():
    try:
        print("\n")
        print("***** Add A Food Item *****")

        print("\n")
        print("Just a few things...")

        while True:
            estabName = input("Input establishment name: ")
            estabId = getFoodEstabId(estabName)

            if estabId:
                # prompt for name
                foodItemName = input("Enter food item name: ")
                # prompt for price
                foodItemPrice = input("Enter food item price: ")
                # prompt for description
                foodItemDesc = input("Enter food item description: ")

                statement = "INSERT INTO fooditem (name, price, description, establishmentId) VALUES (%s, %s, %s, %s)"
                data = (foodItemName, foodItemPrice, foodItemDesc, estabId)
                mdbc.cursor.execute(statement, data)
                mdbc.connection.commit()

                # obtain id of newly inserted food item
                statement2 = "SELECT itemId FROM fooditem WHERE name=%s"
                data2 = (foodItemName,)
                mdbc.cursor.execute(statement2, data2)
                newFoodItemId = mdbc.cursor.fetchone()

                # prompt for food types
                doneFlag = tagFoodItemwithType(newFoodItemId[0], foodItemName)

                # if function returned a value, exit
                if doneFlag:
                    break
            
            else:
                print("Please try again.") 

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

def updateFoodEstab():
    try:
        print("\n")
        print("***** Update A Food Establishment *****")

        estabName = input("Input establishment name: ")
        estabId = getFoodEstabId(estabName)

        if not estabId:
            print("Establishment not found. Please try again.")
            return

        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Location")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE foodestablishment SET name=%s WHERE establishmentId=%s"
                data = (updName, estabId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 2:
                updLocation = input("New location: ")
                statement = "UPDATE foodestablishment SET location=%s WHERE establishmentId=%s"
                data = (updLocation, estabId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to update the food establishment [y/n]? ")
                if confirm.lower() == 'y':
                    mdbc.connection.commit()
                    print("Successfully updated!")
                    break
                elif confirm.lower() == 'n':
                    mdbc.connection.rollback()
                    print("Cancelled update!")
                    break
            else:
                print("Option does not exist. Please try again!")
    except mdbc.database.Error as e:
        print(f"Error updating entry in the database: {e}")

def deleteFoodEstab():
    try:
        print("\n")
        print("***** Delete A Food Establishment *****")

        estabName = input("Input establishment name: ")
        estabId = getFoodEstabId(estabName)

        if not estabId:
            print("Establishment not found. Please try again.")
            return

        confirm = input("Are you sure you want to delete the food establishment [y/n]? ")
        if confirm.lower() == 'y':
            statement = "DELETE FROM foodestablishment WHERE establishmentId=%s"
            data = (estabId,)
            mdbc.cursor.execute(statement, data)
            mdbc.connection.commit()
            print("Successfully deleted!")
        elif confirm.lower() == 'n':
            print("Cancelled delete!")
    except mdbc.database.Error as e:
        print(f"Error deleting entry from the database: {e}")

def updateFoodItem():
    try:
        print("\n")
        print("***** Update A Food Item *****")

        foodItemName = input("Input food item name: ")
        foodItemId = getFoodItemId(foodItemName)

        if not foodItemId:
            print("Food item not found. Please try again.")
            return

        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Price")
            print("[3] Description")
            print("[4] Food Type")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE fooditem SET name=%s WHERE itemId=%s"
                data = (updName, foodItemId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 2:
                updPrice = input("New price: ")
                statement = "UPDATE fooditem SET price=%s WHERE itemId=%s"
                data = (updPrice, foodItemId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 3:
                updDescription = input("New description: ")
                statement = "UPDATE fooditem SET description=%s WHERE itemId=%s"
                data = (updDescription, foodItemId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 4:
                # Delete existing food types for this item
                statement = "DELETE FROM fooditemtype WHERE itemId=%s"
                data = (foodItemId,)
                mdbc.cursor.execute(statement, data)

                # Ask user for new food types and add them
                tagFoodItemwithType(foodItemId, foodItemName)
            elif updChoice == 0:
                confirm = input("Are you sure you want to update the food item [y/n]? ")
                if confirm.lower() == 'y':
                    mdbc.connection.commit()
                    print("Successfully updated!")
                    break
                elif confirm.lower() == 'n':
                    mdbc.connection.rollback()
                    print("Cancelled update!")
                    break
            else:
                print("Option does not exist. Please try again!")
    except mdbc.database.Error as e:
        print(f"Error updating entry in the database: {e}")

def deleteFoodItem():
    try:
        print("\n")
        print("***** Delete A Food Item *****")

        foodItemName = input("Input food item name: ")
        foodItemId = getFoodItemId(foodItemName)

        if not foodItemId:
            print("Food item not found. Please try again.")
            return

        confirm = input("Are you sure you want to delete the food item [y/n]? ")
        if confirm.lower() == 'y':
            # Delete from fooditemtype table first
            statement1 = "DELETE FROM fooditemtype WHERE itemId=%s"
            data1 = (foodItemId,)
            mdbc.cursor.execute(statement1, data1)

            # Delete from fooditem table
            statement2 = "DELETE FROM fooditem WHERE itemId=%s"
            data2 = (foodItemId,)
            mdbc.cursor.execute(statement2, data2)

            mdbc.connection.commit()
            print("Successfully deleted!")
        elif confirm.lower() == 'n':
            print("Cancelled delete!")
    except mdbc.database.Error as e:
        print(f"Error deleting entry from the database: {e}")

def adminViewAllFoodEstab():
    try:
        mdbc.reconnect() 
        print("\n")
        print("***** VIEW FOOD ESTABLISHMENTS ******")
        statement = "SELECT name, location from foodestablishment;"
        mdbc.cursor.execute(statement)
        establishments = mdbc.cursor.fetchall()
        if not establishments:
            print("No food establishments found.")

        for (name, location) in establishments:
            print(f"[{name}] -  {location}")

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def adminViewAllFoodItem():
    try:
        mdbc.reconnect()
        print("\n")
        print("***** VIEW FOOD ITEMS ******")
        print("")
        statement = "SELECT name, price, description from fooditem;"
        mdbc.cursor.execute(statement)
        foods = mdbc.cursor.fetchall()
        if not foods:
            print("No foods found")
        
        for(name, price, description) in foods:
            print(f"[{name}] {price} - {description}")

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

def adminMenu():
    print("Choose an action")
    print("[1] View all establishments")
    print("[2] View all food items")
    print("[0] Logout")

    choice = int(input("I want to... "))

    return choice


def adminEstabMenu():
    print("\n")
    print("Choose an action")
    print("[1] Add an establishment")
    print("[2] Update an establishment")
    print("[3] Delete an establishment")
    print("[0] Back")

    choice = int(input("I want to... "))

    return choice

def adminFoodMenu():
    print("\n")
    print("Choose an action")
    print("[1] Add a food item")
    print("[2] Update a food item")
    print("[3] Delete a food item")
    print("[0] Back")

    choice = int(input("I want to... "))

    return choice


def adminActionsLoop():
    while True:
        print("\n")
        print("***** ADMIN PAGE *****")
        print("")
        adminMenuChoice = adminMenu()

        if adminMenuChoice == 1:
            
            adminViewAllFoodEstab()
            while True:

                estabMenuChoice = adminEstabMenu()

                if estabMenuChoice == 1:
                    addFoodEstab()
                elif estabMenuChoice == 2:
                    updateFoodEstab()
                elif estabMenuChoice == 3:
                    deleteFoodEstab()
                elif estabMenuChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")

        elif adminMenuChoice == 2:
            adminViewAllFoodItem()

            while True:
                foodMenuChoice = adminFoodMenu()

                if foodMenuChoice == 1:
                    addFoodItem()
                elif foodMenuChoice == 2:
                    updateFoodItem()
                elif foodMenuChoice == 3:
                    deleteFoodItem()
                elif foodMenuChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")

        elif adminMenuChoice == 0:
            break
        else:
            print("Option does not exist. Please try again!")