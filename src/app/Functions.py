import database
import datetime


def log_in():
    login = input("Enter your nickname: ")
    password = input("Enter your password: ")
    user_id = 0
    user_type = 0
    for user in database.get_log_info():
        if login == user['user_login'] and password == user['user_password']:
            user_id = user['user_ID']
            user_type = user['user_type']

    if user_id != 0:
        print("Login was successful")
        return user_id, user_type
    else:
        print("Error, login failed")
        return user_id, user_type


def check_if_correct_number(name, length):
    while True:
        user_input = input(f"Enter your {name}: ")
        if len(user_input) != length:
            print(f"Wrong length of {name}: {len(user_input)}, should be {length}. Try again!")
            continue
        try:
            n = int(user_input)
        except ValueError:
            print("Entered value is not a number. Try again!")
            continue
        else:
            break
    return user_input


def register_user():
    user_name = input("Enter your name: ")
    user_surname = input("Enter your surname: ")
    user_email = input("Enter your email 'user@email.com': ")
    user_telephone = check_if_correct_number("phone number", 9)
    user_PESEL = check_if_correct_number("PESEL", 11)
    user_login = input("Enter your user name: ")
    user_password = input("Enter your password: ")
    user_type = 0

    database.add_user(user_name, user_surname, user_email, user_telephone, user_PESEL, user_login, user_password, user_type)


def list_hotels():
    print("List of all available hotels:")
    for hotel in database.get_all_hotels():
        print(f"\t{hotel['country_ID']} {hotel['location_city']} Hotel number: {hotel['hotel_ID']} Hotel name: {hotel['hotel_name']} ")


def list_room_types(hotel_id):
    room_types = database.get_room_types(hotel_id)
    print("\tTypes of rooms available in this hotel:")
    for room_type in room_types:
        print(f"\t - {room_type['room_type_ID']} '{room_type['room_type']}' - cost of a night: {room_type['room_type_price']}")


def list_all_rooms(hotel_id):
    rooms = database.get_all_rooms(hotel_id)
    print("\tList of rooms available in this hotel: ")
    for room in rooms:
        print(f"\t - Room number: {room['room_ID']} '{room['room_type']}' - cost of a night: {room['room_type_price']}")


def list_dining_options():
    dining_options = database.get_dining_options()
    print("\tDining options available in this hotel:")
    for dining_option in dining_options:
        print(f"\t - {dining_option['dining_option_ID']} {dining_option['dining_option_type']} - cost of service: {dining_option['dining_option_cost']}")


def list_payment_methods():
    payment_methods = database.get_payment_methods()
    print("\tPayment options available in this hotel:")
    for payment_method in payment_methods:
        discount = round((1 - payment_method['payment_method_discount'])*100)
        print(f"\t - {payment_method['payment_method_ID']} {payment_method['payment_method']} - amount of discount: {discount}%")


def hotel_info():
    hotel_id = choose_hotel()
    print("Here is more information about the hotel you chose:")
    hotel = database.get_hotel_address(hotel_id)
    print(f"\tHotel number: {hotel[0]['hotel_ID']}")
    print(f"\tName: {hotel[0]['hotel_name']}")
    print(f"\tCountry: {hotel[0]['country_name']}")
    print(f"\tCity: {hotel[0]['location_city']}")
    print(f"\tAddress: {hotel[0]['street_address']}")
    list_room_types(hotel_id)
    list_dining_options()
    list_payment_methods()


RESERVATION_MENU_INTERFACE = """
You are in reservation menu. 

Please decide what you want to do:
- 'fill' to start filling the reservation form.
- 'back' to back to the previous menu.
YOUR CHOICE: """


def calculate_cost(reservation_period, room_cost, dining_option_cost, payment_method_discount):
    return (reservation_period*room_cost + dining_option_cost)*payment_method_discount


def check_date_format(date_string, date_format):
    while True:
        try:
            datetime.datetime.strptime(date_string, date_format)
            print("This is the correct date format.")
        except ValueError:
            date_string = input("This is the incorrect date format. It should be YYYY-MM-DD: ")
            continue
        else:
            break
    return datetime.datetime.strptime(date_string, date_format), date_string


def choose_hotel():
    list_hotels()
    hotel_id = int(input("Enter the number of hotel from list above: "))
    hotels = database.get_all_hotels()
    searching = True
    while searching:
        for hotel in hotels:
            if hotel['hotel_ID'] == hotel_id:
                searching = False
                break
        if searching:
            list_hotels()
            hotel_id = int(input("Enter the proper hotel number from list above: "))
    return hotel_id


