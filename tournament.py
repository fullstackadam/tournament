#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute('DELETE FROM matches')
    DB.commit()
    DB.close()

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute('DELETE FROM players')
    DB.commit()
    DB.close()

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute('SELECT COUNT(*) FROM players')
    total = c.fetchone()[0]
    DB.close()
    return total

def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    player = (name, )
    c.execute('INSERT INTO players (name) VALUES (%s)', player)
    DB.commit()
    DB.close()

def playerStandings():
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
    DB = connect()
    c = DB.cursor()
    q = 'SELECT "id","name",COUNT("winner") as "wins",(' \
    'SELECT COUNT(*)' \
    'FROM "players" as "ps"' \
    'LEFT JOIN "matches" as "ms" ON "ms"."winner" = "players"."id" OR "ms"."loser" = "players"."id"' \
    'WHERE "ps"."id" = "players"."id"' \
    'AND ("ms"."winner"="players"."id" OR "ms"."loser"="players"."id")) as "matchs"' \
    'FROM "players" ' \
    'LEFT JOIN "matches" ON "winner" = "id"' \
    'GROUP BY "id"'
    c.execute(q)
    standings = c.fetchall()
    DB.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match = (winner, loser, )
    DB = connect()
    c = DB.cursor()
    c.execute('INSERT INTO matches (winner,loser) VALUES (%s,%s)', match)
    DB.commit()
    DB.close()

def swissPairings():
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
    DB = connect()
    c = DB.cursor()

    q = 'SELECT id,name,COUNT(winner) ' \
    'as total ' \
    'FROM players ' \
    'LEFT JOIN matches ' \
    'on matches.winner = players.id ' \
    'GROUP BY id ' \
    'ORDER BY total'

    c.execute(q)
    players = c.fetchall()
    DB.close()
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
