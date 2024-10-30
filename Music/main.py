from CRUD import TrackController
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

    elif(number_of_acion == 1): # Записать трек
        try:
            title = input("Введите название песни: ")
            performers = input("Введите название иполнителя: ")
            album = input("Введите название альбома: ")
            duration = input("Введите длительность трека: ")
            print(TrackController.Create(title, performers, album, duration))
        except:
            print("Не получилось записать.")

    elif(number_of_acion == 2): # Получить все треки
        tracks = TrackController.RetrieveAll()
 
        print(tracks)

    elif(number_of_acion == 3): # Получить определенный трек по ключу
        try:                
            id = int(input("Введите идентификатор: "))
            track = TrackController.Retrieve(id)
            
            print(track)
        except:
            print("Не правильно ввели идентификатор.")

    elif(number_of_acion == 4): # Редактирование трека
        try:
            id = int(input("Введите идентификатор: "))
            result = TrackController.IsThereElement(id)
            
            if(result != []):  
                old_title = result[0][1]
                old_performers = result[0][2]
                old_album = result[0][3]
                old_duration = result[0][4]
                
                print("Текущие данные: ")
                print(TrackController.Retrieve(id))

                print("Если хотите оставить прежние данные, то пропустите строку(нажать enter).")

                title = input("Введите название песни: ")
                title = title.strip()
                if(title == ""):
                    title = old_title

                performers = input("Введите название иполнителя: ")
                performers = performers.strip()
                if(performers == ""):
                    performers = old_performers
        
                album = input("Введите название альбома: ")
                album = album.strip()     
                if(album == ""):
                    album = old_album

                duration = input("Введите длительность трека: ")
                if(duration == ""):
                    duration = old_duration

                print(TrackController.Update(id, title, performers, album, duration))   
            else:
                print("Нет такого трека")

        except:
            if(id == ""):
                print("Не правильно ввели идентификатор.")
            

    elif(number_of_acion == 5): # Удалить трек
        try:
            id = int(input("Введите идентификатор: "))

            print(TrackController.Delete(id))
        except:
            print("Не правильно ввели идентификатор.")

    elif(number_of_acion == 6): # Удалить несколько треков
        int_list = []
        for element in input("Введите идентификатор: ").split():
            try:
                int_list.append((int(element),))
            except:
                print(element + " не число. ")

        print(TrackController.DeleteMany(int_list))

    elif(number_of_acion == 7): # Поиск трека
        try:                            
            tracks = search.TrackSearch()
            print(tracks)
        except:
            print("Не получилось найти")

    
    # time.sleep(3)
    # os.system('cls')
