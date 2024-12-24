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
            SELECT  
                t.track_id,
                t.title, 
                t.performers, 
                t.album, 
                RANK() OVER (ORDER BY COUNT(p_t.playlist_id) DESC) rank_cnt_inputs_in_playlists,
                COUNT(p_t.playlist_id)  || '/' ||  (SELECT COUNT(playlist_id) FROM playlist) inputs_in_playlist_OF_all_playlists
                
            FROM track t INNER JOIN playlist_track p_t ON t.track_id = p_t.track_id      
            GROUP BY t.track_id
            ORDER BY rank_cnt_inputs_in_playlists, t.title
                 
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
