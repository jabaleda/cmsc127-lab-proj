import os
import mysql.connector as database

# username = os.environ.get("username")
# password = os.environ.get("password")

connection = database.connect(
    user="root",                                        # Uses root user
    password="comsci.127",                                      # ! Change this to your password
    host="127.0.0.1",
    database="cmsc127project"                                # ! Change this to the name of project database you use
)

cursor = connection.cursor()


def addFoodEstab():
    try:
        print("\n")
        print("***** Add A Food Establishment *****")

        print("\n")
        print("Just a few things...")
        # input establishment name
        name = input("Enter your establishment name (max. 30 characters): ")
        if len(name) > 30:
            print("Invalid establishment name! Exceeded 30 characters.")
            return
        # input establishment location
        location = input("Enter your establishment location (max. 30 characters): ")
        if len(location) > 30:
            print("Invalid establishment location! Exceeded 30 characters.")
            return
        
        statement = "INSERT INTO foodestablishment (name, location) VALUES (%s, %s)"
        data = (name, location)
        cursor.execute(statement, data)
        connection.commit()

        print("Establishment added successfully!")
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    except ValueError:
        print("Invalid input! Please enter the correct data types.")


def getEstabId(estabName):
    try:
        statement = "SELECT establishmentId FROM foodestablishment WHERE name=%s"
        data = (estabName,)
        cursor.execute(statement, data)
        estabId = cursor.fetchone()
        if estabId:
            return estabId[0]
        else:
            print("Establishment not found!")
            return None
        
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return None


def getFoodTypeId(foodTypeName):
    try:
        statement = "SELECT foodtypeId FROM foodtype WHERE foodType=%s"
        data = (foodTypeName,)
        cursor.execute(statement, data)
        foodTypeId = cursor.fetchone()
        if foodTypeId:
            return foodTypeId[0]
        else:
            # print("Establishment not found!")
            return None
        
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return None
    

def addFoodType(foodTypeName):
    try:
        statement = "INSERT INTO foodtype (foodType) VALUES (%s)"
        data = (foodTypeName,)
        cursor.execute(statement, data)
        connection.commit()
        # print success
    except database.Error as e:
        print(f"Error adding entry to database: {e}")


def addtoFoodItemTypeTable(itemId, itemName, foodTypeId, foodType):
    try:
        statement = "INSERT INTO fooditemtype (itemId, name, foodtypeId, foodType) VALUES (%s, %s,%s, %s)"
        data = (itemId, itemName, foodTypeId, foodType,)
        cursor.execute(statement, data)
        connection.commit()
        # print success
    except database.Error as e:
        print(f"Error adding entry to database: {e}")


def tagFoodItemwithType(foodItemId, foodItemName):
    while True:
        # ask to enter a food type
        foodType = input("Enter a food type for your new item: ")
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
            estabId = getEstabId(estabName)

            if estabId:
                # prompt for name
                foodItemName = input("Enter food item name: ")
                # prompt for price
                foodItemPrice = input("Enter food item price: ")
                # prompt for description
                foodItemDesc = input("Enter food item description: ")

                statement = "INSERT INTO fooditem (name, price, description, establishmentId) VALUES (%s, %s, %s, %s)"
                data = (foodItemName, foodItemPrice, foodItemDesc, estabId)
                cursor.execute(statement, data)
                connection.commit()

                # obtain id of newly inserted food item
                statement2 = "SELECT itemId FROM fooditem WHERE name=%s"
                data2 = (foodItemName,)
                cursor.execute(statement2, data2)
                newFoodItemId = cursor.fetchone()

                # prompt for food types
                doneFlag = tagFoodItemwithType(newFoodItemId[0], foodItemName)

                # if function returned a value, exit
                if doneFlag:
                    break
            
            else:
                print("Please try again.") 

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")




