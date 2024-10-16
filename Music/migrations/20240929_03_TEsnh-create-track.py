"""
create_track
"""

from yoyo import step

__depends__ = {'20240929_02_CCvgT-create-playlist'}

steps = [
    step('''
    CREATE TABLE track (
               track_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL,
               performers VARCHAR(400) NOT NULL,
               album VARCHAR(255) NOT NULL,
               duration SMALLINT NOT NULL CHECK (duration > 0),
               created_at timestamp NOT NULL default now()            
               );
               ''')
]
