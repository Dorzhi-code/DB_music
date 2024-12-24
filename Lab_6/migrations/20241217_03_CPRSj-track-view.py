"""
Playlist view
"""

from yoyo import step

__depends__ = {}

steps = [ 
    step(
        '''
            DROP VIEW IF EXISTS playlist_info
        '''
    ),   
    step(
        '''
            CREATE OR REPLACE VIEW playlist_info  AS
            SELECT             
                p.playlist_id,
                p.title playlist,                
                t.track_id,  
                t.title AS track, 
                t.performers, 
                t.album,                 
                p_t.order_num track_order,
                p_t.created_at
            FROM track t 
                JOIN playlist_track p_t ON t.track_id = p_t.track_id 
                RIGHT JOIN playlist p ON p_t.playlist_id = p.playlist_id   
            ORDER BY p.playlist_id ASC, p_t.order_num ASC, t.created_at ASC
        '''
    ),
    step(
        '''
            CREATE OR REPLACE FUNCTION update_playlist_info()
            RETURNS TRIGGER AS $$
            BEGIN
                IF (TG_OP = 'UPDATE') THEN
                    UPDATE playlist
                    SET 
                        title = NEW.playlist
                    WHERE playlist_id = OLD.playlist_id;

                    UPDATE playlist_track
                    SET
                        order_num = NEW.track_order
                    WHERE playlist_id = OLD.playlist_id AND track_id = OLD.track_id;

                    RETURN NEW;

                ELSIF (TG_OP = 'DELETE') THEN
                    DELETE FROM playlist_track WHERE track_id = OLD.track_id;      

                    RETURN OLD;
                END IF;
            END;
            $$ LANGUAGE plpgsql;
        '''
    ),
    step(
        '''
            DROP TRIGGER IF EXISTS playlist_info_trigger ON playlist_info
        '''
    ),
    step(
        '''
            CREATE TRIGGER playlist_info_trigger
            INSTEAD OF UPDATE OR DELETE ON playlist_info
            FOR EACH ROW
            EXECUTE FUNCTION update_playlist_info();
        '''
    )
]
