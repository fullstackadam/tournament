#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

from db import DB

def delete_matches():
    """Remove all the match records from the database."""

    DB().execute('DELETE FROM "matches"',True)

def delete_players():
    """
    Remove all the player records from the database
    
    Returns a count of the players deleted
    """

    conn = DB().execute('DELETE FROM "players"')
    conn["conn"].commit()
    total = conn["cursor"].rowcount
    conn["cursor"].close()
    return total

def count_players():
    """Returns the number of players currently registered."""

    cursor = DB().execute('SELECT COUNT(*) FROM "players"')["cursor"]
    total = cursor.fetchone()[0]
    cursor.close()
    return total

def register_player(name):
    """Adds a player to the tournament database.

    Args:
      name: the player's full name (need not be unique).
    """

    player = (name, )
    query = 'INSERT INTO "players" ("name") VALUES (%s)'
    db = DB()
    db.cursor().execute(query,player)
    db.conn.commit()
    db.cursor().close()
    

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
    query = 'SELECT * FROM "player_standings"'
    cursor = DB().execute(query)["cursor"]
    standings = cursor.fetchall()
    cursor.close()
    return standings

def report_match(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match = (winner, loser, )
    query = 'INSERT INTO "matches" ("winner","loser") VALUES (%s,%s)'
    db = DB()
    db.cursor().execute(query,match)
    db.conn.commit()
    db.cursor().close()


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

    query = 'SELECT * FROM "swiss_pairings"';
    cursor = DB().execute(query)["cursor"]
    pairings = cursor.fetchall()
    cursor.close()

    return pairings
