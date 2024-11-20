from Operations import ProductController
import os
import time


# Получение номера действия
def get_action_number():
    print("""
            0 - Выход
            1 - Добавить лист
            2 - Удалить лист
            3 - Удалить поддерево  
            4 - Удаление узла с переподчинением 
            5 - Получить прямых потомков
            6 - Получить прямого родителя
            7 - Получение всех потомков
            8 - Получение всех родителей      
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

    elif(number_of_acion == 1): # Добавить лист
        print(ProductController.AddLeaf(conn))

    elif(number_of_acion == 2): # Удалить лист
        print(ProductController.DeleteLeaf(conn))

    elif(number_of_acion == 3): # Удалить поддерево                 
        print(ProductController.DeleteSubtree(conn))

    elif(number_of_acion == 4): # Удаление узла с переподчинением 
        print(ProductController.DeleteNode(conn))
        # ! проверить удаление не существующего
    elif(number_of_acion == 5): # Получить прямых потомков
        result = ProductController.GetDirectDescendants(conn)
        
        ProductController.PrintBeautifully(result)
        #! красивый вывод
    elif(number_of_acion == 6): # Получить прямого родителя
        result = ProductController.GetDirectParent(conn)
        ProductController.PrintBeautifully(result)        

    elif(number_of_acion == 7): # Получение всех потомков
        result = ProductController.GetAllDescendants(conn=conn)
        ProductController.PrintBeautifully(result)

        #! красивый вывод
    elif(number_of_acion == 8): # Получение всех родителей
        result = ProductController.GetAllParents(conn)
        ProductController.PrintBeautifully(result)

