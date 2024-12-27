"""
duration_validation
"""

from yoyo import step

__depends__ = {'20241221_03_0IIsX-album-validation'}

steps = [
    step(
        '''
            DROP TRIGGER IF EXISTS duration_trigger ON track;
        '''
    ),

    step(
        '''
            DROP FUNCTION IF EXISTS duration_validate();
        '''
   ),

    step(
        '''
            CREATE OR REPLACE FUNCTION duration_validate()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                NEW.duration = trunc(NEW.duration);      
                 
                RETURN NEW;
            END;
            $$;
        '''
    ),
    
    step(
        '''
            CREATE TRIGGER duration_trigger
            BEFORE INSERT OR UPDATE ON track
            FOR EACH ROW EXECUTE FUNCTION duration_validate();
        '''
    )
]
