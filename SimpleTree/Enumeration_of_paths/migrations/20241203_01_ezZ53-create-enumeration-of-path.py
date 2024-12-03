"""
create enumeration of path
"""

from yoyo import step

__depends__ = {}

steps = [
    step('''
    CREATE TABLE path_enum(
         id SERIAL PRIMARY KEY,
         title VARCHAR(255) UNIQUE CHECK(TRIM(title) = title AND LENGTH(title) != 0),
         path VARCHAR(255) UNIQUE CHECK(TRIM(title) = title AND LENGTH(title) != 0)
         )
         ''')
]
