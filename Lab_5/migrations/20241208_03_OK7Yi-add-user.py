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
        cur_username := TRIM(regexp_replace(cur_username, '\s+', ' ', 'g'));
        cur_password := TRIM(regexp_replace(cur_password, '\s+', ' ', 'g'));
        cur_email := TRIM(regexp_replace(cur_email, '\s+', ' ', 'g'));
         
        IF LENGTH(cur_username) = 0 THEN
            RAISE EXCEPTION 'Username cannot be empty or consist only of spaces';
        END IF;
        
        IF LENGTH(cur_password) = 0 THEN
            RAISE EXCEPTION 'Password cannot be empty or consist only of spaces';
        END IF;
        
        IF LENGTH(cur_email) = 0 THEN
            RAISE EXCEPTION 'E-mail cannot be empty or consist only of spaces';
        END IF;
        
        IF cur_username ~  '^[0-9]+$' THEN
            RAISE EXCEPTION 'Username cannot be only of numbers';
        END IF;         

        IF NOT cur_email LIKE '%@%.%'  THEN
            RAISE EXCEPTION 'The e-mail is not valid. E-mail must be in the format {text@text.text}';
        END IF;
         
        IF EXISTS (SELECT 1 FROM users WHERE email = LOWER(cur_email)) THEN
            RAISE EXCEPTION 'The e-mail is already taken. Enter a another';
        END IF;
        
        INSERT INTO users (username, password, email) 
        VALUES (cur_username, cur_password, cur_email);
    END;
    $$;
         ''')
]
