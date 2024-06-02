# 3. Food Establishment Page Group

# * Import statements
# Changed import statement from main to only access the cursor
# from main import cursor
import mdb_connector as mdbc
from food_page import *

# * functions ----------

# ? DB functions ----------
def getAllFoodItems(estabId):
    items = list()

    try:
        # Corrected the column name to match the schema and parameter name
        statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for (itemId, name, price, description) in mdbc.cursor:
            item = (itemId, name, price, description)
            items.append(item)

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return items

def getAllEstabReviews(estabId):
    reviews = list()
    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE establishmentId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for (rating, comment, date_reviewed, username) in mdbc.cursor:
            review = (rating, comment, date_reviewed, username)
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews

# sorted
def sortFoodItemsbyPrice(estabId, sort):
    sortedItems = list()
    try:
        # Construct the SQL query dynamically to include the sorting order
        statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s ORDER BY price %s"
        if sort.upper() == "ASC":
            statement = statement % (estabId, "ASC")
        elif sort.upper() == "DESC":
            statement = statement % (estabId, "DESC")
        else:
            print("Invalid sorting order specified.")
            return sortedItems
        
        # Use the execute() method to pass parameters securely
        mdbc.cursor.execute(statement)
        for (itemId, name, price, description) in mdbc.cursor:
            item = (itemId, name, price, description)
            sortedItems.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return sortedItems

# * 3a. All Food item Functions ----------
# should receive estabid to search all food items of establishment
def allFoodItems(estabId):
    foodItems = getAllFoodItems(estabId)

    print("---------- FOOD ITEMS ----------")

    if len(foodItems) > 0:
        # print all food items
        for i, x in enumerate(foodItems, start=1):
            print(f"[{i}] {x[1]}")   # prints food name
        print("[0] Back")

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


def allFoodItemsMenu(estabId):
    while True:
        choice = allFoodItems(estabId)

        if choice == 0:
            break
        else:
            # pass the id of the selected food item
            focusedFoodItemPage(choice)
    return


# * 3c. Sort Food Items by Price Functions ----------

def allFoodItemsbyPrice(estabId, sort):
    sortedFoodItems = sortFoodItemsbyPrice(estabId, sort)

    if len(sortedFoodItems) > 0:
        for i, x in enumerate(sortedFoodItems, start=1):
            print(f"[{i}] {x[1]}")  # prints food name
        
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


def allFoodItemsbyPriceMenu(estabId, sort):
    while True:
        choice = allFoodItemsbyPrice(estabId, sort)

        if choice == 0:
            break
        else:
            focusedFoodItemPage(choice)
    return


def sortSelectFoodItemsbyPriceMenu():
    print("\n")
    print("[1] Ascending")
    print("[2] Descending") 
    print("[0] Back")

    while True:
        try:
            page_choice = int(input("Select an action: "))
            if page_choice in [0, 1, 2]:
                return page_choice
            else:
                print("Invalid choice! Please select a valid option.")
        except ValueError:
            print("Invalid input! Please enter a number.")


def sortSelectFoodItemsbyPricePage(estabId):
    while True:
        choice = sortSelectFoodItemsbyPriceMenu()

        if choice == 0:
            break
        elif choice == 1:
            print("Food Items sorted by Price - Ascending")
            allFoodItemsbyPriceMenu(estabId, "ASC")
        elif choice == 2:
            print("Food Items sorted by Price - Descending")
            allFoodItemsbyPriceMenu(estabId, "DESC")


# * 3d. Establishment reviews Functions ----------
def allEstabReviews(estabId):
    estabReviews = getAllEstabReviews(estabId)

    print("Reviews for <Estab Name>")

    if len(estabReviews) > 0:
        for x in estabReviews:
            print("-------------------")
            print(f"Sender:     {x[3]}")
            print(f"Rating:     {x[0]}")
            print(f"{x[1]}")
            print(f"Published:  {x[2]}")

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


# * 3. Food Establishment functions ----------
def foodEstabMenu():
    print("\n")
    print("Establishment location: <location>")  # This can be printed on select of an establishment, before calling this function instead so this function only needs the estabId
    print(" [1] View all food items")
    print(" [2] View food items by food type")
    print(" [3] View food items sorted by price")
    print(" [4] View all establishment reviews")
    print(" [5] View recent establishment reviews")
    print(" [6] Review this establishment")
    print(" [0] Back")

    while True:
        try:
            page_choice = int(input("Select an action: "))
            return page_choice
        except ValueError:
            print("Invalid input! Please enter a number.")


def foodEstablishmentPage(estabId):
    while True:
        print("<Establishment Name> Details")  # This can be printed on select of an establishment, before calling this function instead so this function only needs the estabId
        choice = foodEstabMenu()

        if choice == 0:
            print("Returning...")
            mdbc.connection.close()
            break

        elif choice == 1:
            # redirect to view all food items
            allFoodItemsMenu(estabId)

        elif choice == 2:
            # redirect to view food items by food type
            # Implement if needed
            pass

        elif choice == 3:
            # redirect to view food items sorted by price
            sortSelectFoodItemsbyPricePage(estabId)

        elif choice == 4:
            # redirect to view all establishment reviews
            allEstabReviews(estabId)

        elif choice == 5:
            # redirect to view recent establishment reviews
            # Implement if needed
            pass

        elif choice == 6:
            # redirect to input of adding a review
            # Implement if needed
            pass

        else:
            print("Invalid choice!")



