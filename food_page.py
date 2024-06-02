import mdb_connector as mdbc
from estab_page import *

# * 4. Specific Food Item functions ----------
def allFoodReviews(itemId):
    foodReviews = getAllFoodReviews(itemId)

    if len(foodReviews) > 0:
        for x in foodReviews:
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

def focusedFoodItemPage(itemId):
    # Assuming itemTuple contains itemId, name, price, description
    # name is already retrieved from the item selection function
    name = "Food Item Name Placeholder"  # Replace this with actual name retrieval if needed

    while True:
        print(f"--- FOOD ITEM: {name} ---")
        choice = focusedFoodItemMenu()

        if choice == 0:
            break
        elif choice == 1:
            print("\n")
            print(f"Reviews for {name}")
            allFoodReviews(itemId)
        elif choice == 2:
            # redirect to display recent food reviews only
            # Implement if needed
            pass
        elif choice == 3:
            # redirect to add a review
            # Implement if needed
            pass
        else:
            print("Invalid choice!")

def focusedFoodItemMenu():
    print("\n")
    print("[1] View all reviews")
    print("[2] View recent reviews")
    print("[3] Review this food item")
    print("[0] Back")

    while True:
        try:
            page_choice = int(input("Select an action: "))
            return page_choice
        except ValueError:
            print("Invalid input! Please enter a number.")