from utils import TaoBinApp
from datetime import datetime

app = TaoBinApp()
while True:
    app.print_welcome()
    action = int(input(": "))
    if action == 0:
        break
    elif action == 1:
        keyword = input("Please input a keyword to search: ")
        app.search_menus(keyword)
    elif action == 2:
        keyword = input("Please input a keyword to search: ")
        app.search_location(keyword)
    elif action == 3:
        input_date = input("Please specify date (dd/mm/yyyy): ").split('/')
        date = datetime(int(input_date[2]), int(input_date[1]), int(input_date[0]))
        app.calc_income(date)
    elif action == 4:
        keyword = input("Search your cup: ")
        menu_list = app.search_menus(keyword)
        select = int(input("\nPlease select your cup number: "))
        menu_id = menu_list[select-1]["_id"]
        can_be_smoothie = bool(menu_list[select-1]["CanSmoothie"])
        smoothie_price = int(menu_list[select-1]["SmoothieExtraPrice"])
        can_extra_espresso = bool(menu_list[select-1]["CanExtraEspresso"])
        extra_espresso_price = int(menu_list[select-1]["ExtraEspressoPrice"])
        sweetness = app.get_sweetness()
        select = int(input("Please select your sweetness level: "))
        sweetness_id = sweetness[select-1]["_id"]
        if can_be_smoothie:
            select = input(f"Do you want smoothie? +{smoothie_price} baht (y/n): ").lower()
            if select == 'y':
                is_smoothie = True
            else:
                is_smoothie = False
        else:
            is_smoothie = False
        if can_extra_espresso:
            select = input(f"Do you want to add extra Espresso? +{extra_espresso_price} baht (y/n): ").lower()
            if select == 'y':
                extra_espresso = True
            else:
                extra_espresso = False
        else:
            extra_espresso = False
        select = input("Do you want to get a straw? (y/n): ").lower()
        if select == 'y':
            get_straw = True
        else:
            get_straw = False
        select = input("Do you want to get a lid? (y/n): ").lower()
        if select == 'y':
            get_lid = True
        else:
            get_lid = False
        while True:
            print("\nPlease select your payment method...")
            payment_list = app.print_payments()
            select = int(input(": "))
            if select < len(payment_list) and select > 0:
                break
            print("Incorrect input, please try again...")
        payment_id = payment_list[select-1]["_id"]
        phone = input("Please input your phone number: ")
        customer = app.get_customer_by_phone(phone)
        if customer is None:
            select = input("It seems you're a new customer, do you want to create account? (y/n): ")
            if select == 'y':
                result = app.create_account(phone=phone)
                customer_id = str(result[0])
            else:
                customer_id = None
        else:
            customer_id = customer['_id']
        result = app.create_transaction(menu_id, customer_id, "6273e291c32200d884246530", sweetness_id, is_smoothie, extra_espresso, get_straw, get_lid, payment_id)
    elif action == 5:
        break
    print("\n\n")