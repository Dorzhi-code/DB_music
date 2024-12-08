"""
add_user
"""

from yoyo import step

__depends__ = {'20241208_02_WoOaj-filling-users'}

steps = [
    step('''
    DROP PROCEDURE IF EXISTS add_user(TEXT, TEXT, TEXT);
    CREATE OR REPLACE PROCEDURE add_user(
        IN cur_username TEXT,
        IN cur_password TEXT,
        IN cur_email TEXT     
    )
    LANGUAGE plpgsql AS $$
    BEGIN
        cur_username := TRIM(cur_username);
        cur_password := TRIM(cur_password);
        cur_email := TRIM(cur_email);
        IF LENGTH(cur_username) = 0 OR LENGTH(cur_password) = 0 OR LENGTH(cur_email) = 0 THEN
            RAISE EXCEPTION 'Parameters cannot be emprty or consist only of spaces';
        END IF;

        IF NOT cur_email LIKE '%@%' OR NOT cur_email LIKE '%.%' THEN
            RAISE EXCEPTION 'The mail is not valid';
        END IF;
         
        INSERT INTO users (username, password, email) 
        VALUES (cur_username, cur_password, cur_email);
    END;
    $$;
         ''')
]
