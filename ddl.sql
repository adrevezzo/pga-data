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
    id SERIAL PRIMARY KEY,
    player_id INT NOT NULL REFERENCES players(id) ON DELETE CASCADE,
	tournament_id INT NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    tournament_end_date VARCHAR(80) NOT NULL,
    finish_position VARCHAR(10) NOT NULL,
    r1 INT,
	r2 INT,
	r3 INT,
	r4 INT,
    total INT,
    to_par VARCHAR(10),
    points_rank INT,
	tournament_points FLOAT
);
);

CREATE TABLE IF NOT EXISTS tournaments  (
    id SERIAL PRIMARY KEY,
    pga_tournament_id VARCHAR(50) NOT NULL,
	tournament_num INT NOT NULL,
    tournament_name VARCHAR(255) NOT NULL,
    first_place_earnings VARCHAR(80) NOT NULL,
    purse VARCHAR(80) NOT NULL,
	city VARCHAR(255) NOT NULL,
    state VARCHAR(255) NOT NULL,
	country VARCHAR(255) NOT NULL,
	course_name VARCHAR(255) NOT NULL,
    month VARCHAR(50) NOT NULL,
    year VARCHAR(6) NOT NULL,
    season_year VARCHAR(50) NOT NULL
);

-- Create Courses Table from Tournament Data and remove duplicate columns from Tournaments
CREATE TABLE courses (
	ID SERIAL PRIMARY KEY,
	course_name VARCHAR(255) NOT NULL,
	course_id_pga VARCHAR(10),
	city VARCHAR(255),
	state VARCHAR(255),
	country VARCHAR(255)

);

INSERT INTO courses (course_name, city, state, country)
SELECT 
DISTINCT 
course_name,
city,
state,
country

FROM tournaments;

ALTER TABLE tournaments
ADD column course_id INT;

UPDATE tournaments
SET course_id = courses.id
FROM courses 
WHERE tournaments.course_name = courses.course_name; 

ALTER TABLE tournaments
DROP COLUMN city,
DROP COLUMN state,
DROP COLUMN country,
DROP COLUMN course_name;