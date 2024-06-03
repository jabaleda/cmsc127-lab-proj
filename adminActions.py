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

def updateFoodEstab():
    try:
        print("/n")
        print("***** Update A Food Establishment *****")

        updId = input("Input establishmentId: ")
        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Location")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE foodestablishment SET name=%s WHERE establishmentid = %s"
                data = (updName, updId,)
                cursor.execute(statement, data)
            elif updChoice == 2:
                updLocation = input("New location: ")
                statement = "UPDATE foodestablishment SET location=%s WHERE establishmentid = %s"
                data = (updLocation, updId,)
                cursor.execute(statement, data)
            elif updChoice == 0:
                confirm = input("Are you sure you want to update food establishment [y/n]? ")
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


def deleteFoodEstab():
    try:
        print("/n")
        print("***** Delete A Food Establishment *****")

        delId = input("Input establishmentId: ")

        confirm = input("Are you sure you want to delete food establishment [y/n]? ")
        if confirm == 'y':
            statement = "DELETE from foodestablishment WHERE establishmentId =%s"
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

def updateFoodItem():
    try:
        print("/n")
        print("***** Update A Food Item *****")

        updId = input("Input itemId: ")
        
        typeCount = 0
        while True:
            print("What do you want to update?")
            print("[1] Name")
            print("[2] Price")
            print("[3] Description")
            print("[3] Food Type")
            print("[0] Done Updating")

            updChoice = int(input("Option: "))

            if updChoice == 1:
                updName = input("New name: ")
                statement = "UPDATE fooditem SET name=%s WHERE itemId = %s"
                data = (updName, updId,)
                cursor.execute(statement, data)
            elif updChoice == 2:
                updPrice = input("New price: ")
                statement = "UPDATE fooditem SET price=%s WHERE itemId = %s"
                data = (updPrice, updId,)
                cursor.execute(statement, data)
            elif updChoice == 3:
                updDescription = input("New description: ")
                statement = "UPDATE fooditem SET description=%s WHERE itemId = %s"
                data = (updDescription, updId),
                cursor.execute(statement, data)
            elif updChoice == 4:
                if typeCount == 0:
                    # statement = "SAVEPOINT delfoodtype"
                    # cursor.execute(statement)
                    statement = "DELETE from fooditemtype where itemId = %s"
                    data = (updId,)
                    cursor.execute(statement, data)
                updType = input("New food type: ")
                statement = "INSERT INTO fooditemtype(itemId, foodtypeId) VALUES (%s, %s)"
                data = (updId, updType,)
                cursor.execute(statement, data)
                typeCount = typeCount + 1
            elif updChoice == 0:
                confirm = input("Are you sure you want to update food item [y/n]? ")
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


def deleteFood():
    try:
        print("/n")
        print("***** Delete A Food Item *****")

        delId = input("Input itemId: ")

        confirm = input("Are you sure you want to delete food item [y/n]? ")
        if confirm == 'y':
            statement = "DELETE from fooditem WHERE itemId =%s"
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

# def adminActionsLoop()
#     while True:
#         adminMenuChoice = userMenu()

#         if adminMenuChoice == 1:
#             estabChoice = foodEstabActions()
#             while True:
#                 if estabChoice == 1:
#                     #result =
#                     searchFoodEstab() #returns foodEstabId to be used to redirect to food estab page
#                 elif estabChoice == 2:
#                     #result =
#                     viewAllFoodEstab() #returns foodEstabId to be used to redirect to food estab page
#                 elif estabChoice == 3:
#                     #result =
#                     viewByHighRating() #returns foodEstabId to be used to redirect to food estab page
#                 elif estabChoice == 0:
#                     break
#                 else:
#                     print("Option does not exist. Please try again!")
#         elif adminMenuChoice == 2:
#             while True:
#                 foodChoice = foodItemActions()

#                 if foodChoice == 1:
#                     #result =
#                     searchFoodByPriceRange()
#                 elif foodChoice == 2:
#                     #result =
#                     searchFoodByFoodType()
#                 elif foodChoice == 0:
#                     break
#                 else:
#                     print("Option does not exist. Please try again!")
#         elif adminMenuChoice == 3:
#             while True:
#                 reviewChoice = userReviewActions()

#                 if reviewChoice == 1:
#                     viewUserReviews(username)
#                 elif reviewChoice == 2:
#                     updateReview()
#                 elif reviewChoice == 3:
#                     deleteReview()
#                 elif reviewChoice == 0:
#                     break
#                 else:
#                     print("Option does not exist. Please try again!")
#         elif adminMenuChoice == 0:
#             break
#         else:
#             print("Option does not exist. Please try again!")
        