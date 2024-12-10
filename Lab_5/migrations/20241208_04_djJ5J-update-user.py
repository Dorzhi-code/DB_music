"""
update__user
"""

from yoyo import step

__depends__ = {'20241208_03_OK7Yi-add-user'}

steps = [
step('''
    DROP PROCEDURE IF EXISTS update_user(TEXT,TEXT,TEXT,TEXT);
    CREATE OR REPLACE PROCEDURE update_user(
        IN cur_user_id TEXT, 
        IN cur_username TEXT,
        IN cur_password TEXT,
        IN cur_email TEXT 
    )
    LANGUAGE plpgsql AS $$
    BEGIN
        cur_username := TRIM(regexp_replace(cur_username, '\s+', ' ', 'g'));
        cur_password := TRIM(regexp_replace(cur_password, '\s+', ' ', 'g'));
        cur_email := TRIM(regexp_replace(cur_email, '\s+', ' ', 'g'));
        IF LENGTH(cur_user_id) = 0 OR NOT cur_user_id ~ '^[0-9]+$' THEN
            RAISE EXCEPTION 'The user id must be a positive integer and cannot be empty ';
        END IF;
        DECLARE
            cur_user_id INT := CAST(cur_user_id AS INT);
        BEGIN
            
     
            IF NOT EXISTS (SELECT 1 FROM users WHERE user_id = cur_user_id) THEN
                RAISE EXCEPTION 'User with ID % not found', cur_user_id;
            END IF;
            IF cur_username IS NOT NULL AND cur_username <> '' THEN                
                UPDATE users 
                SET username = cur_username
                WHERE user_id = cur_user_id;
            END IF;
            IF cur_password IS NOT NULL AND cur_password <> '' THEN
                UPDATE users 
                SET password = cur_password
                WHERE user_id = cur_user_id;
            END IF;
            IF cur_email IS NOT NULL AND cur_email <> '' THEN
                IF cur_email LIKE '%@%.%' THEN
                    UPDATE users 
                    SET email = cur_email
                    WHERE user_id = cur_user_id;
                ELSE
                    RAISE EXCEPTION 'The mail is not valid. Mail must be in the format {text@text.text}';
                END IF;
            END IF;
        END;
    END;
    $$;
    ''')
]
