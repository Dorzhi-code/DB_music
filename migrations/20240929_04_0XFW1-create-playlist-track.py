"""
create_playlist_track
"""

from yoyo import step

__depends__ = {'20240929_03_TEsnh-create-track'}

steps = [
    step('''
    CREATE TABLE playlist_track (
               track_id INTEGER REFERENCES track(track_id),
               playlist_id INTEGER REFERENCES playlist(playlist_id),
               order_num INTEGER  NOT NULL,
               created_at timestamp NOT NULL default now()
               );
               ''')
]
