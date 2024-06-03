
import mdb_connector as mdbc
from estab_page import foodEstablishmentPage
from food_page import focusedFoodItemPage

# Home Menu
def userMenu():
    print("\n")
    print("User Menu")
    print("[1] Food Establishment")
    print("[2] Food Items")
    print("[3] User Reviews")
    print("[0] Logout")

    choice = int(input("Option: "))

    return choice

def foodEstabActions():
    print("\n")
    print("Choose an Action:")
    print("[1] Search for a Food Establishment")
    print("[2] View Food Establishments")
    print("[3] View Food Establishments with High Average Rating")
    print("[0] Back")

    choice = int(input("I want to... "))

    return choice

def foodItemActions():
    print("\n")
    print("Choose an Action:")
    print("[1] Search food item by price range")
    print("[2] Search food item by food type")
    print("[0] Back")

    choice = int(input("I want to... "))

    return choice

def userReviewActions():
    print("\n")
    print("Choose an Action:")
    print("[1] View all of your reviews")
    print("[2] Update your review")
    print("[3] Delete your review")
    print("[0] Back")

    choice = int(input("I want to... "))

    return choice

# Check if the user owns the review
def is_user_review(username, reviewId):
    try:
        mdbc.reconnect()
        statement = "SELECT COUNT(*) FROM review WHERE reviewId=%s AND username=%s"
        data = (reviewId, username)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        return result[0] > 0
    except mdbc.database.Error as e:
        print(f"Error checking review ownership: {e}")
        return False

