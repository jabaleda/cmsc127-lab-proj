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
            if result != 0:
                return result #returns foodEstabId to be used to redirect to food estab page

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
            return result #returns foodEstabId to be used to redirect to food estab page
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
            return result #returns foodEstabId to be used to redirect to food estab page
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def searchFoodByPriceRange():
    try:
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
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def searchFoodByFoodType():
    try:
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

def viewUserReviews(username):
    try:
        print("/n")
        print("***** {username}'s Reviews *****")

        #Prints user's food item reviews
        print("-- Food Item Reviews --")
        statement = "SELECT reviewId, rating, comment, date_reviewed, itemId FROM review WHERE username=%s AND itemId IS NOT null"
        data = (username,)
        cursor.execute(statement, data)
        for(reviewId, rating, comment, date_reviewed, itemId) in cursor:
            print(f"[{reviewId}] {rating} - {comment} - {date_reviewed} - {establishmentId}")

        #Prints user's establishment reviews
        print("-- Food Establsihment Reviews --")
        statement = "SELECT reviewId, rating, comment, date_reviewed, establishmentId FROM review WHERE username=%s AND establishmentId IS NOT null"
        data = (username,)
        cursor.execute(statement, data)
        for(reviewId, rating, comment, date_reviewed, establishmentId) in cursor:
            print(f"[{reviewId}] {rating} - {comment} - {date_reviewed} - {establishmentId}")

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def updateReview():
    try:
        print("/n")
        print("***** Update A Review *****")

        updId = input("Input reviewId: ")
        while True:
            print("What do you want to update?")
            print("[1] Rating")
            print("[2] Comment")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updRating = input("New rating: ")
                statement = "UPDATE review SET rating=%s WHERE reviewid = %s"
                data = (updRating, updId)
                cursor.execute(statement, data)
            elif updChoice == 2:
                updComment = input("New comment: ")
                statement = "UPDATE review SET comment=%s WHERE reviewid = %s"
                data = (updComment, updId)
                cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to delete review [y/n]? ")
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


def deleteReview():
    try:
        print("/n")
        print("***** Delete A Review *****")

        delId = input("Input reviewId: ")

        confirm = input("Are you sure you want to delete review [y/n]? ")
        if confirm == 'y':
            statement = "DELETE from review WHERE reviewid =%s"
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

        
def userActionsLoop(username):
    while True:
        userMenuChoice = userMenu()

        if userMenuChoice == 1:
            result = foodEstabActions()
            while True:
                if estabChoice == 1:
                    #result =
                    print(searchFoodEstab())
                elif estabChoice == 2:
                    #result =
                    print(viewAllFoodEstab())
                elif estabChoice == 3:
                    #result =
                    print(viewByHighRating())
                elif estabChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 2:
            while True:
                foodChoice = foodItemActions()

                if foodChoice == 1:
                    #result =
                    searchFoodByPriceRange()
                elif foodChoice == 2:
                    searchFoodByFoodType()
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
                    #update
                    updateReview()
                elif reviewChoice == 3:
                    #delete
                    deleteReview()
                elif reviewChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 0:
            break
        else:
            print("Option does not exist. Please try again!")