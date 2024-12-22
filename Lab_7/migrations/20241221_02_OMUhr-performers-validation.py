"""
performers_validation
"""

from yoyo import step

__depends__ = {'20241221_01_6t66Z-title-validation'}

steps = [
    step(
        '''
            DROP TRIGGER IF EXISTS performers_trigger ON track;
        '''
    ),

    step(
        '''
            DROP FUNCTION IF EXISTS performers_validate();
        '''
   ),

    step(
        '''
            CREATE OR REPLACE FUNCTION performers_validate()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                NEW.performers = TRIM(regexp_replace(NEW.performers, '\s+', ' ', 'g'));      
                NEW.performers = UPPER(SUBSTRING(NEW.performers FROM 1 FOR 1)) || SUBSTRING(NEW.performers FROM 2 FOR length(NEW.performers));
                RETURN NEW;
            END;
            $$;
        '''
    ),
    
    step(
        '''
            CREATE TRIGGER performers_trigger
            BEFORE INSERT OR UPDATE ON track
            FOR EACH ROW EXECUTE FUNCTION performers_validate();
        '''
    )
]
