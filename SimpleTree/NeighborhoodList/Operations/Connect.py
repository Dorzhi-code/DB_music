import psycopg2
# Подключение к БД
def get_connection():
    conn = psycopg2.connect(
        dbname="Lab_3",
        user="postgres",
        password=" ",
        host="127.0.0.1",
        port="5432"
    )    
    return conn