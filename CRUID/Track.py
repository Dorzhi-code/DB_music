# import psycopg2

# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password=" ",
#     host="127.0.0.1",
#     port="5432"
# )
def Create(title, performers, album, duration):
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.execute('''           
        INSERT INTO track (title, performers, album, duration)
        VALUES(%s, %s, %s, %s)
        RETURNING track_id;            
                   ''',
                   (title, performers, album, duration)
                   )
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result
def RetrieveAll():
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.execute('''
        SELECT * 
        FROM track; 
                   ''')
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def Retrieve(id):
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.execute('''
        SELECT *
        FROM track
        WHERE track_id = %s;
                   ''', id)    
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
def Update(id, title, performers, album, duration):
    import Connect
    cursor,conn = Connect.get_connection()
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
    return result
def Delete(id):
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.execute('''
        DELETE FROM track
        WHERE track_id = %s ;
                   ''', (id,))    
    result = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return result
def DeleteMany(list_of_id):
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.executemany('''
        DELETE FROM track
        WHERE track_id = %s ;
                   ''', (list_of_id))    
    result = cursor.rowcount
    conn.commit()
    cursor.close()
    conn.close()
    return result    
# print(Create('Fade Away', 'группа "El Cacto"', 'Fade Away', 200))
# print(Create('Fyex', 'группа "Fyex"', 'Fyex', 204))
# print(Create('Test', 'группа "Test"', 'Test', 207))
# print(Create('Disaster', 'Sønlille', 'Disaster', 120))

print(RetrieveAll())
list_of_id_to_delete = [(18,),(19,),(20,)]
print(DeleteMany(list_of_id_to_delete))
print(RetrieveAll())





