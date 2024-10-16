"""
filing_tables
"""

from yoyo import step

__depends__ = {'20240929_04_0XFW1-create-playlist-track'}

steps = [
    step('TRUNCATE playlist_track, users, playlist, track'),   
    step('''
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
               '''),
    step('''
        ALTER SEQUENCE users_user_id_seq RESTART WITH 11;
         '''),

    step('''
    INSERT INTO playlist (playlist_id, title, user_id)
    VALUES
        (1, 'MY FAVOURITE', 1),
        (2, 'ROAD', 1),
        (3, 'BEST', 2),
        (4, 'I LIKE IT', 3),
        (5, 'GOOD', 4),
        (6, 'CALM', 5),
        (7, 'IN CONCENTRATION', 6),
        (8, 'DANCE', 7),
        (9, 'NEW', 8),
        (10, 'MUSIC', 9),
        (11, 'THE BEST', 10);
               '''),
    step('''
    INSERT INTO track (track_id, title, performers, album, duration)
    VALUES
               (1, 'Люди', 'Дайте танк', 'Люди', 162),
               (2, 'Riptide', 'Вэнс Джой', 'Live at Red Rocks Amphitheatre', 205),
               (3, 'Лесник', 'Король и Шут', 'Король и Шут', 193),
               (4, 'Vacation', 'Dirty Heads', 'Endless Summer From Better Noise Music', 210),
               (5, 'Ainsi bas la vida', 'Индила', 'Mini World', 216),
               (6, 'Tous les mêmes', 'Stromae', 'Racine Carrée', 218),
               (7, 'The Real Slim Shady', 'Eminem', 'The Marshall Mathers LP', 285),
               (8, 'Wellerman Sea Shanty', 'Nathan Evans', 'Wellerman', 275),
               (9, 'Mockingbird', 'Eminem', 'Curtain Call: The Hits', 251),
               (10, 'Believer', 'Imagine Dragons', 'Throwback Hits', 204),
               (11, 'Lovely', 'Billie Eilish, Khalid', 'Dont Smile at Me', 200 );
               '''),
    step('''
        ALTER SEQUENCE track_track_id_seq RESTART WITH 12;
         '''),
    step('''
    INSERT INTO playlist_track (track_id, playlist_id, order_num)
    VALUES
               (1 , 1, 1 ),
               (2 , 1, NULL ),
               (4 , 1, 4 ),
               (10 , 1, 3 ),
               (5 , 2, 5 ),
               (7 , 2, 1 ),
               (8 , 2, 2 ),
               (8 , 3, 1 ),
               (9 , 3, 2 ),
               (7 , 4, 1 ),
               (4 , 4, 2 ),
               (5 , 5, 1 ),
               (11 , 6, 1 ),
               (9 , 7, 1 ),
               (2 , 7, 2 ),
               (2 , 8, 1 ),
               (6 , 8, 2 ),
               (5 , 9, 1 ),
               (8 , 9, 2),
               (8 , 10, 1 ),
               (11 , 10, 2 ),
               (1 , 10, 3 ),
               (1 , 11, 1 ),
               (8 , 11, 2 ),
               (3 , 11, 3 );
               ''')                              
]
