def TrackSearch(conn):
    try:        
        cursor = conn.cursor()

        query = "SELECT * FROM track WHERE TRUE"
        param = []

        
        title = input("Введите название песни: ")
        if(title != ""):
            while '  ' in title:
                title = title.replace('  ', ' ')        
            query += " AND LOWER(' ' || title || ' ') LIKE %s"
            param.append('%'+str.lower(title)+'%')


        performers = input("Введите название иполнителя: ")
        if(performers != ""):
            while '  ' in performers:
                performers = performers.replace('  ', ' ')
            query += " AND  LOWER(' ' || performers || ' ' ) LIKE %s"
            param.append('%'+ str.lower(performers)+'%')


        album = input("Введите название альбома: ")
        if(album != ""):
            while '  ' in album:
                album = album.replace('  ', ' ')
            query += " AND LOWER(' ' || album || ' ') LIKE %s"
            param.append('%'+str.lower(album)+'%')


        duration = (input("Введите длительность трека в формате {оператор(=, >, <) число}: ")) 
        duration = duration.strip()
        if(duration != ""):
            operation = duration[0]
            duration = duration[1:len(duration)]
            if(not duration.isdigit()):
                return "Длительнось это положительное целое число меньшее 32768 секунд "
            else:
                duration = int(duration)

            if(operation == '='):                
                query += " AND duration = %s"         

            elif(operation == '>'):                
                query += " AND duration > %s"

            elif(operation == '<'):            
                query += " AND duration < %s"

            else:
                return "Не известная операция"
            
            param.append(duration)
        

        query += " LIMIT %s "
        number_of_results = input("Введите количества выдаваемых результатов: ")
        number_of_results = number_of_results.strip()
        if(number_of_results != ""):
            if(not number_of_results.isdigit()):
                return "Количества выдаваемых результатов это положительное целое число"
            else:
                number_of_results = int(number_of_results)
                param.append(number_of_results) 
        else:
            param.append(5)


        query += "OFFSET %s"
        offset = input("Введите смещение: ")        
        offset = offset.strip()
        if(offset != ""):
            if(not offset.isdigit()):
                return "Смещение это положительное целое число"
            else:
                offset = int(offset)
                param.append(offset) 
        else:
            param.append(0)


        cursor.execute(query, param)

        tracks = cursor.fetchall()
        cursor.close()

        if(tracks == []):
            return "Нет такого трека"
        
        return tracks
    except:
        return "Не получилось найти трек"