def updateFoodEstab():
    try:
        print("/n")
        print("***** Update A Food Establishment *****")

        updId = input("Input establishmentId: ")
        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Location")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE foodestablishment SET name=%s WHERE establishmentid = %s"
                data = (updName, updId,)
                cursor.execute(statement, data)
            elif updChoice == 2:
                updLocation = input("New location: ")
                statement = "UPDATE foodestablishment SET location=%s WHERE establishmentid = %s"
                data = (updLocation, updId,)
                cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to update food establishment [y/n]? ")
                if confirm == 'y':
                    connection.commit()
                    print("Successfully updated!")
                    break
            
                elif confirm == 'n':
                    connection.rollback()
                    print("Cancelled update!")
                    break
            else:
                print("Option does not exist. Please try again!")
        return 0
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def deleteFoodEstab():
    try:
        print("/n")
        print("***** Delete A Food Establishment *****")

        delId = input("Input establishmentId: ")

        confirm = input("Are you sure you want to delete food establishment [y/n]? ")
        if confirm == 'y':
            statement = "DELETE from foodestablishment WHERE establishmentId =%s"
            data = (delId,)
            cursor.execute(statement, data)
            connection.commit()
            print("Successfully deleted!")
            return 1
        elif confirm == 'n':
            print("Cancelled delete!")
            return 0

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")

def updateFoodItem():
    try:
        print("/n")
        print("***** Update A Food Item *****")

        updId = input("Input itemId: ")
        
        typeCount = 0
        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Price")
            print("[3] Description")
            print("[3] Food Type")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE fooditem SET name=%s WHERE itemId = %s"
                data = (updName, updId,)
                cursor.execute(statement, data)
            elif updChoice == 2:
                updPrice = input("New price: ")
                statement = "UPDATE fooditem SET price=%s WHERE itemId = %s"
                data = (updPrice, updId,)
                cursor.execute(statement, data)
            elif updChoice == 3:
                updDescription = input("New description: ")
                statement = "UPDATE fooditem SET description=%s WHERE itemId = %s"
                data = (updDescription, updId),
                cursor.execute(statement, data)
            elif updChoice == 4:
                if typeCount == 0:
                    # statement = "SAVEPOINT delfoodtype"
                    # cursor.execute(statement)
                    statement = "DELETE from fooditemtype where itemId = %s"
                    data = (updId,)
                    cursor.execute(statement, data)
                updType = input("New food type: ")
                statement = "INSERT INTO fooditemtype(itemId, foodtypeId) VALUES (%s, %s)"
                data = (updId, updType,)
                cursor.execute(statement, data)
                typeCount = typeCount + 1
            elif updChoice == 0:
                confirm = input("Are you sure you want to update food item [y/n]? ")
                if confirm == 'y':
                    connection.commit()
                    print("Successfully updated!")
                    break
            
                elif confirm == 'n':
                    connection.rollback()
                    print("Cancelled update!")
                    break
            else:
                print("Option does not exist. Please try again!")
        return 0
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def deleteFood():
    try:
        print("/n")
        print("***** Delete A Food Item *****")

        delId = input("Input itemId: ")

        confirm = input("Are you sure you want to delete food item [y/n]? ")
        if confirm == 'y':
            statement = "DELETE from fooditem WHERE itemId =%s"
            data = (delId,)
            cursor.execute(statement, data)
            connection.commit()
            print("Successfully deleted!")
            return 1
        elif confirm == 'n':
            print("Cancelled delete!")
            return 0

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def adminViewAllFoodEstab():
    try:
        print("***** View Food Establishments ******")
        statement = "SELECT * from foodestablishment;"
        cursor.execute(statement)
        for(establishmentId, name, location) in cursor:
            print(f"[{establishmentId}] {name} - {location}")

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def adminMenu():
    print("\n")
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
        adminMenuChoice = adminMenu()

        if adminMenuChoice == 1:
            # print all food establishments here -> call view all estab
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
            # print all food items here -> call view all food
            while True:
                foodMenuChoice = adminFoodMenu()

                if foodMenuChoice == 1:
                    addFoodItem()
                elif foodMenuChoice == 2:
                    updateFoodItem()
                elif foodMenuChoice == 3:
                    deleteFood
                elif foodMenuChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")

        elif adminMenuChoice == 0:
            break
        else:
            print("Option does not exist. Please try again!")
        