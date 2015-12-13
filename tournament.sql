-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


CREATE DATABASE tournament;

CREATE TABLE tournaments (
	id SERIAL PRIMARY KEY,
	name TEXT
);

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT
);

CREATE TABLE matches (
	id SERIAL PRIMARY KEY,
	--tournament SERIAL REFERENCES tournaments(id),
	winner SERIAL REFERENCES players(id),
	loser SERIAL REFERENCES players(id)
);

CREATE view player_standings as
SELECT "id","name",COUNT("winner") as "wins", (
	SELECT "matches" 
	FROM "match_counts"
	WHERE "match_counts"."id" = "players"."id"
) as "matches"
FROM "players"
LEFT JOIN "matches" ON "winner" = "id"
GROUP BY "id";

CREATE view match_counts as
SELECT "players"."id",COUNT(*) as "matches"
FROM "players"
LEFT JOIN "matches" ON "matches"."winner" = "players"."id"
OR "matches"."loser" = "players"."id"
GROUP BY "players"."id";

CREATE view swiss_pairings as
SELECT "id","name",COUNT("winner")
as "total"
FROM "players"
LEFT JOIN "matches"
on "matches"."winner" = "players"."id"
GROUP BY "id"
ORDER BY "total";