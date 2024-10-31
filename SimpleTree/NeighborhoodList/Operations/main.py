import Connect
# Добавление листа в дерево. На вход Название, Идентификатор родителя
# ? return id
def AddLeaf(title="", parent_id=""):
    try:
        cursor, conn = Connect.get_connection()

        title = title.strip()
        if(title == ""):
            return "Название не может быть пустым"
        
        parent_id = parent_id.strip()
        if(not parent_id.isdigit()):
            return "Идентификатор родителя должен быть положительным числом"
        
        cursor.execute('''
            INSERT INTO neighborhood_tree(title, parent_id)
            VALUES
                    (%s, %s)
            RETURNING id;
                    ''', (title, parent_id))
        
        result  = cursor.fetchall()

        conn.commit()
        cursor.close()
        conn.close()
        return "Успешно добавили с идентификатором: " + result
    except:
        print("Не получилось добавить. ")

# Удаление листа. На вход Идентификатор 
# ? return int (количество удаленных)
def DeleteLeaf(id=""):
    try:            
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
             
        cnt_descendants = len(GetAllDescendants(id) )

        if(cnt_descendants > 0 ):
            return "Узел с идентификатором: " + id + " не является листом"
        
        cursor.execute('''
            DELETE FROM neighborhood_tree
            WHERE id = %s        
                    ''', (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
    except:
        print("Не удалось удалить лист")

# Удаление поддерева. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteSubtree(id=""):
    try:
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
        
        result = len(GetAllDescendants(id)) + 1

        cursor.execute('''                   
            DELETE FROM neighborhood_tree
            WHERE id = %s
            RETURNING *
            ''', (id,))
        
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except:
        print("Не удалось удалить поддерево")


# Удаление узла с переподчинением. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteNode(id=""):
    try:
            
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
        
        cursor.execute('''
            UPDATE neighborhood_tree SET parent_id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s) WHERE parent_id = %s;                
                    ''', (id, id))
        
        cursor.execute('''
            DELETE FROM neighborhood_tree WHERE id = %s;
                    ''', (id,))
        
        result = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return result
    except:
        print("Не удалось удалить узел")

# Получение прямых потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectDescendants(id=""):
    try:            
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
        
        cursor.execute('''
            SELECT * 
            FROM neighborhood_tree
            WHERE parent_id = %s
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        print("Не удалось получить прямых потомков")

# Получение прямого родителя. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectParent(id=""):
    try:            
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
        
        cursor.execute('''
            SELECT *
            FROM neighborhood_tree
            WHERE id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s)
                    ''', (id,))
        
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result
    except:
        print("Не удалось получить прямых потомков")

# Получение всех потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllDescendants(id = ""):
    try:            
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"
        
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
        conn.close()
        return result
    except:
        print("Не удалось получить всех потомков")

# Получение всех родителей. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllParents(id=""):
    try:
        cursor, conn = Connect.get_connection()

        id = id.strip()
        if(not id.isdigit()):
            return "Идентификатор  должен быть положительным числом"

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
        conn.close()
        return result
    except:
        print("Не удалось получить всех родителей")

# res = (GetAllDescendants("1"))
# for i in res:
#     print(i)

res = DeleteLeaf("19")
print(res)

# result = DeleteSubtree(20)

# print(result)



    