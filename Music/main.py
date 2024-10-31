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



from CRUD import Connect
conn = Connect.get_connection()

while(True):
    number_of_acion = get_action_number()
    if(number_of_acion == 0): # Выход
        conn.close()
        break

    elif(number_of_acion == 1): # Записать трек
        try:
            title = input("Введите название песни: ")
            performers = input("Введите название иполнителя: ")
            album = input("Введите название альбома: ")
            duration = input("Введите длительность трека: ")
            print(TrackController.Create(title, performers, album, duration, conn))
        except:
            print("Не получилось записать.")

    elif(number_of_acion == 2): # Получить все треки
        tracks = TrackController.RetrieveAll(conn)
 
        print(tracks)

    elif(number_of_acion == 3): # Получить определенный трек по ключу
        try:                
            id = int(input("Введите идентификатор: "))
            track = TrackController.Retrieve(id, conn)
            
            print(track)
        except:
            print("Идентификатор это положительное число.")

    elif(number_of_acion == 4): # Редактирование трека
        print(TrackController.Update(conn))
            

    elif(number_of_acion == 5): # Удалить трек
        try:
            id = int(input("Введите идентификатор: "))

            print(TrackController.Delete(id, conn))
        except:
            print("Не правильно ввели идентификатор.")

    elif(number_of_acion == 6): # Удалить несколько треков
        int_list = []
        for element in input("Введите идентификатор: ").split():
            try:
                int_list.append((int(element),))
            except:
                print(element + " не число. ")

        print(TrackController.DeleteMany(int_list, conn))

    elif(number_of_acion == 7): # Поиск трека
        try:                            
            tracks = search.TrackSearch(conn)
            print(tracks)
        except:
            print("Не получилось найти")

    
    # time.sleep(3)
    # os.system('cls')
