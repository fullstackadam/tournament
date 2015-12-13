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
	--tournament SERIAL REFERENCES tournaments(id),
	winner SERIAL REFERENCES players(id),
	loser SERIAL REFERENCES players(id)
);

CREATE view player_standings as
SELECT "id","name",COUNT("winner") as "wins", (
    SELECT COUNT(*)
    FROM "players" as "ps"
    LEFT JOIN "matches" as "ms" ON "ms"."winner" = "players"."id"
    OR "ms"."loser" = "players"."id"
    WHERE "ps"."id" = "players"."id"
    AND ("ms"."winner"="players"."id"
    OR "ms"."loser"="players"."id")
) as "matchs"
    FROM "players"
    LEFT JOIN "matches" ON "winner" = "id"
    GROUP BY "id";

CREATE view swiss_pairings as
SELECT "id","name",COUNT("winner")
as "total"
FROM "players"
LEFT JOIN "matches"
on "matches"."winner" = "players"."id"
GROUP BY "id"
ORDER BY "total";