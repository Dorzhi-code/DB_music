from Operations import Procedures
import os
import time

#  Табличный вывод


# Получение номера действия
def get_action_number():
    print("""
            0 - Выход
            1 - Добавить пользователя
            2 - Получить всех пользователей
            3 - Получить определенного пользователя по ключу
            4 - Редактирование пользователя
            5 - Удалить пользователя
            6 - Удалить несколько пользователей            
        """)
    while(True):
        try:
            choosing_of_action = int(input("Введите номер действия: ")) 
            return choosing_of_action    
        except:
            print("Вы ввели не число. Повторите ввод.")



from Operations import Connect
conn = Connect.get_connection()

while(True):
    number_of_acion = get_action_number()
    if(number_of_acion == 0): # Выход
        conn.close()
        break

    elif(number_of_acion == 1): # Добавить пользователя
        Procedures.AddUser(conn)

    elif(number_of_acion == 2): # Получить всех пользователей
        Procedures.GetAllUsers(conn)
     
    elif(number_of_acion == 3): # Получить определенного пользователя по ключу
        Procedures.GetUser(conn=conn)
        
    elif(number_of_acion == 4): # Редактирование пользователя
        Procedures.UpdateUser(conn)
            
    elif(number_of_acion == 5): # Удалить пользователя
        Procedures.DeleteUser(conn)    

    elif(number_of_acion == 6): # Удалить несколько пользователей

        Procedures.DeleteManyUsers(conn)
   
        

