import hashlib

def AddUser(conn):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")
    email = input("Введите почту: ")

    while '  ' in password:
        password = password.replace('  ', ' ').strip()    
    hashed_password = ''
    if(password != ''):        
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
    for row in rows:
        print(f'|{row[0]}|{row[1]}|{row[2]}|{row[3]}|')
    

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

    while '  ' in password:
        password = password.replace('  ', ' ').strip()
    hashed_password = ''
    if(password != ''):        
        hashed_password = hashlib.sha512(password.encode('utf-8')).hexdigest()
        
    try:
        cursor = conn.cursor()
        cursor.execute("CALL update_user(%s, %s, %s, %s)",
                        (user_id, username, hashed_password, email))
        conn.commit()
        print("Пользователь успешно обновлен.")
    except Exception as e:
        conn.rollback()
        print(e)

def DeleteUser(conn):
    user_id = input("Введите ID пользователя: ")
    try:
        cursor = conn.cursor()
        cursor.execute("CALL delete_user(%s)", (user_id,))
        conn.commit()
        print("Пользователь успешно удален.")
    except Exception as e:
        conn.rollback()
        print(f"Произошла ошибка: {e}")

def DeleteManyUsers(conn):
    ids_input = input("Введите пользоваетелей через пробел: ")    

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