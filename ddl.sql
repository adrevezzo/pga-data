CREATE TABLE players IF NOT EXISTS (
    id INT SERIAL PRIMARY KEY,
    pga_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    age INT,
    headshot_location VARCHAR(255),
    country VARCHAR(255),
    country_flag VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS player_results  (
    id INT SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
	tournament_id INT NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    tournament_end_date VARCHAR(80) NOT NULL
    finish_position VARCHAR(10) NOT NULL,
    r1 INT,
	r2 INT,
	r3 INT,
	r4 INT,
    total INT,
    points_rank INT,
	tournament_points FLOAT
);

CREATE TABLE IF NOT EXISTS tournaments  (
    id SERIAL PRIMARY KEY,
    pga_tournament_id VARCHAR(50) NOT NULL,
	tournament_name VARCHAR(255) NOT NULL,
    first_place_earnings VARCHAR(80) NOT NULL,
    purse VARCHAR(80) NOT NULL,
	city VARCHAR(255) NOT NULL,
	country VARCHAR(255) NOT NULL,
	course_name VARCHAR(255) NOT NULL,
    month VARCHAR(50) NOT NULL,
    year VARCHAR(6) NOT NULL,
    season_year VARCHAR(50) NOT NULL
);