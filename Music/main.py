from CRUD import TrackController
from Search import main as search
import os
import time

#  Табличный вывод


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
            print(TrackController.Create(conn))
        except:
            print("Не получилось записать.")

    elif(number_of_acion == 2): # Получить все треки
        tracks = TrackController.RetrieveAll(conn)
 
        TrackController.PrintPrettyTable(tracks)

    elif(number_of_acion == 3): # Получить определенный трек по ключу                   
        track = TrackController.Retrieve(conn = conn)
        
        TrackController.PrintPrettyTable(track)


    elif(number_of_acion == 4): # Редактирование трека
        print(TrackController.Update(conn))
            
    elif(number_of_acion == 5): # Удалить трек
        print(TrackController.Delete(conn))        

    elif(number_of_acion == 6): # Удалить несколько треков

        print(TrackController.DeleteMany(conn))

    elif(number_of_acion == 7): # Поиск трека
                    
        tracks = search.TrackSearch(conn)
        print(tracks)
        

    
    # time.sleep(3)
    # os.system('cls')
