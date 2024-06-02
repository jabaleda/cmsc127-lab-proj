# Import statements
import mdb_connector as mdbc
from food_page import *

MONTHS = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

# 3. Food Establishment Page Group
# * functions ----------
def getAllFoodItems(estabId):
    items = list()

    try:
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

def sortFoodItemsbyPrice(estabId, sort):
    sortedItems = list()
    try:
        statement = "SELECT itemId, name, price, description FROM fooditem WHERE establishmentId=%s ORDER BY price %s"
        if sort.upper() == "ASC":
            statement = statement % (estabId, "ASC")
        elif sort.upper() == "DESC":
            statement = statement % (estabId, "DESC")
        else:
            print("Invalid sorting order specified.")
            return sortedItems
        
        mdbc.cursor.execute(statement)
        for (itemId, name, price, description) in mdbc.cursor:
            item = (itemId, name, price, description)
            sortedItems.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return sortedItems

def allFoodItems(estabId):
    foodItems = getAllFoodItems(estabId)

    print("")
    print("---------- FOOD ITEMS ----------")
    print("")

    if len(foodItems) > 0:
        for i, x in enumerate(foodItems, start=1):
            print(f"[{i}] {x[1]}")
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

def allFoodItemsMenu(estabId, username):
    while True:
        choice = allFoodItems(estabId)

        if choice == 0:
            break
        else:
            focusedFoodItemPage(choice, username)
    return

def allFoodItemsbyPrice(estabId, sort):
    sortedFoodItems = sortFoodItemsbyPrice(estabId, sort)

    if len(sortedFoodItems) > 0:
        for i, x in enumerate(sortedFoodItems, start=1):
            print(f"[{i}] {x[1]}")
        
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

def allFoodItemsbyPriceMenu(estabId, sort, username):
    while True:
        choice = allFoodItemsbyPrice(estabId, sort)

        if choice == 0:
            break
        else:
            focusedFoodItemPage(choice, username)
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

def sortSelectFoodItemsbyPricePage(estabId, username):
    while True:
        choice = sortSelectFoodItemsbyPriceMenu()

        if choice == 0:
            break
        elif choice == 1:
            print("Food Items sorted by Price - Ascending")
            allFoodItemsbyPriceMenu(estabId, "ASC", username)
        elif choice == 2:
            print("Food Items sorted by Price - Descending")
            allFoodItemsbyPriceMenu(estabId, "DESC", username)

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

def getEstablishmentDetails(establishmentId):
    try:
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

def foodEstablishmentPage(estabId, username):
    estab_details = getEstablishmentDetails(estabId)
    if not estab_details:
        return
    
    estab_name, estab_location = estab_details
    while True:
        print("\n")
        print(f"    {estab_name} Details")
        print(f" Location: {estab_location}")
        choice = foodEstabMenu()

        if choice == 0:
            print("Returning...")
            mdbc.connection.close()
            break

        elif choice == 1:
            allFoodItemsMenu(estabId, username)

        elif choice == 2:
            pass

        elif choice == 3:
            sortSelectFoodItemsbyPricePage(estabId, username)

        elif choice == 4:
            allEstabReviews(estabId)

        elif choice == 5:
            recentEstabReviews(estabId)

        elif choice == 6:
            addEstabReview(estabId, username)

        else:
            print("Invalid choice!")

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
        print("No reviews found for the specified month!")

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
        