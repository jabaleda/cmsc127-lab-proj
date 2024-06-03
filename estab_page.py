# Establishment Page

import mdb_connector as mdbc
from food_page import *

MONTHS = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

# Getting Establishment's name and location
def getEstablishmentDetails(establishmentId):
    try:
        mdbc.reconnect()
        statement = "SELECT name, location FROM foodestablishment WHERE establishmentId = %s"
        data = (establishmentId,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result:
            return result
        else:
            print("Establishment not found!")
            return None
    except mdbc.database.Error as e:
        print(f"Error retrieving establishment details from database: {e}")
        return None

# Retrieving food items of an establishment
def getAllFoodItems(estabId):
    items = list()

    try:
        mdbc.reconnect()
        statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for (itemId, name, price, description) in mdbc.cursor:
            item = (itemId, name, price, description)
            items.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return items

# Retrieving establishment reviews
def getAllEstabReviews(estabId):
    reviews = list()
    try:
        mdbc.reconnect()
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE establishmentId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for (rating, comment, date_reviewed, username) in mdbc.cursor:
            review = (rating, comment, date_reviewed, username)
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews

# Retrieving all food items of an establishment
def allFoodItems(estabId):
    mdbc.reconnect()
    foodItems = getAllFoodItems(estabId)

    print("\n")
    print("***** FOOD ITEMS *****")
    print("")

    if len(foodItems) > 0:
        for i, x in enumerate(foodItems, start=1):
            print(f"[{i}] {x[1]}")
        print("")
        print("[0] Back")
        print("")

        while True:
            try:
                choice = int(input("Select a food item: "))
                if choice == 0:
                    return 0
                elif 1 <= choice <= len(foodItems):
                    return foodItems[choice - 1][0]
                else:
                    print("Invalid choice! Please select a valid food item number.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    else:
        print("No food items found!")
        return
    
# Retrieving all food types
def getAllFoodTypes():
    types = list()
    try:
        statement = "SELECT foodtypeId, foodType FROM foodType"
        mdbc.cursor.execute(statement)
        for(foodtypeId, foodType) in mdbc.cursor:
            type = tuple((foodtypeId, foodType))
            types.append(type)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    return types

# Filtering Food Items by its Food type
def filterFoodItemsbyType(estabId, typeId):
    itemsInType = list()
    try:
        mdbc.reconnect()
        statement = "SELECT DISTINCT fi.itemId, fi.name FROM fooditem fi JOIN fooditemtype fift ON fi.itemId = fift.itemId WHERE fi.establishmentId = %s AND fift.foodtypeId = %s"
        data = (estabId, typeId)
        mdbc.cursor.execute(statement, data)
        for(itemId, name) in mdbc.cursor:
            item = tuple((itemId, name))
            itemsInType.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return itemsInType

# Retrieving the food type's Id
def getFoodTypeById(typeId):
    try:
        mdbc.reconnect()
        statement = "SELECT foodType FROM foodtype WHERE foodtypeId = %s"
        data = (typeId,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Food type not found!")
            return None
    except mdbc.database.Error as e:
        print(f"Error retrieving food type from database: {e}")
        return None

# Sorting Food Items by its price
def sortFoodItemsbyPrice(estabId, sort):
    sortedItems = list()
    try:
        mdbc.reconnect()
        if sort.upper() == "ASC":
            statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s ORDER BY price ASC"
        elif sort.upper() == "DESC":
            statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s ORDER BY price DESC"
        else:
            print("Invalid sorting order specified.")
            return sortedItems
        
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for (itemId, name, price, description) in mdbc.cursor:
            item = (itemId, name, price, description)
            sortedItems.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return sortedItems

def allFoodItemsMenu(estabId, username):
    mdbc.reconnect()
    while True:
        choice = allFoodItems(estabId)

        if choice == 0:
            break
        else:
            focusedFoodItemPage(choice, username)
    return

def allFoodItemsbyPrice(estabId, sort):
    mdbc.reconnect()
    sortedFoodItems = sortFoodItemsbyPrice(estabId, sort)

    if len(sortedFoodItems) > 0:
        for i, x in enumerate(sortedFoodItems, start=1):
            print(f"[{i}] {x[1]} -  {x[2]}")
        
        print("[0] Back")

        while True:
            try:
                choice = int(input("Select a food item: "))
                if choice == 0:
                    return 0
                elif 1 <= choice <= len(sortedFoodItems):
                    return sortedFoodItems[choice - 1][0]
                else:
                    print("Invalid choice! Please select a valid food item number.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    else:
        print("No food items found!")

def allFoodItemsbyType(estabId, typeId, username):
    foodType = getFoodTypeById(typeId)
    filteredItems = filterFoodItemsbyType(estabId, typeId)
    print("\n")
    print(f"***** FOOD ITEMS IN {foodType} *****")

    if len(filteredItems) > 0:
        # print all food items
        i = 1
        for x in filteredItems:
            print(f"[{i}] {x[1]}")   # prints food name
            i += 1
        print("")
        print("[0] Back")

        while True:
            choice = int(input("Select a food item: "))
            if choice == 0:
                break
            elif choice < 0 or choice > len(filteredItems):
                print("Invalid choice!")
            else:
                focusedFoodItemPage(filteredItems[choice - 1][0], username)
                # Display the food items again after navigating back from the food item page
                print(f"\n***** FOOD ITEMS IN {foodType} *****")
                i = 1
                for x in filteredItems:
                    print(f"[{i}] {x[1]}")   # prints food name
                    i += 1
                print("")
                print("[0] Back")
    else:
        print("No food items found!")
        return

def foodTypesMenu(estabId):
    types = getAllFoodTypes()
    print("")
    i = 1
    for x in types:
        print(f"[{i}] {x[1]}")
        i += 1
    print("")
    print("[0] Back")

    while True:
        choice = int(input("Select a type: "))
        if choice == 0:
            return choice
        elif choice < 0 or choice > len(types):
            print("Invalid choice!")
        else:
            return types[choice - 1][0]       # returns the foodtypeId

def filterFoodItemsbyTypePage(estabId, username):
    print("\n")
    print("***** VIEW FOOD ITEMS BY TYPE *****")
    while True:
        choice = foodTypesMenu(estabId)
        if choice == 0:
            break
        else:
            allFoodItemsbyType(estabId, choice, username)

def allFoodItemsbyPriceMenu(estabId, sort, username):
    mdbc.reconnect()
    while True:
        choice = allFoodItemsbyPrice(estabId, sort)

        if choice == 0:
            break
        else:
            focusedFoodItemPage(choice, username)
    return

def sortSelectFoodItemsbyPriceMenu():
    print("\n")
    print("Sort Items by?")
    print("")
    print("[1] Ascending")
    print("[2] Descending")
    print("[0] Back")

    while True:
        try:
            mdbc.reconnect()
            page_choice = int(input("Select an action: "))
            if page_choice in [0, 1, 2]:
                return page_choice
            else:
                print("Invalid choice! Please select a valid option.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def sortSelectFoodItemsbyPricePage(estabId, username):
    while True:
        mdbc.reconnect()
        choice = sortSelectFoodItemsbyPriceMenu()

        if choice == 0:
            break
        elif choice == 1:
            print("\n")
            print("***** Food Items sorted by Price - Ascending *****")
            print("")
            allFoodItemsbyPriceMenu(estabId, "ASC", username)
        elif choice == 2:
            print("\n")
            print("***** Food Items sorted by Price - Descending *****")
            print("")
            allFoodItemsbyPriceMenu(estabId, "DESC", username)

def allEstabReviews(estabId):
    mdbc.reconnect()
    estabReviews = getAllEstabReviews(estabId)
    estab_details = getEstablishmentDetails(estabId)
    if not estab_details:
        return
    
    estab_name, estab_location = estab_details
    print(f"***** REVIEWS FOR {estab_name} *****")

    if len(estabReviews) > 0:
        for x in estabReviews:
            print("-------------------")
            print("")
            print(f"Username:   {x[3]}")
            print(f"Rating:     {x[0]}/5.0")
            print(f"Comment:    {x[1]}")
            print(f"Published:  {x[2]}")
            print("")

        print("[0] Back")

        while True:
            try:
                choice = int(input("Return? "))
                if choice == 0:
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
    else:
        print("No reviews found!")

# 3e. View all reviews made within a month for an establishment
def recentEstabReviews(estabId):
    month = input("Enter the month (e.g., January, February, etc.) to view reviews: ")
    month_num = MONTHS.get(month.capitalize())
    
    if not month_num:
        print("Invalid month! Please enter a valid month name.")
        return

    reviews = list()

    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE establishmentId=%s AND MONTH(date_reviewed) = %s"
        data = (estabId, month_num)
        mdbc.cursor.execute(statement, data)
        for (rating, comment, date_reviewed, username) in mdbc.cursor:
            review = (rating, comment, date_reviewed, username)
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    if len(reviews) > 0:
        for x in reviews:
            print("")
            print("-------------------")
            print("")
            print(f"Username:     {x[3]}")
            print(f"Rating:     {x[0]}/5.0")
            print(f"Comment:    {x[1]}")
            print(f"Published:  {x[2]}")
        
        print("")
        print("[0] Back")

        while True:
            try:
                choice = int(input("Return? "))
                if choice == 0:
                    break
                else:
                    print("Invalid choice!")
            except ValueError:
                print("Invalid input! Please enter a number.")
    else:
        print("No reviews found for the specified month!")

# 3f. Add an establishment review
def addEstabReview(estabId, username):
    try:
        rating = float(input("Enter rating (0.0 to 5.0): "))
        if rating < 0.0 or rating > 5.0:
            print("Invalid rating! Must be between 0.0 and 5.0.")
            return

        comment = input("Enter your comment (max 100 characters): ")
        if len(comment) > 100:
            print("Comment too long! Max 100 characters.")
            return

        statement = "INSERT INTO review (rating, comment, date_reviewed, username, establishmentId) VALUES (%s, %s, NOW(), %s, %s)"
        data = (rating, comment, username, estabId)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()

        print("Review added successfully!")
    except mdbc.database.Error as e:
        print(f"Error adding review to database: {e}")
    except ValueError:
        print("Invalid input! Please enter the correct data types.")

# Establishment Page Menu
def foodEstabMenu():
    print("")
    print(" [1] View all food items")
    print(" [2] View food items by food type")
    print(" [3] View food items sorted by price")
    print(" [4] View all establishment reviews")
    print(" [5] View recent establishment reviews")
    print(" [6] Review this establishment")
    print(" [0] Back")
    print("")

    while True:
        try:
            page_choice = int(input("Select an action: "))
            return page_choice
        except ValueError:
            print("Invalid input! Please enter a number.")

# Establishment Page
def foodEstablishmentPage(estabId, username):
    mdbc.reconnect()
    estab_details = getEstablishmentDetails(estabId)
    if not estab_details:
        return
    
    estab_name, estab_location = estab_details
    while True:
        print("\n")
        print("***** ESTABLISHMENT PAGE *****")
        print("")
        print(f"    {estab_name} Details")
        print(f" Location: {estab_location}")
        choice = foodEstabMenu()

        if choice == 0:
            print("Returning...")
            break

        elif choice == 1:
            allFoodItemsMenu(estabId, username)

        elif choice == 2:
            filterFoodItemsbyTypePage(estabId, username)
            
        elif choice == 3:
            sortSelectFoodItemsbyPricePage(estabId, username)

        elif choice == 4:
            print("\n")
            allEstabReviews(estabId)

        elif choice == 5:
            print("\n")
            recentEstabReviews(estabId)

        elif choice == 6:
            addEstabReview(estabId, username)

        else:
            print("Invalid choice!")

