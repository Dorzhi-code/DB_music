import hashlib

def PrintPrettyTable(tracks=[]):
    print()
    if(not isinstance(tracks, list)):
        print(tracks)
        return
    from prettytable import PrettyTable
    table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])    
    for track in tracks:
        table.add_row([track[0], track[1], track[2], track[3], track[4]])
    print(table)

def AddUser(conn):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    email = input("Введите почту: ")
    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    try:
        cursor = conn.cursor()
        cursor.execute("CALL add_user(%s, %s, %s)", (username, hashed_password, email))
        conn.commit()
        print("Пользователь успешно добавлен.")
    except Exception as e:
        conn.rollback()
        print(e)

def GetAllUsers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM get_all_users()")
    rows = cursor.fetchall()
    # max_lengths = [0] * len(rows[0])
    # for row in rows:
    #     for i, value in enumerate(row):
    #         max_lengths[i] = max(max_lengths[i], len(str(value)))
    # format_string = " ".join(["{:<" + str(length + 3) + "}" for length in max_lengths])
    # for row in rows:
    #     print(format_string.format(row))
    # for row in rows:
    #     print(row)
    for row in rows:
        print('|{:1}|{:^4}|{:>4}|{:<3}|'.format(*row))
    

def GetUser(conn):
    user_id = input("Введите ID пользователя: ")    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM get_user(%s)", (user_id,))
        result = cursor.fetchone()
        if result:
            print("{:<20} {}".format("user_id:", result[0]))
            print("{:<20} {}".format("username:", result[1]))
            print("{:<20} {}".format("password:", result[2]))
            print("{:<20} {}".format("email:", result[3]))
        else:
            print(f"User with ID {user_id} not found.")
    except Exception as e:
        conn.rollback()
        print(e)

def UpdateUser(conn):
    user_id = input("Введите ID пользователя: ")    
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    email = input("Введите почту: ")

    hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
    try:
        cursor = conn.cursor()
        cursor.execute("CALL update_user(%s, %s, %s, %s)",
                        (user_id.strip(), username, hashed_password, email))
        conn.commit()
        print("Пользователь успешно обновлен.")
    except Exception as e:
        conn.rollback()
        print(e)

def DeleteUser(conn):
    user_id = input("Введите ID пользователя: ")    
    try:
        cursor = conn.cursor()
        cursor.execute("CALL delete_user(%s)", (user_id.strip(),))
        conn.commit()
        print("Пользователь успешно удален.")
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")

def DeleteManyUsers(conn):
    ids_input = input("Введите ID пользователeй через пробел: ")    

    # ids_input = input("Введите ID производителей для удаления через пробел: ")
    ids = ids_input.split()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT delete_many_users(%s)", (ids,))
        deleted_count = cursor.fetchone()[0]
        conn.commit()
        print(f"Удалено пользователей: {deleted_count}")
    except Exception as e:
        conn.rollback()
        print(e)