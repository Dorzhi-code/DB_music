def get_connection():
    import psycopg2
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password=" ",
        host="127.0.0.1",
        port="5432"
    )
    cursor = conn.cursor()
    return cursor, conn