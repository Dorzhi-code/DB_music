"""
created_at__validation
"""

from yoyo import step

__depends__ = {'20241226_01_GrwHj-duration-validation'}

steps = [
    step(
        '''
            DROP TRIGGER IF EXISTS created_at_trigger ON track;
        '''
    ),

    step(
        '''
            DROP FUNCTION IF EXISTS created_at_validate();
        '''
   ),

    step(
        '''
            CREATE OR REPLACE FUNCTION created_at_validate()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                IF NEW.created_at > CURRENT_TIMESTAMP THEN                
                    NEW.created_at = CURRENT_TIMESTAMP;
                END IF;
                RETURN NEW;
            END;
            $$;
        '''
    ),
    
    step(
        '''
            CREATE TRIGGER created_at_trigger
            BEFORE INSERT OR UPDATE ON track
            FOR EACH ROW EXECUTE FUNCTION created_at_validate();
        '''
    )
]
