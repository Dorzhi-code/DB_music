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
               password BYTEA NOT NULL,
               email VARCHAR(255) UNIQUE,
               created_at timestamp NOT NULL default now()         
               );
               ''')
]
