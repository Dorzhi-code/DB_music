"""
Create users
"""

from yoyo import step

__depends__ = {}

steps = [
    step('''
    CREATE TABLE users (
               user_id SERIAL PRIMARY KEY,
               username VARCHAR(255) UNIQUE,
               password VARCHAR(130) NOT NULL,
               email VARCHAR(255) UNIQUE CHECK(TRIM(email) = email) ,
               created_at timestamp NOT NULL default now()
               );
         ''')
]
