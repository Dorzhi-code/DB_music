"""
delete_many_users
"""

from yoyo import step

__depends__ = {'20241208_05_54wLl-delete-user'}

steps = [
    step('''
        DROP FUNCTION IF EXISTS delete_many_users(TEXT[]);
        CREATE OR REPLACE FUNCTION delete_many_users(cur_user_ids TEXT[])
        RETURNS INTEGER AS $$
        DECLARE
            cur_id INT;
            deleted_count INT := 0; 
            id TEXT; 
        BEGIN
            FOREACH id IN ARRAY cur_user_ids LOOP
                IF id IS NULL OR NOT id ~ '^[0-9]+$' THEN
                    RAISE NOTICE 'ID % is not valid.', id;
                    CONTINUE; 
                END IF;
                cur_id := id::INT;
                IF EXISTS (SELECT 1 FROM users WHERE user_id = cur_id) THEN
                    DELETE FROM users WHERE user_id = cur_id;
                    deleted_count := deleted_count + 1;  
                ELSE
                    RAISE NOTICE 'The user with ID % was not found.', cur_id;
                END IF;
            END LOOP;
            RAISE NOTICE 'Removed users: %', deleted_count;
            RETURN deleted_count;  
        END;
        $$ LANGUAGE plpgsql;
    ''')
]
