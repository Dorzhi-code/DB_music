import psycopg2

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
conn.commit()

cursor.execute('''
    CREATE TABLE playlist (
               playlist_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               user_id INTEGER REFERENCES users(user_id)
               );
               ''')
conn.commit()

cursor.execute('''
    CREATE TABLE track (
               track_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               performers VARCHAR(255) NOT NULL,
               album VARCHAR(255),
               duration INTEGER CHECK(duration > 0)
               );
               ''')
conn.commit()

cursor.execute('''
    CREATE TABLE playlist_track (
               track_id INTEGER REFERENCES track(track_id),
               playlist_id INTEGER REFERENCES playlist(playlist_id)
               );
               ''')
conn.commit()


cursor.execute('''
    INSERT INTO users (username, password, email)
    VALUES
        ('dodo', 'ac94f165c526746256350c02e01a87e0b46f787494148382383b6b491b9e41587acc83a48aeb4f5e8ff627f14466f90b61acdadc2594c60b447494f306a853b3', 'dodo@music.ru' ),
        ('admin', 'c7ad44cbad762a5da0a452f9e854fdc1e0e7a52a38015f23f3eab1d80b931dd472634dfac71cd34ebc35d16ab7fb8a90c81f975113d6c7538dc69dd8de9077ec', 'admin@music.ru'),
        ('user', 'b14361404c078ffd549c03db443c3fede2f3e534d73f78f77301ed97d4a436a9fd9db05ee8b325c0ad36438b43fec8510c204fc1c1edb21d0941c00e9e2c1ce2', 'user@music.ru'),
        ('listener','5c3633c91d7953c56e99385dca87576eaf8c58694b0491c50647787969b68016e85755bc9b81f6eec6eb5ccb1e5ffce50936bd457efd4a1c5a5204486ece1802', 'listener@music.ru'),
        ('programmer', '4fac82db65d414cae66f72c5ea8a3acde71dac73cf59539995a54bd5232356566b3e5fe415b97da67fb6cd121c3feb826ae46b1fdefa07d3a21980343f1333c4', 'programmer@music.ru'),
        ('worker', '43c6fffaa75a48fdf6aeec373647a3b6a05890f3689e686bbc3a7c0f90b051e5a5c41e2665165dfbc24da1d2f972630bea94439b2ba6dc2f3b2a1373d4d7724f', 'worker@music.ru'),
        ('student', '32ade5e7c36fa329ea39dbc352743db40da5aa7460ec55f95b999d6371ad20170094d88d9296643f192e9d5433b8d6d817d6777632e556e96e58f741dc5b3550', 'student@music.ru'),
        ('teacher', '50ecc45020be014e68d714cd076007e84a9621d9a5e589a916e45273014830b399d143a57f525554bfe9e751d97fe0fa884dbdea7b07721723b4eff39e9d28ad', 'teacher@music.ru'),
        ('Ivan', '8adac786fdbd70ba1fd8b8d40fb21875429882d4b41cb2a556f89f396b8ae72247613f603b9d0e6c53898186651cfd8f27f72cf6664613e42d5206c843460a7f', 'Ivan@music.ru'),
        ('Maxim', '15ff60f75add6975e19653949ef74388f53ea1261b372a31c0bcd06df28f2c8d4f6ce983f19cc1ef70fb67419ccb2a144600bfb3a41993be422c09eba8783858', 'Maxim@music.ru');
               ''')
conn.commit()

cursor.execute('''
    INSERT INTO playlist (title, user_id)
    VALUES
        ('MY FAVOURITE', (SELECT user_id FROM users WHERE username = 'dodo')),
        ('ROAD', (SELECT user_id FROM users WHERE username = 'dodo')),
        ('BEST', (SELECT user_id FROM users WHERE username = 'admin')),
        ('I LIKE IT', (SELECT user_id FROM users WHERE username = 'user')),
        ('GOOD', (SELECT user_id FROM users WHERE username = 'listener')),
        ('CALM', (SELECT user_id FROM users WHERE username = 'programmer')),
        ('IN CONCENTRATION', (SELECT user_id FROM users WHERE username = 'worker')),
        ('DANCE', (SELECT user_id FROM users WHERE username = 'student')),
        ('NEW', (SELECT user_id FROM users WHERE username = 'teacher')),
        ('MUSIC', (SELECT user_id FROM users WHERE username = 'Ivan')),
        ('THE BEST', (SELECT user_id FROM users WHERE username = 'Maxim'));
               ''')
conn.commit()

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
conn.commit()

cursor.execute('''
    INSERT INTO playlist_track (track_id, playlist_id)
    VALUES
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' )),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' )),
               ((SELECT track_id FROM track WHERE title ='Believer') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' )),
               ((SELECT track_id FROM track WHERE title ='Vacation') , (SELECT playlist_id FROM playlist WHERE title ='MY FAVOURITE' )),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' )),
               ((SELECT track_id FROM track WHERE title ='The Real Slim Shady') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' )),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='ROAD' )),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='BEST' )),
               ((SELECT track_id FROM track WHERE title ='Mockingbird') , (SELECT playlist_id FROM playlist WHERE title ='BEST' )),
               ((SELECT track_id FROM track WHERE title ='The Real Slim Shady') , (SELECT playlist_id FROM playlist WHERE title ='I LIKE IT' )),
               ((SELECT track_id FROM track WHERE title ='Vacation') , (SELECT playlist_id FROM playlist WHERE title ='I LIKE IT' )),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='GOOD' )),
               ((SELECT track_id FROM track WHERE title ='Lovely') , (SELECT playlist_id FROM playlist WHERE title ='CALM' )),
               ((SELECT track_id FROM track WHERE title ='Mockingbird') , (SELECT playlist_id FROM playlist WHERE title ='IN CONCENTRATION' )),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='IN CONCENTRATION' )),
               ((SELECT track_id FROM track WHERE title ='Riptide') , (SELECT playlist_id FROM playlist WHERE title ='DANCE' )),
               ((SELECT track_id FROM track WHERE title ='Tous les mêmes') , (SELECT playlist_id FROM playlist WHERE title ='DANCE' )),
               ((SELECT track_id FROM track WHERE title ='Ainsi bas la vida') , (SELECT playlist_id FROM playlist WHERE title ='NEW' )),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='NEW' )),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' )),
               ((SELECT track_id FROM track WHERE title ='Lovely') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' )),
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='MUSIC' )),
               ((SELECT track_id FROM track WHERE title ='Люди') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' )),
               ((SELECT track_id FROM track WHERE title ='Wellerman Sea Shanty') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' )),
               ((SELECT track_id FROM track WHERE title ='Лесник') , (SELECT playlist_id FROM playlist WHERE title ='THE BEST' ));
               ''')
conn.commit()

cursor.close()
conn.close()