from CRUD import Track
from Search import main as search
import os
import time
# Получение номера действия
def get_action_number():
    print("""
            0 - Выход
            1 - Записать трек
            2 - Получить все треки
            3 - Получить определенный трек по ключу
            4 - Редактирование трека
            5 - Удалить трек
            6 - Удалить несколько треков     
            7 - Поиск трека       
        """)
    while(True):
        try:
            choosing_of_action = int(input("Введите номер действия: ")) 
            return choosing_of_action    
        except:
            print("Вы ввели не число. Повторите ввод.")


while(True):
    number_of_acion = get_action_number()
    if(number_of_acion == 0): # Выход
        break
    if(number_of_acion == 1): # Записать трек
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = int(input("Введите длительность трека: "))
        print(Track.Create(title, performers, album, duration))
    elif(number_of_acion == 2): # Получить все треки
        from prettytable import PrettyTable
        tracks = Track.RetrieveAll()
        table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
        for track in tracks:
            table.add_row([track[0], track[1], track[2], track[3], track[4]])
        print(table)
    elif(number_of_acion == 3): # Получить определенный трек по ключу
        from prettytable import PrettyTable
        id = int(input("Введите идентификационный номер: "))
        track = Track.Retrieve(id)
        if(track != []):
            table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
            table.add_row([track[0][0], track[0][1], track[0][2], track[0][3], track[0][4]])
            print(table)
        else:
            print("Не правильно ввели идентификационный номер.")
    elif(number_of_acion == 4): # Редактирование трека
        id = int(input("Введите идентификационный номер: "))
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = int(input("Введите длительность трека: "))   
        print(Track.Update(id, title, performers, album, duration))   
    elif(number_of_acion == 5): # Удалить трек
        id = int(input("Введите идентификационный номер: "))
        print(Track.Delete(id))
    elif(number_of_acion == 6): # Удалить несколько треков
        int_list = []
        for element in input("Введите идентификационный номер: ").split():
            int_list.append((int(element),))
        print(Track.DeleteMany(int_list))
    elif(number_of_acion == 7): # Поиск трека
        from prettytable import PrettyTable
        id = (input("Введите идентификационный номер: "))
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = (input("Введите длительность трека: ")) 
        number_of_results = (input("Введите количества выдаваемых результатов: "))
        offset = (input("Введите смещение: "))
        
        tracks = search.TrackSearch(track_id = id, title=title, performers=performers, album=album, duration=duration, number_of_results=number_of_results, offset=offset)
        table = PrettyTable(['ID', 'Title', 'Performers', 'Album', 'Duration'])
        for track in tracks:
            table.add_row([track[0], track[1], track[2], track[3], track[4]])
        print(table)

    
    # time.sleep(3)
    # os.system('cls')
