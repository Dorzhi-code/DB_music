"""
create_users
"""

from yoyo import step

__depends__ = {}

steps = [
    step('''
    CREATE TABLE users (
               user_id SERIAL PRIMARY KEY,
               username VARCHAR(255) NOT NULL,
               password VARCHAR(255) NOT NULL,
               email VARCHAR(255) UNIQUE
               );
               ''')
]
