"""
create_track
"""

from yoyo import step

__depends__ = {'20240929_02_CCvgT-create-playlist'}

steps = [
    step('''
    CREATE TABLE track (
               track_id SERIAL PRIMARY KEY,
               title VARCHAR(255) NOT NULL CHECK(TRIM(title) = title AND LENGTH(title) != 0),
               performers VARCHAR(400) NOT NULL CHECK(TRIM(title) = title AND LENGTH(title) != 0),
               album VARCHAR(255) NOT NULL CHECK(TRIM(title) = title AND LENGTH(title) != 0),
               duration SMALLINT NOT NULL CHECK (duration > 0.0),
               created_at timestamp NOT NULL default now()            
               );
               ''')
]
