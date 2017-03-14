-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;

\c tournament

-- works
CREATE TABLE players (
        ID serial PRIMARY KEY,
        name text
);


CREATE TABLE matches (
        match_id serial PRIMARY KEY,
        winner int REFERENCES players (ID),
        loser int REFERENCES players (ID)
);

CREATE VIEW Losses AS
    SELECT players.ID, count(matches.loser) as losses
    FROM players LEFT JOIN matches on players.ID = matches.loser 
    group by players.ID;

CREATE VIEW Wins AS
    SELECT players.ID, count(matches.winner) as wins
    FROM players LEFT JOIN matches on players.ID = matches.winner 
    group by players.ID;

CREATE VIEW total_matches AS
	SELECT Wins.ID, Wins.wins + Losses.losses AS tmatches 
	FROM Wins, Losses
	WHERE Wins.ID = Losses.ID;

CREATE VIEW Standings AS
	SELECT Wins.ID as ID, players.name, Wins.wins, 
	total_matches.tmatches FROM Wins
	JOIN players ON players.ID = Wins.ID
	JOIN total_matches ON total_matches.ID = Wins.ID
	ORDER BY Wins.wins DESC;
