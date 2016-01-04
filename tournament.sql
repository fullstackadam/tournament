-- Table definitions for the tournament project.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament;

DROP TABLE IF EXISTS tournaments CASCADE;

CREATE TABLE tournaments (
	id SERIAL PRIMARY KEY,
	name TEXT
);

DROP TABLE IF EXISTS players CASCADE;

CREATE TABLE players (
	id SERIAL PRIMARY KEY,
	name TEXT
);

DROP TABLE IF EXISTS matches CASCADE;

CREATE TABLE matches (
	--tournament SERIAL REFERENCES tournaments(id),
	winner SERIAL REFERENCES players(id),
	loser SERIAL REFERENCES players(id),
	PRIMARY KEY(winner,loser)
);

DROP view IF EXISTS player_standings;

CREATE view player_standings as
SELECT "players"."id","players"."name",(
	SELECT COUNT(*) 
	FROM "matches" 
	WHERE "matches"."winner" = "players"."id"
) as "wins",(
	SELECT COUNT(*) 
	FROM "matches" 
	WHERE "matches"."winner" = "players"."id" 
	OR "matches"."loser" = "players"."id"
) as "matches"
FROM "players"
GROUP BY "players"."id"
ORDER BY "wins";

DROP view IF EXISTS swiss_pairings;

CREATE view swiss_pairings as 
SELECT DISTINCT "p1"."id" as "id1","p1"."name" as "name1","p2"."id" as "id2","p2"."name" as "name2" 
FROM "player_standings" as "p1", "player_standings" as "p2" 
WHERE "p1"."wins" = "p2"."wins" 
AND "p1"."id" <> "p2"."id" 
LIMIT (SELECT (CEIL(COUNT(*)/2.00)) as total FROM "players");