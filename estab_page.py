# 3. Food Establishment Page Group

# * Import statements
# Changed import statement from main to only access the cursor
# from main import cursor
import mdb_connector as mdbc


# * functions ----------

# ? DB functions ----------
def getAllFoodItems(estabId):
    items = list()

    try:
        # ? Changed to access user table from locally created projectdb
        statement = "SELECT itemId, name, price, desription FROM fooditem WHERE estabId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for(itemId, name, price, description) in mdbc.cursor:
            item = tuple((itemId, name, price, description))
            items.append(item)

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return items


def getAllFoodReviews(itemId):
    reviews = list()

    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE itemId=%s"
        data = (itemId,)
        mdbc.cursor.execute(statement, data)
        for(rating, comment, data_reviewed, username) in mdbc.cursor:
            review = tuple((rating, comment, data_reviewed, username))
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews

# * NEW ----------
def getRecentEstabReviews(estabId):
    recentReviews = list()

    try:
        # ! Please recheck the SQL Statement hahjshusfhj
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE estabId=%s AND DATEDIFF(CURDATE(), date_reviewed)"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for(rating, comment, data_reviewed, username) in mdbc.cursor:
            review = tuple((rating, comment, data_reviewed, username))
            recentReviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving from database: {e}")

    return recentReviews
        

def getAllEstabReviews(estabId):
    reviews = list()
    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE estabId=%s"
        data = (estabId,)
        mdbc.cursor.execute(statement, data)
        for(rating, comment, data_reviewed, username) in mdbc.cursor:
            review = tuple((rating, comment, data_reviewed, username))
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews

# sorted
def sortFoodItemsbyPrice( estabId, sort ):
    sortedItems = list()
    try:
        statement = "SELECT itemId, name, price, description FROM fooditem WHERE estabId=%s ORDER BY price %s"
        data = (estabId, sort)
        mdbc.cursor.execute(statement, data)
        for(itemId, name, price, description) in mdbc.cursor:
            item = tuple((itemId, name, price, description))
            sortedItems.append(item)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return sortedItems

# filter by type
def getAllFoodTypes():
    types = list()
    try:
        statement = "SELECT foodtypeId, foodType FROM fooditemtype"
        mdbc.cursor.execute(statement)
        for(foodtypeId, foodtype) in mdbc.cursor:
            type = tuple((foodtypeId, foodtype))
            types.append(type)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    return types

def filterFoodItemsbyType( estabId, typeId ):
    itemsInType = list()
    try:
        # ! Please recheck the SQL Statement hajhsdjsk
        statement = "SELECT DISTINCT itemId, name FROM fooditem NATURAL JOIN fooditemtype WHERE estabId=%s AND foodtypeId=%s"
        data = (estabId, typeId)
        mdbc.cursor.execute(statement, data)
        for(itemId, name) in mdbc.cursor:
            item = tuple((itemId, name))
            itemsInType.append(item)

    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")

    return itemsInType


def addToEstabReviewDB(reviewTuple):
    estabId = reviewTuple[0]
    username = reviewTuple[1]
    rating = reviewTuple[2]
    comment = reviewTuple[3]

    try:
        # ! Please recheck the SQL Statement ajskhjf
        statement = "INSERT INTO review (rating, comment, date_reviewed, username, establismentId) VALUES (%s, %s, CURDATE(), %s, %s)"
        data = (rating, comment, username, estabId)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()
        print("Successfully added a review!")
    except mdbc.database.Error as e:
        print(f"Error adding review: {e}")



# * 3a. All Food item Functions ----------
# should receive estabid to search all food items of establishment
def allFoodItems( estabId ):
    foodItems = getAllFoodItems(estabId)

    print("---------- FOOD ITEMS ----------")

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
            return selectedIdentifier
        else:
            selectedFoodItem = foodItems[choice-1]      # tuple
            return selectedFoodItem

    else:
        print("No food items found!")
        return


def allFoodItemsMenu( estabId ):
    while True:
        choice = allFoodItems(estabId)

        if(choice == 0):
            break
        else:
            # pass the tuple of selected food item
            focusedFoodItemPage(choice)
    return


# * 3b. Filtered by Food Type Functions ----------

def allFoodItemsbyType(estabId, typeId):
    filteredItems = filterFoodItemsbyType(estabId, typeId)
    print("---------- FOOD ITEMS ----------")

    if(len(filteredItems) > 0 ):
        # print all food items
        i=1
        for x in filteredItems:
            print(f"[{i}] {x[1]}")   # prints food name
            i+=1
        print("[0] Back")

        while True:
            choice = int(input("Select a food item: "))
            if(choice == 0):
                break
            elif(choice < 0 or choice > i):
                print("Invalid choice!")
            else:
                focusedFoodItemPage(filteredItems[choice-1][0])

    else:
        print("No food items found!")
        return


def foodTypesMenu():
    types = getAllFoodTypes()
    print("--- Food Types ---")
    i=1
    for x in types:
        print(f"[{i} {x[1]}]")
        i+=1
    print("[0] Back")

    while True:
        choice = int(input("Select a type: "))
        if(choice == 0):
            return choice
        elif(choice < 0 or choice > i):
            print("Invalid choice!")
        else:
            return types[choice-1][0]       # returns the foodtypeId


def filterFoodItemsbyTypePage( estabId ):
    print("\n")
    print("--- View food items by Type ---")
    while True:
        choice = foodTypesMenu(estabId)
        if(choice == 0):
            break
        else:
            allFoodItemsbyType(estabId, choice)
            pass
            # go to display all food items belonging to that type

    
