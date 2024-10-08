import Connect
# Добавление листа в дерево. На вход Название, Идентификатор родителя
# ? return id
def AddLeaf(title, parent_id):
    cursor, conn = Connect.get_connection()
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
    return result

# Удаление листа. На вход Идентификатор 
# ? return int (количество удаленных)
def DeleteLeaf(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        DELETE FROM neighborhood_tree
        WHERE id = %s
                   ''', (id,))
    conn.commit()
    cursor.close()
    conn.close()

# Удаление поддерева. На вход Идентификатор узла
# ? return int (количество удаленных)
# ! как возвращать количество удаленных
def DeleteSubtree(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        DELETE FROM neighborhood_tree
        WHERE id = %s
        RETURNING *
        ''', (id,))
    conn.commit()
    result = cursor.rowcount
    cursor.close()
    conn.close()
    return result


# Удаление узла с переподчинением. На вход Идентификатор узла
# ? return int (количество удаленных)
def DeleteNode(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        
        UPDATE neighborhood_tree SET parent_id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s) WHERE parent_id = %s;

                
                   ''', (id, id))
    cursor.execute('''
        DELETE FROM neighborhood_tree WHERE id = %s;
                   ''', (id,))
    conn.commit()
    cursor.close()
    conn.close()

# Получение прямых потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectDescendants(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        SELECT * 
        FROM neighborhood_tree
        WHERE parent_id = %s
                   ''', (id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Получение прямого родителя. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetDirectParent(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        SELECT *
        FROM neighborhood_tree
        WHERE id = (SELECT parent_id FROM neighborhood_tree WHERE id = %s)
                   ''', (id,))
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Получение всех потомков. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllDescendants(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        WITH RECURSIVE r AS (
            SELECT id, title, parent_id
            FROM neighborhood_tree
            WHERE parent_id = %s            
            UNION ALL
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

# Получение всех родителей. На вход Идентификатор узла
# ? return Array[id, title, parent_id]
def GetAllParents(id):
    cursor, conn = Connect.get_connection()
    cursor.execute('''
        WITH RECURSIVE r AS (
            SELECT id, title, parent_id
            FROM neighborhood_tree
            WHERE id = %s            
            UNION ALL
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

result = DeleteSubtree(65)
# for i in result:
#     print(i)



    