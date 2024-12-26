"""
album_validation
"""

from yoyo import step

__depends__ = {'20241221_02_OMUhr-performers-validation'}

steps = [
    step(
        '''
            DROP TRIGGER IF EXISTS album_trigger ON track;
        '''
    ),

    step(
        '''
            DROP FUNCTION IF EXISTS album_validate();
        '''
   ),

    step(
        '''
            CREATE OR REPLACE FUNCTION album_validate()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                NEW.album = TRIM(regexp_replace(NEW.album, '\s+', ' ', 'g'));      

                RETURN NEW;
            END;
            $$;
        '''
    ),
    
    step(
        '''
            CREATE TRIGGER album_trigger
            BEFORE INSERT OR UPDATE ON track
            FOR EACH ROW EXECUTE FUNCTION album_validate();
        '''
    )
]
