import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

def get_parent_num(st):
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

def PrintBeautifully(products=[]):
    print()
    if(not isinstance(products, list)):
        print(products)
        return
    
    # for i in products:
    #     print(i)

    from collections import defaultdict
    tree = defaultdict(list)
    mn = 1e9
    mn_product = []
    for product in products:
        num = get_parent_num(product[2])        
        # if(num == None):
        #     mn = product[0]
        #     mn_product = product
        #     continue
        tree[num].append(product)
        if( mn > product[0]):
            mn = product[0]
            mn_product = product

    def format_tree(node_id, level = 1):
        result = []
        
        for child in tree[node_id]:
            result.append(str(child[0]).rjust(3) +  '    ' * level + child[1])
            result.extend(format_tree(child[0], level + 1))
        return result
    result = [str(mn_product[0]).rjust(3) + ' ' + mn_product[1]]
    nm = get_parent_num(mn_product[2])
    result = format_tree(nm)
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

        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO path_enum (title) VALUES (%s)   
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

        if(not isinstance(GetAllDescendants(id = id, conn=conn), list)):
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

        if(not isinstance(GetNode(id=id, conn=conn), list)):
            return("Нет узла с таким идентификатором")

        result = len(GetAllDescendants(id, conn)) + 1
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
        cursor.execute('''
                    -- удалим из пути потомков удаляемый узел
                    UPDATE path_enum SET path = SUBSTRING(
                        REPLACE(
                            '/%s/', CONCAT('/', path),'/'
                        ), 2
                    )

                    ''', (id,))
        
        cursor.execute('''
                    DELETE FROM path_enum WHERE id = %s
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
            SELECT * FROM path_enum
            WHERE SUBSTRING(
                path, 1, LENGTH(path) - POSITION(
                    '/' in REVERSE( SUBSTRING(path, 1, LENGTH(path)-1) )
                )
            ) LIKE(SELECT path FROM path_enum WHERE id = %s)       
            ORDER BY title 
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
         
        if(result == []):
            if(not isinstance(GetNode(id=id, conn=conn), list)):
                return("Нет узла с идентификатором: ") + str(id)
            else:
                return "Узел " + str(id) + " не иммеет потомков"
        
        return result
    # except:
        # conn.rollback() 
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
            SELECT * FROM path_enum WHERE path LIKE (
                SELECT
                SUBSTRING(
                    path, 1, LENGTH(path) - POSITION(
                        '/' in  REVERSE( SUBSTRING( path, 1, LENGTH(path)-1 ) )
                    )
                )
                FROM path_enum WHERE id = %s
            )
            ORDER BY title 

                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
                  
        if(result == []):  
            if(not isinstance(GetNode(id=id, conn=conn), list)):          
                return("Нет узла с идентификатором: ") + str(id)
            else:
                return "Узел " + str(id) + " не иммеет прямого родителя"
        
        return result

    except:
        conn.rollback()
        return("Не удалось получить прямых потомков")

# Получение всех потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllDescendants(id = "", conn = psycopg2.connect):
    # try:         
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
        # result.extend(curent_node)

        cursor.close()
         
        if(result == []):        
            return "Узел " + str(id) + " не иммеет потомков"
            
        
        return result

    # except:
    #     conn.rollback()
    #     return("Не удалось получить всех потомков")

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
            if(not isinstance(GetNode(id=id, conn=conn),list)):          
                return("Нет узла с идентификатором: ") + str(id)
            else:
                return "Узел " + str(id) + " не иммеет родителей"
        
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