def choose_start_date(date_format):
    first_day = input("Enter first day of your reservation 'RRRR-MM-DD': ")
    first_day_obj, first_day = check_date_format(first_day, date_format)
    while True:
        if first_day_obj < datetime.datetime.now():
            first_day = input("The reservation may start at the earliest today 'RRRR-MM-DD': ")
            first_day_obj, first_day = check_date_format(first_day, date_format)
        else:
            break
    return first_day_obj


def choose_end_date(date_format, first_day_obj):
    last_day = input("Enter the last day of your reservation 'RRRR-MM-DD': ")
    last_day_obj, last_day = check_date_format(last_day, date_format)
    while True:
        if last_day_obj < first_day_obj:
            last_day = input("Reservation can not end before the first day 'RRRR-MM-DD': ")
            last_day_obj, last_day = check_date_format(last_day, date_format)
        else:
            break
    return last_day_obj


def choose_room(hotel_id):
    list_all_rooms(hotel_id)
    room_id = int(input("Enter the room number from a list above you want to book: "))
    rooms = database.get_all_rooms(hotel_id)
    room_cost = 0
    searching = True
    while searching:
        for room in rooms:
            if room['room_ID'] == room_id:
                searching = False
                room_cost = room['room_type_price']
                break
        if searching:
            list_all_rooms(hotel_id)
            room_id = int(input("Enter the proper room number from a list above you want to book: "))
    return room_id, room_cost


def choose_dining_option():
    list_dining_options()
    dining_option_id = int(input("Enter dining option number from a list above: "))
    dining_options = database.get_dining_options()
    dining_option_cost = 0
    searching = True
    while searching:
        for dining_option in dining_options:
            if dining_option['dining_option_ID'] == dining_option_id:
                searching = False
                dining_option_cost = dining_option['dining_option_cost']
                break
        if searching:
            list_dining_options()
            dining_option_id = int(input("Enter proper dining option number from a list above: "))
    return dining_option_id, dining_option_cost


def choose_payment_method():
    list_payment_methods()
    payment_method_id = int(input("Enter payment method number from a list above: "))
    payment_methods = database.get_payment_methods()
    payment_method_discount = 0
    searching = True
    while searching:
        for payment_method in payment_methods:
            if payment_method['payment_method_ID'] == payment_method_id:
                searching = False
                payment_method_discount = payment_method['payment_method_discount']
                break
        if searching:
            list_payment_methods()
            payment_method_id = int(input("Enter proper payment method number from a list above: "))
    return payment_method_id, payment_method_discount


DECISION_INTERFACE = """
You have reached to the end of reservation form. 

Please decide what you want to do:
- 'cancel' to discard the reservation. 
- 'save' to finalize the reservation. 
YOUR CHOICE: """


def make_reservation(user_id):
    user_input = input(RESERVATION_MENU_INTERFACE)
    while user_input != 'back':
        if user_input == 'fill':
            print("Here is the reservation form:")
            hotel_id = choose_hotel()

            date_format = '%Y-%m-%d'
            first_day_obj = choose_start_date(date_format)

            last_day_obj = choose_end_date(date_format, first_day_obj)

            reservation_period = last_day_obj - first_day_obj

            room_id, room_cost = choose_room(hotel_id)

            dining_option_id, dining_option_cost = choose_dining_option()

            payment_method_id, payment_method_discount = choose_payment_method()

            reservation_cost = calculate_cost(reservation_period.days, room_cost, dining_option_cost, payment_method_discount)
            print(f"Reservation cost: {reservation_cost} PLN for {reservation_period.days} days.")

            decision = input(DECISION_INTERFACE)
            while True:
                if decision == 'save':
                    database.add_reservation(user_id, hotel_id, first_day_obj.date(), last_day_obj.date(), room_id, dining_option_id, payment_method_id, reservation_cost)
                    print("Your reservation has been saved.")
                    break
                elif decision == 'cancel':
                    print("You have discarded your reservation.")
                    break
                else:
                    print("Unknown command! Try again.")
                decision = input(DECISION_INTERFACE)
        else:
            print("Unknown command! Try again.")

        user_input = input(RESERVATION_MENU_INTERFACE)


def list_all_reservations():
    reservation_list = database.get_all_reservations_info()
    for reservation in reservation_list:
        print(f"Reservation number: {reservation['reservation_ID']}\n"
              f"\tClient: {reservation['user_name']} {reservation['user_surname']}\n"
              f"\tHotel: {reservation['hotel_name']}\n"
              f"\tDate: {reservation['first_day']} - {reservation['last_day']}\n"
              f"\tRoom: {reservation['room_ID']} {reservation['room_type']}\n"
              f"\tDining option: {reservation['dining_option_type']}\n"
              f"\tPayment: {reservation['payment_method']} - {reservation['cost']} PLN")


