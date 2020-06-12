import pymysql

connection = pymysql.Connection(
    host='localhost',
    user='Mateusz',
    password='zaq1@WSX',
    db='hotel4',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


def close_database():
    with connection.cursor():
        print("Database status: 'Closed'")
        connection.close()


def get_log_info():
    with connection.cursor() as cursor:
        sql = "SELECT user_login, user_password, user_ID, user_type FROM `users`"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def add_user(user_name, user_surname, user_email, user_telephone, user_PESEL, user_login, user_password, user_type):
    with connection.cursor() as cursor:
        sql = "INSERT INTO users (user_name, user_surname, user_email, user_telephone, user_PESEL, " \
              "user_login, user_password, user_type)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_name, user_surname, user_email, user_telephone, user_PESEL, user_login, user_password, user_type))
        connection.commit()


def get_all_hotels():
    with connection.cursor() as cursor:
        sql = "SELECT hotels.hotel_ID, hotels.hotel_name, countries.country_ID, locations.location_city " \
              "FROM `hotels` " \
              "INNER JOIN `locations` on locations.location_ID=hotels.location_id " \
              "INNER JOIN `countries` on countries.country_ID=locations.country_id ORDER by locations.country_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_hotel_address(hotel_id):
    with connection.cursor() as cursor:
        sql = "SELECT hotels.hotel_ID, hotels.hotel_name, countries.country_name, " \
              "locations.location_city, locations.street_address " \
              "FROM `hotels` " \
              "INNER JOIN `locations` on locations.location_ID=hotels.location_id " \
              "INNER JOIN `countries` on countries.country_ID=locations.country_id " \
              "WHERE hotels.hotel_ID = %s"
        cursor.execute(sql, hotel_id)
        result = cursor.fetchall()
        return result


def get_room_types(hotel_id):
    with connection.cursor() as cursor:
        sql = "SELECT room_types.room_type_ID, room_types.room_type, room_types.room_type_price " \
              "FROM `room_types` " \
              "INNER JOIN `rooms` ON room_types.room_type_ID=rooms.room_type_id " \
              "WHERE rooms.hotel_id = %s " \
              "GROUP by room_types.room_type " \
              "ORDER by room_types.room_type_ID"
        cursor.execute(sql, hotel_id)
        result = cursor.fetchall()
        return result


def get_all_rooms(hotel_id):
    with connection.cursor() as cursor:
        sql = "SELECT rooms.room_ID, room_types.room_type, room_types.room_type_price " \
              "FROM `room_types` " \
              "INNER JOIN `rooms` ON room_types.room_type_ID=rooms.room_type_id " \
              "WHERE rooms.hotel_id = %s " \
              "ORDER by room_types.room_type_ID"
        cursor.execute(sql, hotel_id)
        result = cursor.fetchall()
        return result


def get_dining_options():
    with connection.cursor() as cursor:
        sql = "SELECT dining_option_ID, dining_option_type, dining_option_cost " \
              "FROM `dining_options` " \
              "ORDER BY dining_option_ID"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_payment_methods():
    with connection.cursor() as cursor:
        sql = "SELECT payment_method_ID, payment_method, payment_method_discount " \
              "FROM `payment_methods`" \
              "ORDER BY payment_method_ID"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def add_reservation(user_id, hotel_id, first_day_obj, last_day_obj, room_id, dining_option_id, payment_method_id, reservation_cost):
    with connection.cursor() as cursor:
        sql = "INSERT INTO reservations (client_id, hotel_id, first_day, last_day, room_id, dining_option_id, " \
              "payment_method_id, cost) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (user_id, hotel_id, first_day_obj, last_day_obj, room_id, dining_option_id, payment_method_id, reservation_cost))
        connection.commit()


def get_all_reservations_info():
    with connection.cursor() as cursor:
        sql = "SELECT reservations.reservation_ID, users.user_name, users.user_surname, hotels.hotel_name, " \
              "rooms.room_ID, room_types.room_type, dining_options.dining_option_type, " \
              "payment_methods.payment_method, reservations.cost " \
              "FROM `reservations` " \
              "INNER JOIN `users` ON reservations.client_id=users.user_ID " \
              "INNER JOIN `hotels` ON reservations.hotel_id=hotels.hotel_ID " \
              "INNER JOIN `rooms` ON reservations.room_id=rooms.room_ID " \
              "INNER JOIN `room_types` ON rooms.room_type_id=room_types.room_type_ID " \
              "INNER JOIN `dining_options` ON reservations.dining_option_id=dining_options.dining_option_ID " \
              "INNER JOIN `payment_methods` ON reservations.payment_method_id=payment_methods.payment_method_ID " \
              "ORDER BY reservations.reservation_ID"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result


def get_my_reservations_info(user_id):
    with connection.cursor() as cursor:
        sql = "SELECT reservations.reservation_ID, users.user_name, users.user_surname, hotels.hotel_name, " \
              "rooms.room_ID, room_types.room_type, dining_options.dining_option_type, " \
              "payment_methods.payment_method, reservations.cost " \
              "FROM `reservations` " \
              "INNER JOIN `users` ON reservations.client_id=users.user_ID " \
              "INNER JOIN `hotels` ON reservations.hotel_id=hotels.hotel_ID " \
              "INNER JOIN `rooms` ON reservations.room_id=rooms.room_ID " \
              "INNER JOIN `room_types` ON rooms.room_type_id=room_types.room_type_ID " \
              "INNER JOIN `dining_options` ON reservations.dining_option_id=dining_options.dining_option_ID " \
              "INNER JOIN `payment_methods` ON reservations.payment_method_id=payment_methods.payment_method_ID " \
              "WHERE users.user_ID = %s " \
              "ORDER BY reservations.reservation_ID"
        cursor.execute(sql, user_id)
        result = cursor.fetchall()
        return result


def get_my_reservation(reservation_id):
    with connection.cursor() as cursor:
        sql = "SELECT reservations.reservation_ID, reservations.client_id, reservations.hotel_id, " \
              "reservations.first_day, reservations.last_day, reservations.room_id, reservations.dining_option_id, " \
              "reservations.payment_method_id, reservations.cost, room_types.room_type_price, " \
              "dining_options.dining_option_cost, payment_methods.payment_method_discount " \
              "FROM `reservations` " \
              "INNER JOIN `rooms` ON reservations.room_id = rooms.room_ID " \
              "INNER JOIN `room_types` ON rooms.room_type_id = room_types.room_type_ID " \
              "INNER JOIN `dining_options` ON reservations.dining_option_id = dining_options.dining_option_ID " \
              "INNER JOIN `payment_methods` ON reservations.payment_method_id = payment_methods.payment_method_ID " \
              "WHERE reservation_ID = %s"
        cursor.execute(sql, reservation_id)
        result = cursor.fetchall()
        return result


def update_my_reservation(hotel_id, first_day, last_day, room_id, dining_option_id, payment_method_id, cost, reservation_id):
    with connection.cursor() as cursor:
        sql = "UPDATE `reservations` SET hotel_id = %s, first_day = %s, last_day = %s, " \
              "room_id = %s, dining_option_id = %s, payment_method_id = %s, cost = %s " \
              "WHERE reservation_ID = %s"
        cursor.execute(sql, (hotel_id, first_day, last_day, room_id, dining_option_id, payment_method_id, cost, reservation_id))
        connection.commit()
