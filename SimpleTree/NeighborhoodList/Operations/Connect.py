import psycopg2
# Подключение к БД
def get_connection():
    conn = psycopg2.connect(
        dbname="DNS",
        user="postgres",
        password=" ",
        host="127.0.0.1",
        port="5432"
    )    
    return conn