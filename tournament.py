#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("databasename=tournament")

def delete_matches():
    """Remove all the match records from the database."""
    database = connect()
    cursor = database.cursor()
    cursor.execute('DELETE FROM matches')
    database.commit()
    database.close()

def delete_players():
    """Remove all the player records from the database."""
    database = connect()
    cursor = database.cursor()
    cursor.execute('DELETE FROM players')
    database.commit()
    database.close()

def count_players():
    """Returns the number of players currently registered."""
    database = connect()
    cursor = database.cursor()
    cursor.execute('SELECT COUNT(*) FROM players')
    total = cursor.fetchone()[0]
    database.close()
    return total

def register_player(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    database = connect()
    cursor = database.cursor()
    player = (name, )
    cursor.execute('INSERT INTO players (name) VALUES (%s)', player)
    database.commit()
    database.close()

def player_standings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    database = connect()
    cursor = database.cursor()
    query = 'SELECT "id","name",COUNT("winner") as "wins",(' \
    'SELECT COUNT(*)' \
    'FROM "players" as "ps"' \
    'LEFT JOIN "matches" as "ms" ON "ms"."winner" = "players"."id" ' \
    'OR "ms"."loser" = "players"."id"' \
    'WHERE "ps"."id" = "players"."id"' \
    'AND ("ms"."winner"="players"."id" ' \
    'OR "ms"."loser"="players"."id")) as "matchs"' \
    'FROM "players" ' \
    'LEFT JOIN "matches" ON "winner" = "id" ' \
    'GROUP BY "id"'
    cursor.execute(query)
    standings = cursor.fetchall()
    database.close()
    return standings

def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match = (winner, loser, )
    database = connect()
    cursor = database.cursor()
    cursor.execute('INSERT INTO matches (winner,loser) VALUES (%s,%s)', match)
    database.commit()
    database.close()

def swiss_pairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    database = connect()
    cursor = database.cursor()

    query = 'SELECT id,name,COUNT(winner) ' \
    'as total ' \
    'FROM players ' \
    'LEFT JOIN matches ' \
    'on matches.winner = players.id ' \
    'GROUP BY id ' \
    'ORDER BY total'

    cursor.execute(query)
    players = cursor.fetchall()
    database.close()
    player1 = True
    for player in players:
        if player1:
            player1data = player[0], player[1]
            player1 = False
        else:
            match = (player1data[0], player1data[1], player[0], player[1])
            try:
                pairings = pairings, match
            except NameError:
                pairings = match
            player1 = True

    return pairings
