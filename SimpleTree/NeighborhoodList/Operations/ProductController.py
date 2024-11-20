import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors

def PrintBeautifully(products=[]):
    print()
    if(not isinstance(products, list)):
        print(products)
        return
    
    from collections import defaultdict
    tree = defaultdict(list)
    mn = 1e9
    mn_product = []
    for product in products:
        tree[product[2]].append(product)
        if( mn > product[0]):
            mn = product[0]
            mn_product = product

    def format_tree(node_id, level = 1):
        result = []
        
        for child in tree[node_id]:
            result.append('    ' * level + str(child[0]) + ") " +child[1])
            result.extend(format_tree(child[0], level + 1))
        return result
    result = [str(mn_product[0]) + ') ' + mn_product[1]]
    result = format_tree(mn_product[2])
    for item in result:
        print(item)


# Добавление листа в дерево. На вход Название, Идентификатор родителя
# ? return id
def AddLeaf(conn):
    try:
        title = input("Введите название: ")        
        title = title.strip()
        if(title == ""):
            return "Название не может быть пустым"
        
        parent_id = input("Введите идентификатор родителя: ")
        parent_id = parent_id.strip()
        if(not parent_id.isdigit()):
            return "Идентификатор родителя должен быть положительным целым числом"
        
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO neighborhood_tree(title, parent_id)
            VALUES
                    (%s, %s)
            RETURNING id;
                    ''', (title, parent_id))
        
        result  = cursor.fetchall()

        conn.commit()
        cursor.close()

        return "Успешно добавили с идентификатором: " + str(result)
    except errors.lookup(UNIQUE_VIOLATION) as e:
        print(e)
    # except:
    #     return("Не получилось добавить. ")

# Удаление листа. На вход Идентификатор 
# ? return int (количество удаленных)
def DeleteLeaf(conn):
    try:            
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
             
        cnt_descendants = len(GetAllDescendants(id, conn)) 

        if(cnt_descendants > 0 ):
            return "Узел с идентификатором: " + id + " не является листом"
        
        cursor = conn.cursor()        
        cursor.execute('''
            DELETE FROM neighborhood_tree
            WHERE id = %s        
                    ''', (id,))
        
        result = cursor.rowcount
        conn.commit()
        cursor.close()

        if(result == 0):
            return("Нет листа с таким идентификатором")

        return "Успешно удалили лист"
    except:
        return("Не удалось удалить лист")

# Удаление поддерева. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteSubtree(conn):
    try:
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        
        result = len(GetAllDescendants(id, conn)) + 1
        cursor = conn.cursor()
        cursor.execute('''                   
            DELETE FROM neighborhood_tree
            WHERE id = %s
            RETURNING *
            ''', (id,))
        
        conn.commit()
        cursor.close()
        
        if(result == 0):
            return("Нет узла с таким идентификатором")
        
        if(result == 1):
            return "Удалили " + str(result) + " узeл"

        return "Удалили " + str(result) + " узлов"
    except:
        return("Не удалось удалить поддерево")


# Удаление узла с переподчинением. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteNode(conn):
    try:        
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE neighborhood_tree SET parent_id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s) WHERE parent_id = %s;                
                    ''', (id, id))
        
        cursor.execute('''
            DELETE FROM neighborhood_tree WHERE id = %s;
                    ''', (id,))
        
        result = cursor.rowcount
        if(result == 0):
            return("Нет узла с таким идентификатором")

        conn.commit()

        return "Успешно удалили узел"
    except:
        return("Не удалось удалить узел")

# Получение прямых потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectDescendants(conn):
    # try:       
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"

        cursor = conn.cursor()
        cursor.execute('''
            SELECT * 
            FROM neighborhood_tree
            WHERE parent_id = %s            
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
         
        return result
    # except:
    #     return("Не удалось получить прямых потомков")

# Получение прямого родителя. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectParent(conn):
    try:            
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        
        cursor = conn.cursor()        
        cursor.execute('''
            SELECT *
            FROM neighborhood_tree
            WHERE id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s)
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
         
        return result
    except:
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
            
        cursor = conn.cursor()                
        cursor.execute('''
            WITH RECURSIVE r AS (
                SELECT id, title, parent_id
                FROM neighborhood_tree
                WHERE parent_id = %s            
                UNION 
                SELECT neighborhood_tree.id, neighborhood_tree.title, neighborhood_tree.parent_id
                FROM neighborhood_tree
                    JOIN r
                    ON neighborhood_tree.parent_id = r.id
            )
            
            SELECT * FROM r;     
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
         
        return result
    except:
        return("Не удалось получить всех потомков")

# Получение всех родителей. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllParents(conn):
    try:
        id = input("Введите идентификатор: ")
        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным целым числом"
        
        cursor = conn.cursor()        
        cursor.execute('''
            WITH RECURSIVE r AS (
                SELECT id, title, parent_id
                FROM neighborhood_tree
                WHERE id = %s            
                UNION 
                SELECT neighborhood_tree.id, neighborhood_tree.title, neighborhood_tree.parent_id
                FROM neighborhood_tree
                    JOIN r
                        ON neighborhood_tree.id = r.parent_id
            )
            
            SELECT * FROM r;     
                        ''', (id,))

        result = cursor.fetchall()
        cursor.close()
         
        return result
    except:
        return("Не удалось получить всех родителей")



    