# * 3c. Sort Food Items by PriceFunctions ----------

def allFoodItemsbyPrice( estabId, sort ):
    sortedFoodItems = sortFoodItemsbyPrice( estabId, sort )

    if(len(sortedFoodItems) > 0):
        i=1
        for x in sortedFoodItems:
            print(f"[{i}] {x[1]}")  # prints food name
            i+=1
        
        print("[0] Back")

        choice = int(input("Select a food item: "))
        if(choice == 0):
            selectedIdentifier = 0
        else:
            selectedIdentifier = sortedFoodItems[choice-1]          # tuple

        return selectedIdentifier

    else:
        print("No food items found!")


def allFoodItemsbyPriceMenu( estabId, sort):
    while True:
        choice = allFoodItemsbyPrice(estabId, sort)

        if(choice == 0):
            break
        else:
            focusedFoodItemPage(choice)
    return


def sortSelectFoodItemsbyPriceMenu():
    print("\n")
    print("[1] Ascending")
    print("[2] Descending") 
    print("[0] Back")

    page_choice = int(input("Select an action: "))

    return page_choice


def sortSelectFoodItemsbyPricePage( estabId ):
    while True:
        choice = sortSelectFoodItemsbyPriceMenu()

        if(choice == 0):
            break
        elif(choice == 1):
            print("Food Items sorted by Price - Ascending")
            # display sorted by price - asc
            allFoodItemsbyPriceMenu(estabId, "asc")

            pass
        elif(choice == 2):
            print("Food Items sorted by Price - Ascending")
            # display sorted by price - desc
            allFoodItemsbyPriceMenu(estabId, "desc")
            pass
        else: 
            print("Invalid choice!")



# * 3d. Establishment reviews Functions ----------
def allEstabReviews( estabId ):
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
    else:
        print("No reviews found!")
        return


# * 3e. View recent establishment reviews ----------
def recentEstabReviews(estabId):
    recentReviews = getRecentEstabReviews(estabId)
    
    if len(recentEstabReviews) > 0:
        for x in recentReviews:
            print("-------------------")
            print(f"Sender:     {x[3]}")
            print(f"Rating:     {x[0]}")
            print(f"{x[1]}")
            print(f"Published:  {x[2]}")

        print("[0] Back")

        while True:
            choice = int(input("Return? "))
            if choice == 0:
                break
            else:
                print("Invalid choice!")

    else:
        print("No reviews found!")
        return


# * 3f. Add an Estab. Review Functions ----------
def addAReview( estabId, username):
    print("\n")
    print("Leave a review")
    
    rating = int(input("Rating (On a scale of 1-5): "))
    comment = int(input("Leave a comment: "))

    # reviewDetails = tuple((rating, comment))

    while True:
        print("Publish review?")
        print("[1] Yes")
        print("[2] No")

        choice = int(input("Select: "))
        if choice == 1:
            reviewDetails = (estabId, username, rating, comment)
            # save to db
            addToEstabReviewDB(reviewDetails)
            return
        
        elif choice == 2:
            print("Review cancelled. Returning...")
            return 
        else:
            print("Invalid choice!")


# * 3. Food Establishment functions ----------
def foodEstabMenu():
    print("\n")
    print("Establishment location: <location>")                         # ? This can be printed on select of an establishment, before calling this function instead so this function only needs the estabId
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
# TODO: Provide args - username, food establishment id, details when calling this from Section 2
def foodEstablishmentPage( estabId, username ):
    while True:
        print("<Establishment Name> Details")                           # ? This can be printed on select of an establishment, before calling this function instead so this function only needs the estabId
        choice = foodEstabMenu()

        if(choice == 0):
            print("Returning...")
            mdbc.connection.close()
            break

        elif(choice == 1):
            # redirect to view all food items
            # Pass id to func here
            allFoodItemsMenu(estabId)
            

        elif(choice == 2):
            # redirect to view of sorted food items
            # Essentially just like choice 1, but modify SQL statement
            sortSelectFoodItemsbyPricePage(estabId)

        elif(choice == 3):
            # redirect to view of sorted food items
            # Essentially just like choice 1, but modify SQL statement
            sortSelectFoodItemsbyPricePage(estabId)

        elif(choice == 4):
            # redirect to view of all estab reviews
            # Pass id to func here
            allEstabReviews(estabId)
            
        elif(choice == 5):
            # TODO: redirect to view of recent estab reviews
            # Essentially just like choice 1, but modify SQL statement
            pass

        elif(choice == 6):
            # redirect to input of adding a review
            addAReview(estabId, username)
            pass


        else:
            print("Invalid choice!")



# * 4. Specific Food Item functions ----------
# TODO/Optional: Put this section in a separate file
def allFoodReviews( itemId ):
    foodReviews = getAllFoodReviews(itemId)

    if(len(foodReviews) > 0):
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
    print("\n")
    print("[1] View all reviews")
    print("[2] View recent reviews")
    print("[3] Review this food item")
    print("[0] Back")

    page_choice = int(input("Select an action: "))

    return page_choice


def focusedFoodItemPage( itemTuple ):
    itemId = itemTuple[0]
    name = itemTuple[1]

    while True:
        print(f"--- FOOD ITEM: {name} ---")
        choice = focusedFoodItemMenu()

        if(choice == 0):
            break
        elif(choice == 1):
            print("\n")
            print(f"Reviews for {name}")
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
        

