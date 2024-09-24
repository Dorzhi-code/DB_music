from CRUID import Track
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
        title = input()
        performers = input()
        album = input()
        duration = int(input())
        print(Track.Create(title, performers, album, duration))
    elif(number_of_acion == 2):
        print(Track.RetrieveAll())
    elif(number_of_acion == 3):
        id = int(input())
        print(Track.Retrieve(id))
    elif(number_of_acion == 4):
        id = int(input())
        title = input()
        performers = input()
        album = input()
        duration = int(input())     
        print(Track.Update(id, title, performers, album, duration))   
    elif(number_of_acion == 5):
        id = int(input())
        print(Track.Delete(id))
    elif(number_of_acion == 6):
        int_list = []
        for element in input().split():
            int_list.append((int(element),))
        print(Track.DeleteMany(int_list))

