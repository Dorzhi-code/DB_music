# import psycopg2

# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres",
#     password=" ",
#     host="127.0.0.1",
#     port="5432"
# )
def Create(title, performers, album, duration):
    import Connect
    cursor,conn = Connect.get_connection()
    cursor.execute('''           
        INSERT INTO track (title, performers, album, duration)
        VALUES(%s, %s, %s, %s)
        RETURNING track_id               
                   ''',
                   (title, performers, album, duration)
                   )
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result
print(Create('Режиссер', 'группа "Градусы"', 'Голая', 219))