def list_my_reservations_info(user_id):
    reservation_list = database.get_my_reservations_info(user_id)
    for reservation in reservation_list:
        print(f"Reservation number: {reservation['reservation_ID']}\n"
              f"\tClient: {reservation['user_name']} {reservation['user_surname']}\n"
              f"\tHotel: {reservation['hotel_name']}\n"
              f"\tDate: {reservation['first_day']} - {reservation['last_day']}\n"
              f"\tRoom: {reservation['room_ID']} {reservation['room_type']}\n"
              f"\tDining option: {reservation['dining_option_type']}\n"
              f"\tPayment: {reservation['payment_method']} - {reservation['cost']} PLN")


def choose_reservation(user_id, action_name):
    list_my_reservations_info(user_id)
    reservation_id = int(input(f"Enter the reservation number from a list above, you want to {action_name}: "))
    reservations = database.get_my_reservations_info(user_id)
    searching = True
    reservation_obj = 0
    while searching:
        for reservation in reservations:
            if reservation['reservation_ID'] == reservation_id:
                reservation_obj = database.get_my_reservation(reservation_id)
                searching = False
                break
        if searching:
            list_my_reservations_info(user_id)
            reservation_id = int(input(f"Enter the proper reservation number from a list above, you want to {action_name}: "))
    return reservation_obj


CLIENT_PICK_TO_EDIT_RESERVATION_MENU = """
You are in reservation editing menu. 

Please decide what you want to do:
- 'pick' to choose specific reservation to change.
- 'back' to back to the previous menu.
YOUR CHOICE: """


CLIENT_EDIT_RESERVATION_MENU = """

Please decide what you want to change:
- 'hotel' to change hotel.
- 'date' to change starting and ending date.
- 'room' to change room.
- 'dining' to change dining options.
- 'payment' to change payment method.
- 'save' to save changes.
- 'cancel' to cancel changes.
YOUR CHOICE:  """

EDIT_DECISION_INTERFACE = """

Are you sure you want to save the changes:
- 'yes' 
- 'no' 
YOUR CHOICE: """


def pick_to_edit_my_reservation_menu(user_id):
    user_input = input(CLIENT_PICK_TO_EDIT_RESERVATION_MENU)
    while user_input != 'back':
        if user_input == 'pick':
            reservation_obj = choose_reservation(user_id, 'edit')
            edit_my_reservation(reservation_obj[0])
        else:
            print("Unknown command! Try again.")

        user_input = input(CLIENT_PICK_TO_EDIT_RESERVATION_MENU)


def edit_my_reservation(reservation_obj):
    user_input = input(CLIENT_EDIT_RESERVATION_MENU)
    while True:
        if user_input == 'hotel':
            reservation_obj['hotel_id'] = choose_hotel()

        elif user_input == 'date':
            date_format = '%Y-%m-%d'
            reservation_obj['first_day'] = choose_start_date(date_format)
            reservation_obj['last_day'] = choose_end_date(date_format, reservation_obj['first_day'])

        elif user_input == 'room':
            reservation_obj['room_id'], reservation_obj['room_type_price'] = choose_room(reservation_obj['hotel_id'])

        elif user_input == 'dining':
            reservation_obj['dining_option_id'], reservation_obj['dining_option_cost'] = choose_dining_option()

        elif user_input == 'payment':
            reservation_obj['payment_method_id'], reservation_obj['payment_method_discount'] = choose_payment_method()

        elif user_input == 'save':
            reservation_period = reservation_obj['last_day'] - reservation_obj['first_day']
            reservation_obj['cost'] = calculate_cost(reservation_period.days, reservation_obj['room_type_price'],
                                                     reservation_obj['dining_option_cost'],
                                                     reservation_obj['payment_method_discount'])
            print(f"Reservation cost: {reservation_obj['cost']} PLN for {reservation_period.days} days.")
            decision = input(EDIT_DECISION_INTERFACE)
            if decision == 'yes':
                database.update_my_reservation(reservation_obj['hotel_id'], reservation_obj['first_day'],
                                               reservation_obj['last_day'], reservation_obj['room_id'],
                                               reservation_obj['dining_option_id'],
                                               reservation_obj['payment_method_id'], reservation_obj['cost'],
                                               reservation_obj['reservation_ID'])
                break
            elif decision == 'no':
                pass
            else:
                print("Unknown command! Try again.")

        elif user_input == 'cancel':
            break
        else:
            print("Unknown command! Try again.")

        user_input = input(CLIENT_EDIT_RESERVATION_MENU)


