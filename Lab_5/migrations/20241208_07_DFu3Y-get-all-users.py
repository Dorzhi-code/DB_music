"""
get_all_users
"""

from yoyo import step

__depends__ = {'20241208_06_q3vTL-delete-many-users'}

steps = [
      step("""
        DROP FUNCTION IF EXISTS get_all_users();
        CREATE OR REPLACE FUNCTION get_all_users()
        RETURNS TABLE(user_id INT, username VARCHAR(255), password VARCHAR(130), email VARCHAR(255)) AS $$
        BEGIN
            RETURN QUERY
                SELECT users.user_id, users.username, users.password, users.email 
                FROM users  ORDER BY users.user_id;
        END;
        $$ LANGUAGE plpgsql;
    """)
]
