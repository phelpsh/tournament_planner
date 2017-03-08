-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

\c tournament

-- works
CREATE TABLE players (
        ID serial,
        name text,
        num_matches int DEFAULT 0
);


CREATE TABLE matches (
        match_id serial,
        winner int,
        loser int
);

