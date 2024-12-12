import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

def PrintBeautifully(products=[]):
    print()
    if(not isinstance(products, list)):
        print(products)
        return
    
    result = []
    mn_level = products[0][3]
    for node in products:
        result.append(str(node[0]).rjust(3) + '   ' * (abs(mn_level-node[3]) + 1) + node[1])
    
    for item in result:
        print(item)



# Are there node
# return True or False
def GetNode(id = "", conn = psycopg2.connect):
    try:
        if(id == ""):
            id = input("Введите идентификатор: ")

            id = id.strip()
            if(not id.isdigit()):
                return "Идентификатор  должен быть положительным целым числом"
            id = int(id)
            if(id <= 0):
                return "Идентификатор  должен быть положительным целым числом"
        
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM path_enum
            WHERE id = %s
        ''', (id,))
        
        result = cursor.fetchall()

        if(result ==[]):
            return "Нет узла с идентификатором: " + str(id)         
        
        return result
    
    except:
        return "Не получилось получить узел"
    
# Are there node
# return True or False
def GetNodeByTitle(title = "" ,conn = psycopg2.connect):
    try:
        if(title == ""):
            title = input("Введите назвние: ")

        title = title.lower()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT *
            FROM path_enum
            WHERE LOWER(title) = %s
        ''', (title,))
        
        result = cursor.fetchall()

        if(result ==[]):
            return False        
        else:
            return True
        
    except:
        return "Не получилось получить узел"

# Добавление листа в дерево. На вход Название, Идентификатор родителя
# ? return id
def AddLeaf(conn):
    try:
        title = input("Введите название: ")        
        title = title.strip()
        if(title == ""):
            return "Название не может быть пустым"
        
        title = ' '.join(title.split())

        if(GetNodeByTitle(conn=conn, title = title)):
            return "Узел с названием " + str(title) + " уже существует"

        parent_id = input("Введите идентификатор родителя: ")
        parent_id = parent_id.strip()
        if(not parent_id.isdigit()):
            return "Идентификатор родителя должен быть положительным целым числом"
        
        parent_id = int(parent_id)
        if(parent_id <= 0):
            return "Идентификатор родителя должен быть положительным целым числом"

        if(isinstance(GetNode(conn=conn, id = parent_id), str)):
            return "Нет такого родителя"
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO path_enum (title, path) VALUES (%s, ' ')   
            RETURNING id                     
                    ''', (title, ))
        id = cursor.fetchall()[0]
        cursor.execute('''
            UPDATE path_enum SET path = (
                SELECT path FROM path_enum WHERE id = %s
            ) || %s || '/'
            WHERE id = %s
                       ''', (parent_id,id,id,))
        
        conn.commit()
        cursor.close()

        return "Успешно добавили с идентификатором: " + str(id[0])    
    except:
        conn.rollback()
        return("Не получилось добавить. ")

# Удаление листа. На вход Идентификатор листа
# ? return int (количество удаленных)
def DeleteLeaf(conn):
    try:            
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"
                     
        
        if(not isinstance(GetNode(id=id, conn=conn), list)):
            return("Нет листа с таким идентификатором")
        
        descendants = GetAllDescendants(id = id, conn=conn)

        if(not isinstance(descendants, str)):
            return "Узел с идентификатором: " + str(id) + " не является листом"

        cursor = conn.cursor()        
        cursor.execute('''
            DELETE FROM path_enum
            WHERE id = %s        
                    ''', (id,))
        
        result = cursor.rowcount
        conn.commit()
        cursor.close()

        if(result == 0):
            return("Нет листа с таким идентификатором")

        return "Успешно удалили лист"
    except:
        conn.rollback()
        return("Не удалось удалить лист")

# Удаление поддерева. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteSubtree(conn):
    try:
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"

        if(isinstance(GetNode(id=id, conn=conn), str)):
            return("Нет узла с идентификатором: ") + str(id)

        
        descendants = GetAllDescendants(id, conn)
        result = len(descendants)
        if(isinstance(descendants, str)):
            result = 1

        cursor = conn.cursor()
        cursor.execute('''                   
            DELETE FROM path_enum WHERE id IN (
                SELECT id FROM path_enum
                WHERE path LIKE (
                    SELECT path || '%%' FROM path_enum WHERE id = %s
                )
            )
            ''', (id,))
        
        conn.commit()
        cursor.close()
        
        if(result == 0):
            return("Нет узла с идентификатором: ") + str(id)
        
        if(result == 1):
            return "Удалили " + str(result) + " узeл"

        return "Удалили " + str(result) + " узлов"

    except:
        conn.rollback()
        return("Не удалось удалить поддерево")


# Удаление узла с переподчинением. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteNode(conn):
    try:        
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"
                
        if(not isinstance(GetNode(id=id, conn=conn), list)):

            return("Нет листа с таким идентификатором")

        cursor = conn.cursor()
        
        cursor.execute(
            '''
                DELETE FROM path_enum WHERE id = %s
            ''', (id,))
        cursor.execute('''
                    UPDATE path_enum SET path = (
                        REPLACE(
                            path, '/%s/', '/'
                        )
                    )
                    ''', (id,))
        
        result = cursor.rowcount
        if(result == 0):
            return("Нет узла с идентификатором: ") + str(id)

        conn.commit()

        return "Успешно удалили узел"
    except:
        conn.rollback()
        return("Не удалось удалить узел")

# Получение прямых потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectDescendants(conn):
    try:       
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"
        
        cursor = conn.cursor()
        cursor.execute('''
            WITH RECURSIVE tree(id, title, path, level, sort_key) AS(
                SELECT pe.id, pe.title, pe.path, 0 AS level, pe.path ||'' AS sort_key
                FROM path_enum pe
                WHERE pe.id = %s
                UNION 
                SELECT p.id, p.title, p.path, t.level + 1, t.sort_key ||  p.title AS sort_key
                FROM path_enum p INNER JOIN tree t ON p.path = t.path ||  p.id || '/'
                WHERE t.level = 0
            )
            SELECT id, title, path, level
            FROM tree
            ORDER BY sort_key
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
         
        if(result == [] ):            
            return("Нет узла с идентификатором: ") + str(id)
        
        if(len(result) == 1):
                return "Узел " + str(id) + " не иммеет потомков"
        
        return result
    except:
        conn.rollback() 
        return("Не удалось получить прямых потомков")

