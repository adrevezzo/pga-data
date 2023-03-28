# GLOBAL QUERIES
PLAYER_ID_SELECT = """
SELECT id FROM players WHERE pga_id = %s

"""

PLAYER_RESULTS_INSERT_QUERY = """
INSERT INTO player_results (
    player_id,
    tournament_id,
    tournament_end_date,
    finish_position,
    r1,
    r2,
    r3,
    r4,
    total,
    to_par,
    points_rank,
    tournament_points
    ) 
    
VALUES
(%s, %s, to_date(%s, 'MM.DD.YYYY'), %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

TOURNAMENT_ID_SELECT = """
    SELECT id FROM tournaments WHERE pga_tournament_id = %s
"""