# Retrieving Food establishment's Id
def getFoodEstabId(name):
    print("\n")
    try:
        mdbc.reconnect()
        statement = "SELECT establishmentId from foodestablishment WHERE name=%s"
        data = (name,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result:
            establishmentId = result[0]  # Fetch the first element of the tuple
            return establishmentId
        else:
            return 0

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
        return 0

# Search Food Establishment
def searchFoodEstab(username):
    print("\n")
    try:
        mdbc.reconnect()  
        name = input("Which establishment do you want to view?: ")
        result = getFoodEstabId(name)
        if result != 0:
            statement = "SELECT * FROM foodestablishment WHERE establishmentId=%s"
            data = (result,)
            mdbc.cursor.execute(statement, data)
            establishment_details = mdbc.cursor.fetchone()
            if establishment_details:
                establishmentId, name, location = establishment_details
                print(f"Establishment ID: {establishmentId}")
                print(f"Name: {name}")
                print(f"Location: {location}")

                choice = input("Do you want to view this establishment? (y/n): ")
                if choice.lower() == 'y':
                    foodEstablishmentPage(result, username)
                else:
                    return None
            else:
                print("Establishment not found.")
                return None 
        else:
            print("No establishment found")
            return None  

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return None

# View all establishments
def viewAllFoodEstab():
    try:
        mdbc.reconnect() 
        print("\n")
        print("***** VIEW FOOD ESTABLISHMENTS ******")
        statement = "SELECT name, location from foodestablishment;"
        mdbc.cursor.execute(statement)
        establishments = mdbc.cursor.fetchall()
        if not establishments:
            print("No food establishments found.")
            return None 

        for (name, location) in establishments:
            print(f"[{name}] -  {location}")
        
        print("")
        print("[0] Go Back")
        choice = input("Which establishment do you want to view?: ")
        if choice == '0':
            return None
        result = getFoodEstabId(choice)
        if result != 0:
            return result  # returns foodEstabId to be used to redirect to food estab page
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

# View establishments sorted by highest rating
def viewByHighRating():
    try:
        mdbc.reconnect()  
        print("\n")
        print("***** VIEW ESTABLISHMENTS BY HIGHEST RATING ******")
        statement = "SELECT name, AVG(rating) FROM foodestablishment fe JOIN review r on fe.establishmentId= r.establishmentId GROUP BY fe.establishmentId HAVING AVG(rating) >= 4 ORDER BY AVG(rating) DESC"
        mdbc.cursor.execute(statement)
        establishments = mdbc.cursor.fetchall()
        if not establishments:
            print("No food establishments found with high ratings.")
            return None  

        for (name, rating) in establishments:
            formatted_rating = "{:.1f}".format(rating)  # Format the rating to display with one decimal place
            print(f"[{name}] -   {formatted_rating}")
            
        print("")
        print("[0] Go Back")
        choice = input("Which establishment do you want to view?: ")
        if choice == '0':
            return None
        result = getFoodEstabId(choice)
        if result != 0:
            return result  # returns foodEstabId to be used to redirect to food estab page
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

# Search Food Item by Price Range
def searchFoodByPriceRange(username):
    try:
        mdbc.reconnect()
        print("\n")
        print("***** SEARCH FOOD ITEM BY PRICE RANGE ******")
        priceRange = input("Enter price range (e.g., 10-50): ")
        lowRange, highRange = map(int, priceRange.split("-"))

        statement = "SELECT itemId, name, price, description FROM fooditem WHERE price BETWEEN %s AND %s"
        data = (lowRange, highRange)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchall()
        if not result:
            print("No food item in that price range")
            return

        for (itemId, name, price, description) in result:
            print(f"[{itemId}] {name} - {price} - {description}")

        print("\n")
        print("[0] Go back")
        choice = input("Input food Id to view food item: ")

        while choice != '0' and not any(int(choice) == item[0] for item in result):
            print("Invalid option! Please select a valid food item or '0' to go back.")
            choice = input("Input food Id to view food item: ")

        if choice == '0':
            return
        else:
            # Redirect to the food_page
            focusedFoodItemPage(int(choice), username)

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

# Search Food Item by Food Type
def searchFoodByFoodType(username):
    try:
        mdbc.reconnect()
        print("\n")
        print("***** SEARCH FOOD ITEMS BY FOOD TYPE ******")
        print("")
        statement = "SELECT * from foodtype"
        mdbc.cursor.execute(statement)
        food_types = {str(foodtypeId): foodType for foodtypeId, foodType in mdbc.cursor}
        for foodtypeId, foodType in food_types.items():
            print(f"[{foodtypeId}] {foodType}")

        print("\n")

        while True:
            searchChoice = input("Which food type would you like to search? ")

            if searchChoice in food_types:
                searchChoice = int(searchChoice)
                break
            else:
                print("Only choose in the food types above")

        statement = "SELECT itemId, name, price, description from fooditem WHERE itemid in (SELECT itemid from fooditemtype WHERE foodtypeId = %s)"
        data = (searchChoice,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchall()
        if not result:
            print("No food item of that type found")
            return

        for (itemId, name, price, description) in result:
            print(f"[{itemId}] {name} - {price} - {description}")

        print("\n")
        print("[0] Go back")
        choice = input("Input food Id to view food item: ")

        while choice != '0' and not any(int(choice) == item[0] for item in result):
            print("Invalid option! Please select a valid food item or '0' to go back.")
            choice = input("Input food Id to view food item: ")

        if choice == '0':
            return
        else:
            # Redirect to the food_page
            focusedFoodItemPage(int(choice), username)

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

# View all user's reviews
def viewUserReviews(username):
    try:
        mdbc.reconnect()
        print("\n")
        statement = "SELECT COUNT(*) FROM review WHERE username=%s"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result[0] == 0:
            print(" You currently have no reviews.")
            return
        
        print("\n")
        print(f"***** YOUR REVIEWS *****")
        # Print user's food item reviews
        print("")
        print("----- Food Reviews -----")
        statement = """SELECT r.reviewId, r.rating, r.comment, r.date_reviewed, fi.name, fe.name
                       FROM review r
                       JOIN fooditem fi ON r.itemId = fi.itemId
                       JOIN foodestablishment fe ON fi.establishmentId = fe.establishmentId
                       WHERE r.username=%s AND r.itemId IS NOT null"""
        data = (username,)
        mdbc.cursor.execute(statement, data)
        for (reviewId, rating, comment, date_reviewed, food_name, estab_name) in mdbc.cursor:
            print(f"[{food_name}]\nReview ID: {reviewId}\nRating: {rating}\nComment: {comment}\nDate Reviewed: {date_reviewed}")
            print("")

        # Print user's establishment reviews
        print("----- Establishment Reviews -----")
        statement = """SELECT r.reviewId, r.rating, r.comment, r.date_reviewed, fe.name
                       FROM review r
                       JOIN foodestablishment fe ON r.establishmentId = fe.establishmentId
                       WHERE r.username=%s AND r.establishmentId IS NOT null"""
        data = (username,)
        mdbc.cursor.execute(statement, data)
        for (reviewId, rating, comment, date_reviewed, estab_name) in mdbc.cursor:
            print(f"[{estab_name}]\nReview ID: {reviewId}\nRating: {rating}\nComment: {comment}\nDate Reviewed: {date_reviewed}")
            print("")

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

# Updating user's review
def updateReview(username):
    try:
        mdbc.reconnect()
        viewUserReviews(username)
        statement = "SELECT COUNT(*) FROM review WHERE username=%s"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result[0] == 0:
            return
        
        print("")
        updId = input("Input review ID to update: ")
        if not is_user_review(username, updId):
            print("You can only update your own reviews.")
            return

        while True:
            print("What do you want to update?")
            print("[1] Rating")
            print("[2] Comment")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updRating = input("New rating: ")
                statement = "UPDATE review SET rating=%s WHERE reviewId = %s"
                data = (updRating, updId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 2:
                updComment = input("New comment: ")
                statement = "UPDATE review SET comment=%s WHERE reviewId = %s"
                data = (updComment, updId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to save the updates [y/n]? ")
                if confirm == 'y':
                    mdbc.connection.commit()
                    print("Successfully updated!")
                    break
                elif confirm == 'n':
                    mdbc.connection.rollback()
                    print("Cancelled update!")
                    break
            else:
                print("Option does not exist. Please try again!")
    except mdbc.database.Error as e:
        print(f"Error updating review: {e}")

# Deleting user's review
def deleteReview(username):
    try:
        mdbc.reconnect()
        print("\n")
        viewUserReviews(username)
        statement = "SELECT COUNT(*) FROM review WHERE username=%s"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result[0] == 0:
            return
        
        print("\n")
        print("***** Delete A Review *****")

        delId = input("Input reviewId: ")
        if not is_user_review(username, delId):
            print("You can only delete your own reviews.")
            return

        confirm = input("Are you sure you want to delete this review [y/n]? ")
        if confirm == 'y':
            statement = "DELETE FROM review WHERE reviewId=%s"
            data = (delId,)
            mdbc.cursor.execute(statement, data)
            mdbc.connection.commit()
            print("Successfully deleted!")
        elif confirm == 'n':
            print("Cancelled delete!")
    except mdbc.database.Error as e:
        print(f"Error deleting review: {e}")
   
# User Menu
def userActionsLoop(username):
    while True:
        userMenuChoice = userMenu()

        if userMenuChoice == 1:
            while True:
                estabChoice = foodEstabActions()
                if estabChoice == 1:
                    searchFoodEstab(username)
                elif estabChoice == 2:
                    estabId = viewAllFoodEstab()
                    if estabId:
                        foodEstablishmentPage(estabId, username)
                elif estabChoice == 3:
                    estabId = viewByHighRating()
                    if estabId:
                        foodEstablishmentPage(estabId, username)
                elif estabChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 2:
            while True:
                foodChoice = foodItemActions()
                if foodChoice == 1:
                    searchFoodByPriceRange(username)
                elif foodChoice == 2:
                    searchFoodByFoodType(username)
                elif foodChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 3:
            while True:
                reviewChoice = userReviewActions()
                if reviewChoice == 1:
                    viewUserReviews(username)
                elif reviewChoice == 2:
                    updateReview(username)
                elif reviewChoice == 3:
                    deleteReview(username)
                elif reviewChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 0:
            mdbc.connection.close()
            break
        else:
            print("Option does not exist. Please try again!")