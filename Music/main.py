from CRUID import Track
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
    if(number_of_acion == 0):
        break
    if(number_of_acion == 1):
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = int(input("Введите длительность трека: "))
        print(Track.Create(title, performers, album, duration))
    elif(number_of_acion == 2):
        ans = Track.RetrieveAll()
        for i in ans:
            print(i)
    elif(number_of_acion == 3):
        id = int(input("Введите идентификационный номер: "))
        print(Track.Retrieve(id))
    elif(number_of_acion == 4):
        id = int(input("Введите идентификационный номер: "))
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = int(input("Введите длительность трека: "))   
        print(Track.Update(id, title, performers, album, duration))   
    elif(number_of_acion == 5):
        id = int(input("Введите идентификационный номер: "))
        print(Track.Delete(id))
    elif(number_of_acion == 6):
        int_list = []
        for element in input("Введите идентификационный номер: ").split():
            int_list.append((int(element),))
        print(Track.DeleteMany(int_list))
    elif(number_of_acion == 7):
        id = (input("Введите идентификационный номер: "))
        title = input("Введите название песни: ")
        performers = input("Введите название иполнителя: ")
        album = input("Введите название альбома: ")
        duration = (input("Введите длительность трека: ")) 
        number_of_results = input("Введите количества выдаваемых результатов: ")
        offset = input("Введите смещение: ")
        ans = search.TrackSearch(track_id = id, title=title, performers=performers, album=album, duration=duration, number_of_results=number_of_results, offset=offset)
        for i in ans:
            print(i)

    
    time.sleep(3)
    os.system('cls')
