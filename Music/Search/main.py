def TrackSearch(track_id = '', title = "", performers ="", album="", duration= '', number_of_results = 5, offset = 0):
    try:
        import os
        import sys
        # Добавляем путь к директории проекта в sys.path
        #project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "C:\\Users\\Dorzhi\\source\\rep\\DB_music"))
        #sys.path.append(project_directory)  
        from CRUD import Connect
        cursor,conn = Connect.get_connection()
        query = "SELECT * FROM track WHERE TRUE"
        param = []
        if(track_id != ''):
            query += " AND track_id = %s"
            param.append(track_id)
        else:
            if(duration != ''):
                query += " AND duration = %s"
                param.append(duration)

            title = title.strip()
            performers = performers.strip()
            album = album.strip()  

            query += " AND LOWER(title) LIKE %s AND  LOWER(performers) LIKE %s AND LOWER(album) LIKE %s"

            param.append('%'+str.lower(title)+'%')
            param.append('%'+ str.lower(performers)+'%')
            param.append('%'+str.lower(album)+'%')

        query += " LIMIT %s OFFSET %s"

        if(number_of_results == ''):
             number_of_results = 5
        param.append(number_of_results)

        if(offset == ''):
             offset = 0
        param.append(offset)          

        cursor.execute(query, param)

        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        return "Failed to search records in track table"
