# 3. Food Establishment Page Group

# * Import statements
import mysql.connector as database
import main

connection = main.connection
cursor = main.cursor


# * functions ----------

# ? DB functions ----------
def getAllFoodItems(estabId):
    items = list()

    try:
        # ? Changed to access user table from locally created projectdb
        statement = "SELECT itemId, name, price, desription FROM fooditem WHERE estabId=%s"
        data = (estabId,)
        cursor.execute(statement, data)
        for(itemId, name, price, description) in cursor:
            item = tuple((itemId, name, price, description))
            items.append(item)

    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return items


def getAllFoodReviews(itemId):
    reviews = list()

    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE itemId=%s"
        data = (itemId,)
        cursor.execute(statement, data)
        for(rating, comment, data_reviewed, username) in cursor:
            review = tuple((rating, comment, data_reviewed, username))
            reviews.append(review)
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews


def getAllEstabReviews(estabId):
    reviews = list()
    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE estabId=%s"
        data = (estabId,)
        cursor.execute(statement, data)
        for(rating, comment, data_reviewed, username) in cursor:
            review = tuple((rating, comment, data_reviewed, username))
            reviews.append(review)
    except database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews


# sorted gets




# * 3a. All Food item Functions ----------
# should receive estabid to search all food items of establishment
def allFoodItems(estabId):
    foodItems = getAllFoodItems(estabId)

    print("Food items of <EstabName>")

    if(len(foodItems) > 0 ):
        # print all food items
        i=1
        for x in foodItems:
            print(f"[{i}] {x[1]}")   # prints food name
            i+=1
        print("[0] Back")

        choice = int(input("Select a food item: "))
        if(choice == 0):
            selectedIdentifier = 0
        else:
            selectedIdentifier = foodItems[choice-1][0]

        return selectedIdentifier

    else:
        print("No food items found!")


def allFoodItemsMenu(estabId):
    while True:
        choice = allFoodItems(estabId)

        if(choice == 0):
            break
        else:
            focusedFoodItemPage(choice)



# * 3b. Functions ----------


# * 3c. Functions ----------


# * 3d. Establishment reviews Functions ----------
def allEstabReviews(estabId):
    estabReviews = getAllEstabReviews(estabId)

    print("Reviews for <Estab Name>")

    if(len(estabReviews) > 0):
        for x in estabReviews:
            print("-------------------")
            print(f"Sender:     {x[3]}")
            print(f"Rating:     {x[0]}")
            print(f"{x[1]}")
            print(f"Published:  {x[2]}")

        print("[0] Back")

        # ? Implementation Notes: Prompt user if they want to return, on input of invalid value, it does not print all of the reviews again, for readability idk
        while True:
            choice = int(input("Return? "))
            if(choice == 0):
                break
            else:
                print("Invalid choice!")
        return



# * 3e. Functions ----------



# * 4. Specific Food Item functions ----------
# TODO/Option: Put this section in a separate file
def allFoodReviews(itemId):
    foodReviews = getAllFoodReviews(itemId)

    print("Reviews for <Food item Name>")

    if(len(foodReviews) > 0):
        # i=0
        for x in foodReviews:
            print("-------------------")
            print(f"Sender:     {x[3]}")
            print(f"Rating:     {x[0]}")
            print(f"{x[1]}")
            print(f"Published:  {x[2]}")

        print("[0] Back")

        # ? Implementation Notes: Prompt user if they want to return, on input of invalid value, it does not print all of the reviews again, for readability idk
        while True:
            choice = int(input("Return? "))
            if(choice == 0):
                break
            else:
                print("Invalid choice!")
        return
    else:
        print("No reviews found!")


def focusedFoodItemMenu():
    print("[1] View all reviews")
    print("[2] View recent reviews")
    print("[3] Review this food item")
    print("[0] Back")

    page_choice = int(input("Select an action: "))

    return page_choice


def focusedFoodItemPage(itemId):
    while True:
        print("<Food item Name>")
        choice = focusedFoodItemMenu()

        if(choice == 0):
            break
        elif(choice == 1):
            # redirect to display all food reviews for this item
            allFoodReviews(itemId)
            
        elif(choice == 2):
            # TODO: redirect to dislpay recent food reviews only
            pass
        elif(choice == 3):
            # TODO: redirect to add a review
            pass
        else:
            print("Invalid choice!")


    




# * 3. Food Establishment functions ----------
def foodEstabMenu():
    print("Establishment location: <location>")
    print(" [1] View all food items")
    print(" [2] View food items by food type")
    print(" [3] View food items sorted by price")
    print(" [4] View all establishment reviews")
    print(" [5] View recent establishment reviews")
    print(" [6] Review this establishment")
    print(" [0] Back")

    page_choice = int(input("Select an action: "))

    return page_choice

# ? What should this receive?
# TODO: Provide args - food establishment id and details when calling this from Section 2
def foodEstablishmentPage():
    while True:
        print("<Establishment Name> Details")
        choice = foodEstabMenu()

        if(choice == 0):
            print("Returning...")
            break

        elif(choice == 1):
            # redirect to view all food items
            # TODO: Pass id to func here
            # allFoodItemsMenu()
            pass

        elif(choice == 2):
            # TODO: redirect to view of sorted food items
            # Essentially just like choice 1, but modify SQL statement
            pass

        elif(choice == 3):
            # TODO: redirect to view of sorted food items
            # Essentially just like choice 1, but modify SQL statement
            pass

        elif(choice == 4):
            # TODO: redirect to view of all estab reviews
            # TODO: Pass id to func here
            # allEstabReviews()
            pass

        elif(choice == 5):
            # TODO: redirect to view of recent estab reviews
            # Essentially just like choice 1, but modify SQL statement
            pass

        elif(choice == 6):
            # TODO: redirect to input of adding a review
            pass


        else:
            print("Invalid choice!")

        

