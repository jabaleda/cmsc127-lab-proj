import os
# import mysql.connector as database

# # username = os.environ.get("username")
# # password = os.environ.get("password")

# connection = database.connect(
#     user="root",                                        # Uses root user
#     password="comsci.127",                                      # ! Change this to your password
#     host="127.0.0.1",
#     database="cmsc127project"                                # ! Change this to the name of project database you use
# )

# mdbc.cursor = connection.mdbc.cursor()
import mdb_connector as mdbc
from estab_page import *

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
            mdbc.cursor.execute(statement, data)
            for(establishmentId) in mdbc.cursor:
                # print(f"{establishmentId} - {name} - {location}")
                return establishmentId
                # loop = 0
                #successful
            print(name + " not found!")
            return 0

        except mdbc.database.Error as e:
            print(f"Error retrieving entry from database: {e}")


def searchFoodEstab():
        print("\n")
        try:
            name = input("Which establishment do you want to view?: ")
            result = getFoodEstabId(name)
            if result != 0:
                return result #returns foodEstabId to be used to redirect to food estab page

        except mdbc.database.Error as e:
            print(f"Error retrieving entry from database: {e}")


def viewAllFoodEstab():
    try:
        print("***** View Food Establishments ******")
        statement = "SELECT * from foodestablishment;"
        mdbc.cursor.execute(statement)
        for(establishmentId, name, location) in mdbc.cursor:
            print(f"[{establishmentId}] {name} - {location}")
        choice = input("Which establishment do you want to view?: ")
        result = getFoodEstabId(choice)
        if result != 0:
            return result #returns foodEstabId to be used to redirect to food estab page
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def viewByHighRating():
    try:
        print("***** View Food Establishments By High Rating ******")
        statement = "SELECT fe.establishmentId, name, location, AVG(rating) FROM foodestablishment fe JOIN review r on fe.establishmentId= r.establishmentId GROUP BY fe.establishmentId HAVING AVG(rating) >= 4"
        mdbc.cursor.execute(statement)
        for(establishmentId, name, location, rating) in mdbc.cursor:
            print(f"[{establishmentId}] {name} - {location} - {rating} ")
        choice = input("Which establishment do you want to view?: ")
        result = getFoodEstabId(choice)
        if result != 0:
            return result #returns foodEstabId to be used to redirect to food estab page
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def getFoodItemId(name):
        print("\n")
        try:
            statement = "SELECT itemId from fooditem WHERE name=%s"
            data = (name,)
            mdbc.cursor.execute(statement, data)
            for(itemId) in mdbc.cursor:
                # print(f"{establishmentId} - {name} - {location}")
                return itemId
                # loop = 0
                #successful
            print(name + " not found!")
            return 0

        except mdbc.database.Error as e:
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
        mdbc.cursor.execute(statement, data)
        for(itemId, name, price, description, establishmentId) in mdbc.cursor:
            print(f"[{itemId}] {name} - {price} - {description} - {establishmentId}")
        choice = input("Which food item do you want to view?: ")
        result = getFoodItemId(choice)
        if result != 0:
            return result #returns itemId to be used to redirect to food item page
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")


def searchFoodByFoodType():
    try:
        print("\n")
        print("***** Search Food Items By Food Type ******")
    
        #Displays options for foodtype
        print("- FOOD TYPES -")
        statement = "SELECT * from foodtype"
        mdbc.cursor.execute(statement)
        for(foodtypeId, foodType) in mdbc.cursor:
            print(f"[{foodtypeId}] {foodType}")
    
        searchChoice = int(input(("Which food type would you like to search? ")))
        print("\n")
            
        #Executes search
        statement = "SELECT * from fooditem WHERE itemid in (SELECT itemid from fooditemtype WHERE foodtypeId = %s)"
        data = (searchChoice,)
        mdbc.cursor.execute(statement, data)
        for(itemId, name, price, description, establishmentId) in mdbc.cursor:
            print(f"[{itemId}] {name} - {price} - {description} - {establishmentId}")

        choice = input("Which food item do you want to view?: ")
        result = getFoodItemId(choice)
        if result != 0:
            return result

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

def viewUserReviews(username):
    try:
        print("/n")
        print("***** {username}'s Reviews *****")

        #Prints user's food item reviews
        print("-- Food Item Reviews --")
        statement = "SELECT reviewId, rating, comment, date_reviewed, itemId FROM review WHERE username=%s AND itemId IS NOT null"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        for(reviewId, rating, comment, date_reviewed, itemId) in mdbc.cursor:
            print(f"[{reviewId}] {rating} - {comment} - {date_reviewed} - {itemId}")

        #Prints user's establishment reviews
        print("-- Food Establsihment Reviews --")
        statement = "SELECT reviewId, rating, comment, date_reviewed, establishmentId FROM review WHERE username=%s AND establishmentId IS NOT null"
        data = (username,)
        mdbc.cursor.execute(statement, data)
        for(reviewId, rating, comment, date_reviewed, establishmentId) in mdbc.cursor:
            print(f"[{reviewId}] {rating} - {comment} - {date_reviewed} - {establishmentId}")

    except mdbc.database.Error as e:
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
                mdbc.cursor.execute(statement, data)
            elif updChoice == 2:
                updComment = input("New comment: ")
                statement = "UPDATE review SET comment=%s WHERE reviewid = %s"
                data = (updComment, updId)
                mdbc.cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to update review [y/n]? ")
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
        return 0
    except mdbc.database.Error as e:
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
            mdbc.cursor.execute(statement, data)
            mdbc.connection.commit()
            print("Successfully deleted!")
            return 1
        elif confirm == 'n':
            print("Cancelled delete!")
            return 0

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

        
def userActionsLoop(username):
    while True:
        userMenuChoice = userMenu()

        if userMenuChoice == 1:
            estabChoice = foodEstabActions()
            while True:
                if estabChoice == 1:
                    #result =
                    searchFoodEstab() #returns foodEstabId to be used to redirect to food estab page
                elif estabChoice == 2:
                    result = viewAllFoodEstab() #returns foodEstabId to be used to redirect to food estab page
                    foodEstablishmentPage(result, username)
                elif estabChoice == 3:
                    #result =
                    viewByHighRating() #returns foodEstabId to be used to redirect to food estab page
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
                    #result =
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
                    updateReview()
                elif reviewChoice == 3:
                    deleteReview()
                elif reviewChoice == 0:
                    break
                else:
                    print("Option does not exist. Please try again!")
        elif userMenuChoice == 0:
            break
        else:
            print("Option does not exist. Please try again!")