CLIENT_PICK_TO_DELETE_RESERVATION_MENU = """
You are in reservation deleting menu. 

Please decide what you want to do:
- 'pick' to choose specific reservation to delete.
- 'delete all' to delete all your reservations.
- 'back' to back to the previous menu.
YOUR CHOICE: """


DELETE_DECISION_INTERFACE = """

Are you sure you want to delete:
- 'yes' 
- 'no' 
YOUR CHOICE: """


def pick_to_delete_my_reservation_menu(user_id):
    user_input = input(CLIENT_PICK_TO_DELETE_RESERVATION_MENU)
    while user_input != 'back':
        if user_input == 'pick':
            reservation_obj = choose_reservation(user_id, 'delete')
            decision = input(DELETE_DECISION_INTERFACE)
            if decision == 'yes':
                database.delete_reservation(reservation_obj[0]['reservation_ID'])
                print("Your reservation has been deleted.")
            elif decision == 'no':
                pass
            else:
                print("Unknown command! Try again.")
        elif user_input == 'delete all':
            decision = input(DELETE_DECISION_INTERFACE)
            if decision == 'yes':
                database.delete_all_my_reservation(user_id)
                print("All your reservations have been deleted.")
                break
            elif decision == 'no':
                pass
            else:
                print("Unknown command! Try again.")
        else:
            print("Unknown command! Try again.")

        user_input = input(CLIENT_PICK_TO_DELETE_RESERVATION_MENU)


STATISTICS_MENU = """
You are in statistics menu. 

Please decide what you want to see:
- 'booking price' to see minimum, maximum and average price of booking.
- 'pop hotels' to see hotels by popularity.
- 'pop rooms' to see room types by popularity.
- 'pop dining' to see dining options by popularity.
- 'pop payment' to see payment methods by popularity.
- 'best clients' to see client that have more than one reservation' 
- 'back' to back to the previous menu.
YOUR CHOICE: """


def cost_statistics():
    costs = database.get_min_max_avg_cost()
    print("Reservation costs statistics:")
    print(f" - Lowest booking value: {costs[0]['minimum']} PLN")
    print(f" - Average booking value: {costs[0]['average']} PLN")
    print(f" - Highest booking value: {costs[0]['maximum']} PLN")


def list_hotels_by_popularity():
    print("List of hotels by number of reservations:")
    hotels = database.get_hotels_popularity()
    for hotel in hotels:
        if hotel['bookings'] == 1:
            print(f"Hotel: {hotel['hotel_name']} in {hotel['location_city']} has {hotel['bookings']} booking.")
        else:
            print(f"Hotel: {hotel['hotel_name']} in {hotel['location_city']} has {hotel['bookings']} bookings.")


def list_room_types_by_popularity():
    print("List of room types by number of bookings:")
    room_types = database.get_room_types_popularity()
    for room_type in room_types:
        if room_type['bookings'] == 1:
            print(f"The '{room_type['room_type']}' type was chosen {room_type['bookings']} time.")
        else:
            print(f"The '{room_type['room_type']}' type was chosen {room_type['bookings']} times.")


def list_dining_options_by_popularity():
    print("List of dining options by number of orders:")
    dining_options = database.get_dining_options_popularity()
    for dining_option in dining_options:
        if dining_option['orders'] == 1:
            print(f"The '{dining_option['dining_option_type']}' option was chosen {dining_option['orders']} time.")
        else:
            print(f"The '{dining_option['dining_option_type']}' option was chosen {dining_option['orders']} times.")


def list_payment_methods_by_popularity():
    print("List of payment methods by number of orders:")
    payment_methods = database.get_payment_methods_popularity()
    for payment_method in payment_methods:
        if payment_method['orders'] == 1:
            print(f"The '{payment_method['payment_method']}' method was chosen {payment_method['orders']} time.")
        else:
            print(f"The '{payment_method['payment_method']}' method was chosen {payment_method['orders']} times.")


def list_clients_with_multiple_reservations():
    print("List of clients with multiple reservations:")
    clients = database.get_clients_with_multiple_reservations()
    for client in clients:
        print(f"{client['user_name']} {client['user_surname']} has {client['reservations']} reservations.")


def statistic_menu():
    user_input = input(STATISTICS_MENU)
    while user_input != 'back':
        if user_input == 'booking price':
            cost_statistics()
        elif user_input == 'pop hotels':
            list_hotels_by_popularity()
        elif user_input == 'pop rooms':
            list_room_types_by_popularity()
        elif user_input == 'pop dining':
            list_dining_options_by_popularity()
        elif user_input == 'pop payment':
            list_payment_methods_by_popularity()
        elif user_input == 'best clients':
            list_clients_with_multiple_reservations()
        else:
            print("Unknown command! Try again.")

        user_input = input(STATISTICS_MENU)
