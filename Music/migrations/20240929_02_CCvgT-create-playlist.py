"""
create_playlist
"""

from yoyo import step

__depends__ = {'20240929_01_Ura3S-create-users'}

steps = [
    step('''
    CREATE TABLE playlist (
               playlist_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               user_id INTEGER REFERENCES users(user_id),
               order_num SMALLINT NULL,
               created_at timestamp NOT NULL default now()         
               );
               ''')
]
