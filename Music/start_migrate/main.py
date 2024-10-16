import psycopg2
from datetime import datetime, timezone


conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password=" ",
    host="127.0.0.1",
    port="5432"
)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE users (
               user_id SERIAL PRIMARY KEY,
               username VARCHAR(255) NOT NULL,
               password VARCHAR(255) NOT NULL,
               email VARCHAR(255) UNIQUE
               );
               ''')

cursor.execute('''
    CREATE TABLE playlist (
               playlist_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               user_id INTEGER REFERENCES users(user_id)
               );
               ''')

cursor.execute('''
    CREATE TABLE track (
               track_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               performers VARCHAR(255) NOT NULL,
               album VARCHAR(255),
               duration SMALLINT CHECK (duration > 0)
               );
               ''')

cursor.execute('''
    CREATE TABLE playlist_track (
               track_id INTEGER REFERENCES track(track_id),
               playlist_id INTEGER REFERENCES playlist(playlist_id),
               order_num INTEGER  NOT NULL,
               created_at timestamp NOT NULL default now()
               );
               ''')


cursor.execute('''
    INSERT INTO users (user_id, username, password, email)
    VALUES
        (1, 'dodo', sha512('dodo'), 'dodo@music.ru' ),
        (2, 'admin', sha512('admin'), 'admin@music.ru'),
        (3, 'user', sha512('user'), 'user@music.ru'),
        (4, 'listener', sha512('listener'), 'listener@music.ru'),
        (5, 'programmer', sha512('programmer'), 'programmer@music.ru'),
        (6, 'worker', sha512('worker'), 'worker@music.ru'),
        (7, 'student', sha512('student'), 'student@music.ru'),
        (8, 'teacher', sha512('teacher'), 'teacher@music.ru'),
        (9, 'Ivan', sha512('Ivan'), 'Ivan@music.ru'),
        (10, 'Maxim', sha512('Maxim'), 'Maxim@music.ru');
               ''')
cursor.execute('''
    INSERT INTO playlist (playlist_id, title, user_id, order_num)
    VALUES
        (1, 'MY FAVOURITE', 1, 1),
        (2, 'ROAD', 1, 2),
        (3, 'BEST', 2, 1),
        (4, 'I LIKE IT', 3, 1),
        (5, 'GOOD', 4, 1),
        (6, 'CALM', 5, 1),
        (7, 'IN CONCENTRATION', 6, 1),
        (8, 'DANCE', 7, 1),
        (9, 'NEW', 8, 1),
        (10, 'MUSIC', 9, 1),
        (11, 'THE BEST', 10, 1);
               ''')

cursor.execute('''
    INSERT INTO track (title, performers, album, duration)
    VALUES
               ('Люди', 'Дайте танк', 'Люди', 162),
               ('Riptide', 'Вэнс Джой', 'Live at Red Rocks Amphitheatre', 205),
               ('Лесник', 'Король и Шут', 'Король и Шут', 193),
               ('Vacation', 'Dirty Heads', 'Endless Summer From Better Noise Music', 210),
               ('Ainsi bas la vida', 'Индила', 'Mini World', 216),
               ('Tous les mêmes', 'Stromae', 'Racine Carrée', 218),
               ('The Real Slim Shady', 'Eminem', 'The Marshall Mathers LP', 285),
               ('Wellerman Sea Shanty', 'Nathan Evans', 'Wellerman', 275),
               ('Mockingbird', 'Eminem', 'Curtain Call: The Hits', 251),
               ('Believer', 'Imagine Dragons', 'Throwback Hits', 204),
               ('Lovely', 'Billie Eilish, Khalid', 'Dont Smile at Me', 200 );
               ''')

cursor.execute('''
    INSERT INTO playlist_track (track_id, playlist_id, order_num)
    VALUES
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Vacation') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' ), 4 ),
               ((SELECT track_id FROM track WHERE title ='Believer') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' ), 3 ),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' ), 5 ),
               ((SELECT track_id FROM track WHERE title ='The Real Slim Shady') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='BEST' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Mockingbird') , (SELECT playlist_id FROM playlist WHERE title ='BEST' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='The Real Slim Shady') , (SELECT playlist_id FROM playlist WHERE title ='I LIKE IT' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Vacation') , (SELECT playlist_id FROM playlist WHERE title ='I LIKE IT' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='GOOD' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Lovely') , (SELECT playlist_id FROM playlist WHERE title ='CALM' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Mockingbird') , (SELECT playlist_id FROM playlist WHERE title ='IN CONCENTRATION' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='IN CONCENTRATION' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='DANCE' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Tous les mêmes') , (SELECT playlist_id FROM playlist WHERE title ='DANCE' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='NEW' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='NEW' ), 2),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Lovely') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' ), 3 ),
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' ), 1 ),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' ), 2 ),
               ((SELECT track_id FROM track WHERE title ='Лесник') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' ), 3 );
                ''')
conn.commit()

cursor.close()
conn.close()