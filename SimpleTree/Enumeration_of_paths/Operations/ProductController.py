import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

# Получить идентификатор родителя
def get_parent_num(st=""):
    result = ''
    for i in st:
        if i.isdigit():
            result+=i
        else:
            result+=','

    result1 = result.split(',')
    output = []
    
    for i in result1:
        if i != '':
            output.append(i)
            
    if(len(output) >= 2):
        return int(output[-2])
    return None

# Получить уровень 
def get_level(st):
    result = 0
    for i in st:
        if(i == '/'):
            result+=1
    return result

# Многоуровневый вывод
def PrintBeautifully(products=[]):
    print()
    if(not isinstance(products, list)):
        print(products)
        return
    
    from collections import defaultdict
    tree = defaultdict(list)
    root_level = 1e9
    root_product = []
    for product in products:
        num = get_parent_num(product[2])        
        tree[num].append(product)      
        level = get_level(product[2])  
        if( root_level > level):
            root_level = level
            root_product = product

    def format_tree(node_id, level = 1):
        result = []
        
        for child in tree[node_id]:
            result.append(str(child[0]).rjust(3) +  '    ' * level + child[1])
            result.extend(format_tree(child[0], level + 1))
        return result

    parent = get_parent_num(root_product[2])
    result = format_tree(parent)
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
    # try:
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
    # except:
    #     conn.rollback()
    #     return("Не получилось добавить. ")

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
                
        if(id == 1):
            return "Узел с идентификатором 1 явлется корнем"
        
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
    # try:       
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
            WHERE SUBSTRING(
                    path, 1, LENGTH(path) - POSITION(
                        '/' in  REVERSE( SUBSTRING( path, 1, LENGTH(path)-1 ) )
                    )
                ) LIKE(SELECT path FROM path_enum WHERE id = %s)   
            UNION 
            SELECT *
            FROM path_enum
            WHERE id = %s    
            ORDER BY title 
                    ''', (id,id))
        
        result = cursor.fetchall()
        cursor.close()
         
        if(result == [] ):            
            return("Нет узла с идентификатором: ") + str(id)
        
        if(len(result) == 1):
                return "Узел " + str(id) + " не иммеет потомков"
        
        return result
    # except:
    #     conn.rollback() 
    #     return("Не удалось получить прямых потомков")

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
            SELECT * 
            FROM path_enum 
            WHERE path LIKE (
                SELECT
                SUBSTRING(
                    path, 1, LENGTH(path) - POSITION(
                        '/' in  REVERSE( SUBSTRING( path, 1, LENGTH(path)-1 ) )
                    )
                )
                FROM path_enum WHERE id = %s
            )
            UNION 
            SELECT *
            FROM path_enum
            WHERE id = %s  
            ORDER BY title 
                    ''', (id,id))
        
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
            SELECT * 
            FROM path_enum
            WHERE path LIKE (
                SELECT path || '%%' FROM path_enum WHERE id = %s
            )    
            ORDER BY title 
            
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
            SELECT * 
            FROM path_enum
            WHERE (
                SELECT path FROM path_enum WHERE id = %s
            ) LIKE path || '%%'
            ORDER BY title     
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
        return("Не удалось получить всех родителей")


def GetAll(conn):
    try:
        cursor = conn.cursor()        
        cursor.execute('''
            SELECT * 
            FROM path_enum
            ORDER BY title     
                        ''')

        result = cursor.fetchall()
        cursor.close()
         
        if(result == []):  
            return "Нет ничего"
        
        return result

    except:
        conn.rollback()
        return("Не удалось получить всех")    