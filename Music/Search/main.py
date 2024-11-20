def TrackSearch(conn):
    # try:        
        cursor = conn.cursor()

        query = "SELECT * FROM track WHERE TRUE"
        param = []

        
        title = input("Введите название песни в формате [строка  [строка  [...]]]: ")
        if(title != ""):
            list_title = title.split('  ')                      
            query += " AND LOWER(' ' || title || ' ') LIKE ALL(%s)"
            formatted_title = []
            for item in list_title:
                formatted_title.append('%' + item + '%')
            param.append(formatted_title)


        performers = input("Введите название иполнителя в формате [строка  [строка  [...]]]: ")
        if(performers != ""):
            list_performers = performers.split('  ')
            query += " AND  LOWER(' ' || performers || ' ' ) LIKE ALL(%s)"
            formatted_performers = []
            for item in list_performers:
                formatted_performers.append('%' + item + '%')
            param.append(formatted_performers)


        album = input("Введите название альбома в формате [строка  [строка  [...]]]: ")
        if(album != ""):
            list_album = album.split('  ')
            query += " AND LOWER(' ' || album || ' ') LIKE ALL(%s)"
            formatted_album = []
            for item in list_album:
                formatted_album.append('%' + item + '%')
            param.append(formatted_album)


        duration = (input("Введите длительность трека в формате [{>|<|=} число }]: ")) 
        duration = duration.strip()
        if(duration != ""):
            operation = duration[0]
            duration = duration[1:len(duration)]
            duration = duration.strip()
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
        number_of_results = input("Введите количества выдаваемых результатов в формате [число]: ")
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
        offset = input("Введите смещение в формате [число]: ")        
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
    # except:
    #     return "Не получилось найти трек"
