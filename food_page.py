# * 4. Specific Food Item functions

import mdb_connector as mdbc

MONTHS = {
    "January": "01", "February": "02", "March": "03", "April": "04",
    "May": "05", "June": "06", "July": "07", "August": "08",
    "September": "09", "October": "10", "November": "11", "December": "12"
}

# retrieving all food reviews
def allFoodReviews(itemId):
    foodReviews = getAllFoodReviews(itemId)

    if len(foodReviews) > 0:
        for x in foodReviews:
            print("-------------------")
            print("")
            print(f"Username:   {x[3]}")
            print(f"Rating:     {x[0]}/5.0")
            print(f"Comment:    {x[1]}")
            print(f"Published:  {x[2]}")
            print("")

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

def getAllFoodReviews(itemId):
    reviews = list()

    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE itemId=%s"
        data = (itemId,)
        mdbc.cursor.execute(statement, data)
        for (rating, comment, date_reviewed, username) in mdbc.cursor:
            review = (rating, comment, date_reviewed, username)
            reviews.append(review)
    except mdbc.database.Error as e:
        print(f"Error retrieving entry from database: {e}")
    
    return reviews

# Retrieving Food item's name
def getFoodItemName(itemId):
    try:
        statement = "SELECT name FROM fooditem WHERE itemId = %s"
        data = (itemId,)
        mdbc.cursor.execute(statement, data)
        result = mdbc.cursor.fetchone()
        if result:
            return result[0]
        else:
            print("Food item not found!")
            return None
    except mdbc.database.Error as e:
        print(f"Error retrieving food item name from database: {e}")
        return None
    
# View all reviews made within a month for a food item
def recentFoodReviews(itemId):
    month = input("Enter the month (e.g., January, February, etc.) to view reviews: ")
    month_num = MONTHS.get(month.capitalize())
    
    if not month_num:
        print("Invalid month! Please enter a valid month name.")
        return

    reviews = list()

    try:
        statement = "SELECT rating, comment, date_reviewed, username FROM review WHERE itemId=%s AND MONTH(date_reviewed) = %s"
        data = (itemId, month_num)
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

# Add Food review
def addFoodReview(itemId, username):

    print("\n")
    try:
        rating = float(input("Enter rating (0.0 to 5.0): "))
        if rating < 0.0 or rating > 5.0:
            print("Invalid rating! Must be between 0.0 and 5.0.")
            return

        comment = input("Enter your comment (max 100 characters): ")
        if len(comment) > 100:
            print("Comment too long! Max 100 characters.")
            return

        statement = "INSERT INTO review (rating, comment, date_reviewed, username, itemId) VALUES (%s, %s, NOW(), %s, %s)"
        data = (rating, comment, username, itemId)
        mdbc.cursor.execute(statement, data)
        mdbc.connection.commit()

        print("Review added successfully!")
        print("")
    except mdbc.database.Error as e:
        print(f"Error adding review to database: {e}")
    except ValueError:
        print("Invalid input! Please enter the correct data types.")

# Food Page 
def focusedFoodItemPage(itemId, username):
    name = getFoodItemName(itemId)
    if not name:
        return

    while True:
        print("\n")
        print("*****    FOOD ITEM:  *****")
        print(f"----- {name} -----")
        choice = focusedFoodItemMenu()

        if choice == 0:
            break
        elif choice == 1:
            print("\n")
            print(f"****** REVIEWS FOR {name} *****")
            allFoodReviews(itemId)
        elif choice == 2:
            print("\n")
            recentFoodReviews(itemId)
        elif choice == 3:
            addFoodReview(itemId, username)
        else:
            print("Invalid choice!")

def focusedFoodItemMenu():
    print("")
    print("[1] View all reviews")
    print("[2] View reviews in a specific month")
    print("[3] Review this food item")
    print("[0] Back")
    print("")

    while True:
        try:
            page_choice = int(input("Select an action: "))
            return page_choice
        except ValueError:
            print("Invalid input! Please enter a number.")