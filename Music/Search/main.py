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

        track_id = (input("Введите идентификационный номер: "))
        track_id = track_id.strip()

        if(track_id != ""):
            if(not track_id.isdigit()):
                return "Идентификатор это положительное число"
            else:
                track_id = int(track_id)
                query += " AND track_id = %s"
                param.append(track_id)

        else:
            title = input("Введите название песни: ")
            title = title.strip()
            if(title != ""):
                query += " AND LOWER(title) LIKE %s"
                param.append('%'+str.lower(title)+'%')


            performers = input("Введите название иполнителя: ")
            performers = performers.strip()
            if(performers != ""):
                query += " AND  LOWER(performers) LIKE %s"
                param.append('%'+ str.lower(performers)+'%')


            album = input("Введите название альбома: ")
            album = album.strip()  
            if(album != ""):
                query += " AND LOWER(album) LIKE %s"
                param.append('%'+str.lower(album)+'%')


            duration = (input("Введите длительность трека: ")) 
            duration = duration.strip()
            if(duration != ""):
                if(not duration.isdigit()):
                    return "Продолжительность это положительное число"
                else:
                    duration = int(duration)
                    query += " AND duration = %s"
                    param.append(duration)
            

            query += " LIMIT %s "
            number_of_results = input("Введите количества выдаваемых результатов: ")
            number_of_results = number_of_results.strip()
            if(number_of_results != ""):
                if(not number_of_results.isdigit()):
                    return "Количества выдаваемых результатов это положительное число"
                else:
                    number_of_results = int(number_of_results)
                    param.append(number_of_results) 
            else:
                param.append(5)


            query += "OFFSET %s"
            offset = input("Введите смещение: ")
            offset = (input("Введите количества выдаваемых результатов: "))
            offset = offset.strip()
            if(offset != ""):
                if(not offset.isdigit()):
                    return "Количества выдаваемых результатов это положительное число"
                else:
                    offset = int(offset)
                    param.append(offset) 
            else:
                param.append(0)


        cursor.execute(query, param)

        tracks = cursor.fetchall()
        cursor.close()
        conn.close()

        if(tracks == []):
            return "Нет такого трека(ов)"
        
        from prettytable import PrettyTable
        table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
        for track in tracks:
            table.add_row([track[0], track[1], track[2], track[3], track[4]])

        return table
    except:
        return "Не получилось найти трек"
