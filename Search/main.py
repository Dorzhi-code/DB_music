def TrackSearch(id = 0, title = "", performers ="", album="", duration= 0, number_of_results = 5, offset = 0):
    import os
    import sys
    # Добавляем путь к директории проекта в sys.path
    project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "C:\\Users\\Dorzhi\\source\\rep\\DB_music"))
    sys.path.append(project_directory)  
    from CRUID import Connect
    cursor,conn = Connect.get_connection()
    if(id):
        cursor.execute('''
            SELECT *
            FROM track
            WHERE id = %s
            LIMIT %s
            OFFSET %s                       
                    ''', (id,number_of_results, offset))
    elif(duration):
        if(title == "" and performers == "" and album ==""):
            cursor.execute('''
                SELECT *
                FROM track
                WHERE duration = %s
                LIMIT %s
                OFFSET %s
                           
                        ''', (duration,number_of_results, offset))
        else:
            cursor.execute('''
                SELECT *
                FROM track
                WHERE duration = %s AND title LIKE %s AND  performers LIKE %s AND album LIKE %s
                LIMIT %s
                OFFSET %s        
                        ''', (duration, '%'+title+'%', '%'+performers+'%', '%'+album+'%', number_of_results, offset))            
    else:
        cursor.execute('''
                    SELECT *    
                    FROM track 
                    WHERE title LIKE %s AND  performers LIKE %s AND album LIKE %s
                    LIMIT %s
                    OFFSET %s                         
                       '''
                       , ('%'+title+'%', '%'+performers+'%', '%'+album+'%', number_of_results, offset))
        
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

res = TrackSearch(performers="", offset=0)
for i in res:
    print(i)