# Получение прямого родителя. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectParent(conn):
    try:            
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"
        cursor = conn.cursor()   
        cursor.execute('''
            WITH RECURSIVE tree(id, title, path, level, sort_key) AS(
                SELECT id, title, path, 0 AS level, 
                    path AS sort_key
                FROM path_enum 
                WHERE id = %s
                UNION 
                SELECT p.id, p.title, p.path, t.level - 1,
                    p.path  AS sort_key
                FROM path_enum p INNER JOIN tree t ON
                    p.path || t.id || '/' = t.path
                WHERE t.level = 0
            )
            SELECT id, title, path, level
            FROM tree
            ORDER BY sort_key
                        ''', (id,))           
        
        result = cursor.fetchall()
        cursor.close()
                  
        if(result == []):  

            return("Нет узла с идентификатором: ") + str(id)
        
        if(len(result) == 1):
            return "Узел " + str(id) + " не иммеет прямого родителя"
        
        return result

    except:
        conn.rollback()
        return("Не удалось получить прямых потомков")

# Получение всех потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllDescendants(id = "", conn = psycopg2.connect):
    try:         
        if(id == ""):            
            id = input("Введите идентификатор: ")
            id = id.strip()
            if(not id.isdigit()):
                return "Идентификатор  должен быть положительным целым числом"
            id = int(id)
            if(id <= 0):
                return "Идентификатор  должен быть положительным целым числом"
        curent_node = GetNode(id=id, conn=conn)
        
        if(not isinstance(curent_node,list)):
            return("Нет узла с идентификатором: ") + str(id)

        cursor = conn.cursor()                
        cursor.execute('''
            WITH RECURSIVE tree(id, title, path, level, sort_key) AS(
                SELECT pe.id, pe.title, pe.path, 0 AS level, pe.path ||'' AS sort_key
                FROM path_enum pe
                WHERE pe.id = %s
                UNION ALL
                SELECT p.id, p.title, p.path, t.level + 1, t.sort_key || p.title || '/' AS sort_key
                FROM path_enum p INNER JOIN tree t ON p.path = t.path ||  p.id || '/'
            )
            SELECT id, title, path, level
            FROM tree
            ORDER BY sort_key
                    ''', (id,))
        
        result = cursor.fetchall()

        cursor.close()
        if(result == [] ):            
            return("Нет узла с идентификатором: ") + str(id)
        
        if(len(result) == 1):
                return "Узел " + str(id) + " не иммеет потомков"
        
        
        return result

    except:
        conn.rollback()
        return("Не удалось получить всех потомков")

# Получение всех родителей. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllParents(conn):
    try:
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        id = int(id)
        if(id <= 0):
            return "Идентификатор  должен быть положительным целым числом"
        cursor = conn.cursor()        
        cursor.execute('''
            WITH RECURSIVE tree(id, title, path, level, sort_key) AS(
                SELECT id, title, path, 0 AS level, 
                    path AS sort_key
                FROM path_enum 
                WHERE id = %s
                UNION 
                SELECT p.id, p.title, p.path, t.level - 1,
                    p.path  AS sort_key
                FROM path_enum p INNER JOIN tree t ON
                    p.path || t.id || '/' = t.path
            )
            SELECT id, title, path, level
            FROM tree
            ORDER BY sort_key
                        ''', (id,))

        result = cursor.fetchall()
        cursor.close()
         
        if(result == []):  

            return("Нет узла с идентификатором: ") + str(id)
        
        if(len(result) == 1):
            return "Узел " + str(id) + " не иммеет родителей"
        
        return result

    except:
        conn.rollback()
        return("Не удалось получить всех родителей")


def GetAll(conn):
    try:
        cursor = conn.cursor()        
        cursor.execute('''
            SELECT id
            FROM path_enum
            WHERE path = (SELECT MIN(path) FROM path_enum)                  
                        ''')

        result = cursor.fetchall()
        cursor.close()
         
        if(result == []):  
            return "Нет ничего"
        
        return GetAllDescendants(id=result[0], conn=conn)
    except:
        conn.rollback()
        return("Не удалось получить всех")    