from unittest.mock import NonCallableMagicMock
from connection import ConnectDatabase
from datetime import datetime, timedelta
from bson.objectid import ObjectId
import pprint
from math import floor

class TaoBinApp:
    def __init__(self) -> None:
        self.__db = ConnectDatabase()

    def search_menus(self, keyword):
        # Search by name directly and category with case-insensitive query
        col = self.__db.get_collection("menus").find({"$or":[ {"Name": {'$regex': keyword, '$options': 'i'}}, {"Genre": {'$regex': keyword, '$options': 'i'}}]})
        searched_list = list(col)
        print(f"{'Name':^40}|{'Price':^10}")
        print(f"{'-'*51}")
        for index, item in enumerate(searched_list, 1):
            print(f"{str(index)+'. '+item['Name']:<40}|{str(item['BasePrice'])+'.-':^10}")
        return searched_list
    
    def search_location(self, keyword):
        # Search by name directly and category with case-insensitive query.
        col = self.__db.get_collection("locations").find({"$or":[ {"Location Name": {'$regex': keyword, '$options': 'i'}}, {"City": {'$regex': keyword, '$options': 'i'}}]}, {"_id": 0, "Location Name": 1, "City": 1})
        for index, item in enumerate(col, 1):
            print(f"{index}. {item['Location Name']} - {item['City']}")

    def calc_income(self, date: datetime):
        """Calculate income for a specific date."""
        start_date = date
        end_date = date + timedelta(days=1)
        pipeline = [{
            "$match": {
                "$and": [
                    {"Timestamp": {'$lt': end_date}},
                    {"Timestamp": {'$gte': start_date} }
                ]}}, {"$group": {"_id": 0, "sum": {"$sum": "$Price"}}}]
        total_income = self.__db.get_collection("transactions").aggregate(pipeline)
        print(f"Income for {date.day}/{date.month}/{date.year} is", list(total_income)[0]['sum'], 'baht')
        action = input("Do you want to see details (y/n)? ").lower()
        if action != 'y':
            return
        col = self.__db.get_collection("transactions").find({"Timestamp": {'$lt': end_date, '$gte': start_date}})
        print(f"{'Name':^40}|{'Price':^10}")
        print(f"{'-'*51}")
        for index, item in enumerate(col, 1):
            # Get Menu Information from another collection
            menu = self.__db.get_collection("menus").find_one({"_id": ObjectId(item['MenuID'])}, {"_id": 0, "Name": 1})
            print(f"{str(index)+'. '+menu['Name']:<40}|{str(item['Price'])+'.-':^10}")

    def create_transaction(self, menu_id, customer_id, location_id, sweetness_id, isSmoothie, getExtraEspresso, getStraw, getLid, payment_id):
        """Create a new order."""
        order_time = datetime.now()
        # Get price and additional information by menu id
        menu = self.__db.get_collection("menus").find_one({"_id": ObjectId(menu_id)})
        customer = self.__db.get_collection("customers").find_one({"_id": ObjectId(customer_id)})
        price = menu['BasePrice']
        print("Order Information...")
        print(f"Menu: {menu['Name']}")
        print(f"Price: {menu['BasePrice']}")
        if isSmoothie:
            print(f"Smoothie: +{menu['SmoothieExtraPrice']} baht")
            price += menu['SmoothieExtraPrice']
        if getExtraEspresso:
            print(f"Extra Espresso Shot +{menu['ExtraEspressoPrice']} baht")
            price += menu['ExtraEspressoPrice']
        print(f"Total price: {price} baht")
        points = floor(price/15)
        confirm = input("Confirm (y/n)? ").lower()
        if confirm == 'y':
            result = self.__db.insert("transactions", [{
                "Timestamp": order_time,
                "CustomerID": customer_id,
                "LocationID": location_id,
                "MenuID": menu_id,
                "SweetnessID": sweetness_id,
                "IsSmoothie": isSmoothie,
                "GetExtraEspresso": getExtraEspresso,
                "GetStraw": getStraw,
                "GetLid": getLid,
            }])
            print("Order successfully created")
            if customer is not None:
                current_points = customer['Points']
                print(f"+{points} points for {customer['Firstname']} {customer['Lastname']}")
                update_points = {"$set": {"Points": current_points+points}}
                self.__db.get_collection("customers").update_one({"_id": ObjectId(customer_id)}, update_points)
                customer = self.__db.get_collection("customers").find_one({"_id": ObjectId(customer_id)})
                print(f"your current points: {customer['Points']}")


    def create_account(self, first_name=None, last_name=None, gender=None, birthday=None, phone=None):
        """Create new customer account"""
        fill_info = False
        temp_first_name = first_name
        temp_last_name = last_name
        temp_gender = gender
        temp_birthday = birthday
        temp_phone = phone
        while True:
            if phone == None:
                fill_info = True
                phone = input("Please input your phone number: ")
            if first_name == None:
                fill_info = True
                first_name = input("Please input your first name: ")
            if last_name == None:
                fill_info = True
                last_name = input("Please input your first name: ")
            if gender == None:
                fill_info = True
                gender_list = ["", "Male", "Female", "Other"]
                while True:
                    gender_id = int(input("Please select your gender...\n(1) Male\n(2) Female\n(3) Other\n: "))
                    if gender_id < len(gender_list) and gender_id > 0:
                        break
                    print("Incorrect input. Please try again...")
                gender = gender_list[gender_id]
            if birthday == None:
                fill_info = True
                birthdate = input("Please input your birthday in format dd/mm/yyyy in A.D.: ")
                birth = birthdate.split('/')
                birthday = datetime(int(birth[2]), int(birth[1]), int(birth[0]))
            if not fill_info:
                break
            print(f"Please check your information...\nName: {first_name} {last_name}\nGender: {gender}\nPhone: {phone}\nbirthday: {birth[0]}/{birth[1]}/{birth[2]}\n")
            confirm = input("Confirm (y/n)? ").lower()
            if confirm == 'y':
                break
            first_name = temp_first_name
            last_name = temp_last_name
            gender = temp_gender
            birthday = temp_birthday
            phone = temp_phone
        result = self.__db.insert("customers", [{
            "Firstname": first_name,
            "Lastname": last_name,
            "Gender": gender,
            "Birthday": birthday,
            "Phone": phone,
            "Points": 0
        }])
        print(f"Successfully created account: {first_name} {last_name}\n")
        return result

    def get_sweetness(self):
        """Get all sweetness levels."""
        col = self.__db.get_collection("sweetness").find({})
        searched_list = list(col)
        for index, i in enumerate(searched_list, 1):
            print(f"({index}) {i['Sweetness']}")
        return searched_list

    def print_payments(self):
        col = self.__db.get_collection("paymentType").find({})
        searched_list = list(col)
        for index, i in enumerate(searched_list, 1):
            print(f"({index}) {i['Name']}")
        return searched_list

    def get_customer_by_phone(self, phone_number):
        col = self.__db.get_collection("customers").find_one({"Phone": phone_number})
        return col

    def print_welcome(self):
        """Print welcome text."""
        print("Welcome to TaoBin roboic coffee machine.")
        print("Please select your action...")
        print("(1) Find your cup")
        print("(2) Find TaoBin")
        print("(3) Calculate income on a specific date")
        print("(4) Create new order")
        print("(5) Calculate new worth on a specific month")
        print("(0) Terminate program")
