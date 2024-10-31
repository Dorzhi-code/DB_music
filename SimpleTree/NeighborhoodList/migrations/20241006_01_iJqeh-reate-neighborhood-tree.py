"""
reate_neighborhood_tree
"""

from yoyo import step

__depends__ = {}

steps = [
    step('''
    CREATE TABLE neighborhood_tree(
         id SERIAL PRIMARY KEY,
         title VARCHAR(255) UNIQUE CHECK(TRIM(title) = title AND LENGTH(title) != 0),
         parent_id INTEGER REFERENCES neighborhood_tree(id) ON DELETE CASCADE     
         )
         ''')
]
