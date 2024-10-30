# Создание экземляра трека. На вход: (string, string, string, int)
# ? return id
def Create(title, performers, album, duration ):
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection()

        title = title.strip()
        performers = performers.strip()
        album = album.strip() 
        duration = duration.strip()       

        if(title == ""):
            return("Название не может быть пустой строкой")        
        
        if(performers == ""):
            return("Исполнитель не может быть пустой строкой")
        
        if(album == ""):
            return("Альбом не может быть пустой строкой")
        
        if(not duration.lstrip("-").isdigit()):
            return("Продолжительность это число")
        else:
            duration = int(duration)
        if(duration <= 0):
            return("Длительнось может быть только положительной")
        
        cursor.execute('''           
            INSERT INTO track (title, performers, album, duration)
            VALUES (%s, %s, %s, %s)
            RETURNING track_id;            
                    ''', (title, performers, album, duration))
        
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return ("Успешно добавили с идентификатором: " + str(result[0][0]))
    except:
        return "Не получилось добавить."

# Получение всех экземляров трека. 
# ? return Array[Aray[track_id, title, performers, album, duration]]
def RetrieveAll():
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection()
        cursor.execute('''
            SELECT * 
            FROM track; 
                    ''')
        tracks = cursor.fetchall()
        cursor.close()
        conn.close()

        from prettytable import PrettyTable
        table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
        for track in tracks:
            table.add_row([track[0], track[1], track[2], track[3], track[4]])

        return table
    except:
        return("Не получилось получить.")
# Получение экземляра трека. На вход (int)
# ? return Array[track_id, title, performers, album, duration]
def Retrieve(id):
    try:
        from CRUD import Connect   
        cursor,conn = Connect.get_connection()
        cursor.execute('''
            SELECT *
            FROM track
            WHERE track_id = %s;
                    ''', (id,))    
        track = cursor.fetchall()
        cursor.close()
        conn.close()

        from prettytable import PrettyTable
        table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
        table.add_row([track[0][0], track[0][1], track[0][2], track[0][3], track[0][4]])
        return table
    except:
        return "Нет такого трека."

# Редактирование экземляра трека. На вход (int, string, string, string, int)
# ? return track_id
def Update(id, title, performers, album, duration):
    try: 
        from CRUD import Connect
        cursor,conn = Connect.get_connection()

        title.strip()
        performers.strip()
        album.strip()

        cursor.execute('''
                    UPDATE track 
                    SET (title, performers, album, duration) = (%s, %s, %s, %s)
                    WHERE track_id = (%s)
                    RETURNING track_id;
                            ''', (title, performers, album, duration, id))  

        conn.commit()
        result = cursor.fetchall()
        cursor.close()
        conn.close()
                    
        return ("Успешно изменилoсь с идентификатором: " + str(result[0][0]))
    except:
        return "Не получилось изменить."
# Удаление экземляра трека. На вход (int)
# ? return number_of_deleted
def Delete(id):
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection() 
        cursor.execute('''
            DELETE FROM track
            WHERE track_id = %s ;
                    ''', (id,))    
        result = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        if(result == 0):
            return("Нет таких записей")
        return ("Успешно удалено: " + str(result))
    except:
        return "Не получилось удалить."
# Удаление экземляров трека. На вход (Array[int])
# ? return number_of_deleted
def DeleteMany(list_of_id):
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection()
        result = 0
        for id in list_of_id:   
            cursor.execute('''
                DELETE FROM track
                WHERE track_id = %s ;
                        ''', (id,))    
            result += cursor.rowcount                      
        conn.commit()
        cursor.close()
        conn.close()
        if(result == 0):
            return("Нет таких записей")
        return ("Успешно удалено: " + str(result))
    except:
        return "Не получилось удалить."

def IsThereElement(id):
    try:
        from CRUD import Connect   
        cursor,conn = Connect.get_connection()
        cursor.execute('''
            SELECT *
            FROM track
            WHERE track_id = %s;
                    ''', (id,))    
        track = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return track 
    except:
        return []
    


