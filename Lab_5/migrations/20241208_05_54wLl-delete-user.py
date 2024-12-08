"""
delete_user
"""

from yoyo import step

__depends__ = {'20241208_04_djJ5J-update-user'}

steps = [
    step('''
        DROP PROCEDURE IF EXISTS delete_user(TEXT);
        CREATE OR REPLACE PROCEDURE delete_user(IN cur_user_id TEXT)
        LANGUAGE plpgsql AS $$
        DECLARE
            cur_id INT;
        BEGIN
            cur_id := NULLIF(TRIM(cur_user_id), '');
            IF cur_id IS NULL OR NOT (cur_user_id ~ '^[0-9]+$') OR (cur_user_id = '0') THEN
                RAISE EXCEPTION 'The user id must be a positive integer and cannot be empty';
            END IF;
            cur_id := CAST(cur_id AS INT);

            IF NOT EXISTS (SELECT 1 FROM users WHERE user_id = cur_id) THEN
                RAISE EXCEPTION 'Users with ID % not found', cur_id;
            END IF;
            DELETE FROM users WHERE user_id = cur_id;
        END;
        $$;
    ''')
]
