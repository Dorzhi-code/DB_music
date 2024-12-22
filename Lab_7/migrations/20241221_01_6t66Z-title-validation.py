'''
title_validation
'''

from yoyo import step

__depends__ = {}

steps = [    
    step(
        '''
            DROP TRIGGER IF EXISTS title_trigger ON track;
        '''
    ),

    step(
        '''
            DROP FUNCTION IF EXISTS title_validate();
        '''
   ),

    step(
        '''
            CREATE OR REPLACE FUNCTION title_validate()
            RETURNS trigger
            LANGUAGE plpgsql
            AS $$
            BEGIN
                NEW.title = TRIM(regexp_replace(NEW.title, '\s+', ' ', 'g'));
                
                IF NEW.title ~ '[a-zA-Z]' THEN
                    NEW.title = INITCAP(NEW.title);   
                ELSE             
                    NEW.title = UPPER(SUBSTRING(NEW.title FROM 1 FOR 1)) || SUBSTRING(NEW.title FROM 2 FOR length(NEW.title));
                END IF;


                RETURN NEW;
            END;
            $$;
        '''
    ),
    
    step(
        '''
            CREATE TRIGGER title_trigger
            BEFORE INSERT OR UPDATE ON track
            FOR EACH ROW EXECUTE FUNCTION title_validate();
        '''
    )
]
