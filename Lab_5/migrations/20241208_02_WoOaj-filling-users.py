"""
Filling users
"""

from yoyo import step

__depends__ = {'20241208_01_r8l6e-create-users'}

steps = [
    step('TRUNCATE users'),   
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
]
