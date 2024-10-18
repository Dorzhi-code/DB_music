# Создание экземляра трека. На вход: (string, string, string, int)
# ? return id
def Create(title, performers, album, duration ):
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection()

        title = title.strip()
        performers = performers.strip()
        album = album.strip()        
    
        cursor.execute('''           
            INSERT INTO track (title, performers, album, duration)
            VALUES (%s, %s, %s, %s)
            RETURNING track_id;            
                    ''', (title, performers, album, duration))
        
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return ("Successfully added with id = " + str(result[0][0]))
    except:
        return "Failed to create record into track table"

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
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        return("Failed to get records in track table")
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
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        return "Failed to get record in track table"

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
        return "Successfully updated with id = " + result
    except:
        return "Failed to edit record in track table"
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
        return "Successfully deleted with id = " + result
    except:
        return "Failed to delete record in track table"
# Удаление экземляров трека. На вход (Array[int])
# ? return number_of_deleted
def DeleteMany(list_of_id):
    try:
        from CRUD import Connect
        cursor,conn = Connect.get_connection()
        cursor.executemany('''
            DELETE FROM track
            WHERE track_id = %s ;
                    ''', (list_of_id))    
        result = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        print(result)
        return ("Successfully deleted: " + str(result))
    except:
        return "Failed to delete records in track table"





