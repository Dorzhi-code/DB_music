"""
get_user
"""

from yoyo import step

__depends__ = {'20241208_07_DFu3Y-get-all-users'}

steps = [
    step("""
        DROP FUNCTION IF EXISTS get_user(TEXT);
        CREATE OR REPLACE FUNCTION get_user(IN cur_user_id TEXT)
        RETURNS TABLE(user_id INT, username VARCHAR(255), password VARCHAR(130), email VARCHAR(255)) AS $$
        DECLARE
            cur_id INT;
        BEGIN
            cur_user_id := TRIM(cur_user_id);
            IF LENGTH(cur_user_id) = 0 OR NOT cur_user_id ~ '^[0-9]+$' OR (cur_user_id = '0') THEN
                RAISE EXCEPTION 'The identifier must be a positive integer and cannot be empty';
            END IF;
            
            cur_id := CAST(cur_user_id AS INT);
            
            IF NOT EXISTS (SELECT 1 FROM users WHERE users.user_id = cur_id) THEN
                RAISE EXCEPTION 'Users with ID % not found', cur_id;
            END IF;
            
            RETURN QUERY SELECT users.user_id, users.username, users.password, users.email  FROM users WHERE users.user_id = cur_id;
        END;
        $$ LANGUAGE plpgsql;
    """)
]
