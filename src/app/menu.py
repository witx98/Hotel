import sys
import Functions
from src.app import database

START_MENU_INTERFACE = """
Hello and welcome to Hotel Application. 

Please decide and type what you want to do:
- 'log' to sing in .
- 'reg' to sing up your account .
- 'exit' to turn off the application.
YOUR CHOICE: """

CLIENT_MENU = """
Enter:
- 'hotels' to list all available hotels.
- 'more' to get more information about specific hotel
- 'res' to make reservation.
- 'my res' to see the list of all your reservations.
- 'log out' to log off and go to previous menu.
YOUR CHOICE: """

WORKER_MENU = """
Enter:
- 'hotels' to list all available hotels.
- 'list res' to see the list of all reservations in the system.
- 'log out' to log off and go to previous menu.
YOUR CHOICE: """

CLIENT_RESERVATIONS_MENU = """
Reservations menu. Enter: 
- 'list res' to see detailed information about all your reservations.
- 'edit' to change your reservations.
- 'del' to remove one of your reservations.
- 'back' to back to the previous menu
YOUR CHOICE: """


def menu():
    user_input = input(START_MENU_INTERFACE)
    user_id = 0
    user_type = 0
    if user_input == 'log':
        user_id, user_type = Functions.log_in()
    elif user_input == 'reg':
        Functions.register_user()
        menu()
    elif user_input == 'exit':
        database.close_database()
        sys.exit(0)
    else:
        print("Unknown command! Please try again.")

    if user_id != 0:
        if user_type == 0:
            print("Logged in as a client!")
            client_menu(user_id)
        else:
            print("Logged in as a administrator!")
            worker_menu(user_id)
    else:
        menu()


def client_menu(user_id):
    user_input = input(CLIENT_MENU)
    while True:
        if user_input == 'hotels':
            Functions.list_hotels()
        elif user_input == 'more':
            Functions.hotel_info()
        elif user_input == 'res':
            Functions.make_reservation(user_id)
        elif user_input == 'my res':
            client_reservations_menu(user_id)
        elif user_input == 'log out':
            menu()
        else:
            print("Unknown command! try again.")

        user_input = input(CLIENT_MENU)


def worker_menu(user_id):
    user_input = input(WORKER_MENU)
    while True:
        if user_input == 'hotels':
            Functions.list_hotels()
        elif user_input == 'list res':
            Functions.list_all_reservations()
        elif user_input == 'log out':
            menu()
        else:
            print("Unknown command! try again.")

        user_input = input(WORKER_MENU)


def client_reservations_menu(user_id):
    user_input = input(CLIENT_RESERVATIONS_MENU)
    while user_input != 'back':
        if user_input == 'list res':
            Functions.list_my_reservations_info(user_id)
        elif user_input == 'edit':
            Functions.pick_to_edit_my_reservation_menu(user_id)
        elif user_input == 'del':
            Functions.delete_my_reservation(user_id)
        else:
            print("Unknown command! try again.")

        user_input = input(CLIENT_RESERVATIONS_MENU)


menu()
