-- Table with Incrementing Integer ID
CREATE TABLE academy_award_winning_films (
    id INTEGER PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    year INTEGER,
    awards INTEGER,
    nominations INTEGER
);

-- Table with UUID (Other RDBMS)
CREATE TABLE academy_award_winning_films (
    id VARCHAR(36) PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    year INTEGER,
    awards INTEGER,
    nominations INTEGER
);

-- Table with UUID (Postgres - supports UUID natively)
CREATE TABLE academy_award_winning_films (
    id UUID PRIMARY KEY,
    film VARCHAR(255) NOT NULL,
    year INTEGER,
    awards INTEGER,
    nominations INTEGER
);