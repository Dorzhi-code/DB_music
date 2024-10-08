"""
filing_tables
"""

from yoyo import step

__depends__ = {'20240929_04_0XFW1-create-playlist-track'}

steps = [
    # использовать SHA512()
    # playlist_track можно без подзапроса
    step('''
    INSERT INTO users (username, password, email)
    VALUES
        ('dodo', sha512('dodo'), 'dodo@music.ru' ),
        ('admin', sha512('admin'), 'admin@music.ru'),
        ('user', sha512('user'), 'user@music.ru'),
        ('listener', sha512('listener'), 'listener@music.ru'),
        ('programmer', sha512('programmer'), 'programmer@music.ru'),
        ('worker', sha512('worker'), 'worker@music.ru'),
        ('student', sha512('student'), 'student@music.ru'),
        ('teacher', sha512('teacher'), 'teacher@music.ru'),
        ('Ivan', sha512('Ivan'), 'Ivan@music.ru'),
        ('Maxim', sha512('Maxim'), 'Maxim@music.ru');
               '''),
    step('''
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
               '''),
    step('''
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
               '''),
    step('''
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
]
