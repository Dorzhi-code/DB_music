"""
track rank view
"""

from yoyo import step

__depends__ = {'20241217_03_CPRSj-track-view'}

steps = [
    step(
        '''
            DROP MATERIALIZED VIEW IF EXISTS track_stats
        '''
    ),         
    step(
        '''
            CREATE MATERIALIZED VIEW track_stats AS
            SELECT DISTINCT 
                t.track_id,
                t.title, 
                t.performers, 
                t.album, 
                COUNT(p_t.playlist_id) OVER (PARTITION BY p_t.track_id ) rank
            FROM track t INNER JOIN playlist_track p_t ON t.track_id = p_t.track_id      
            UNION
            SELECT DISTINCT 
                t.track_id,
                t.title, 
                t.performers, 
                t.album, 
                0 rank
            FROM track t
            WHERE track_id NOT IN (SELECT track_id FROM playlist_track)
            ORDER BY rank DESC        
        '''
    ),
    step(
        '''
            CREATE OR REPLACE FUNCTION refresh_track()
            RETURNS TRIGGER LANGUAGE plpgsql
            AS $$
            BEGIN
                REFRESH MATERIALIZED VIEW track_stats;
                RETURN NULL;
            END $$;
        '''
    ),
    step(
        '''
            DROP TRIGGER IF EXISTS refresh_view ON track;
        '''
    ),
   
    step(
        '''
            CREATE OR REPLACE TRIGGER refresh_view
            AFTER
            INSERT OR UPDATE OR DELETE
            ON track
            FOR EACH ROW
            EXECUTE FUNCTION refresh_track();    
        '''
    ),

    step(
        '''
            DROP TRIGGER IF EXISTS refresh_view ON playlist_track;
        '''
    ),

    step(
        '''
            CREATE OR REPLACE TRIGGER refresh_view
            AFTER
            INSERT OR UPDATE OR DELETE
            ON playlist_track
            FOR EACH ROW
            EXECUTE FUNCTION refresh_track();
        '''
    )
]
