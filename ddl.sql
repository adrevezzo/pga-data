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