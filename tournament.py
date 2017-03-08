#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM matches")
    db.commit()

    # set all players num_matches to 0
    c.execute("UPDATE players SET num_matches = 0 WHERE num_matches != 0;")
    db.commit()

    db.close()


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("DELETE FROM players")
    db.commit()
    db.close()


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("SELECT count(*) FROM players")
    for row in c.fetchall():
        tt = row[0]
    db.close()
    return tt


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    player = bleach.clean(name)
    player = bleach.linkify(player)
    c.execute("INSERT INTO players (name) VALUES (%s)", (player,))
    db.commit()
    db.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a
    player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    c.execute("""select players.name, players.ID, foo.numw,
        players.num_matches
        FROM (select players.ID,
        count(matches.winner) as numW
        from players left join matches on players.ID = matches.winner
        group by players.ID order by numW) as foo
        join players on players.ID = foo.id;""")
    # for row in c.fetchall():
    #     m = row[2] + row[3]
    #     t = ({'id': str(row[1]), 'name': str(row[0]), 'wins': row[2],
    #           'matches': m})
    t = ()
    o = list(t)
    for row in c.fetchall():
        j = (str(row[1]), str(row[0]), row[2], row[3])
        o.append(j)

    t2 = tuple(o)

    # posts = ({'id': str(row[1]), 'name': str(row[0]), 'wins': row[2],
    #           'matches': row[3]}
             
    db.close()
    return t2


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    sql = "INSERT INTO matches (winner, loser) VALUES (%s, %s);"
    data = (winner, loser)
    c.execute(sql, data)
    db.commit()

    newm = 0
    # find out number of matches for winner ID
    # sql = "SELECT num_matches from players where id = %s;"
    #        SELECT num_matches from players where id = 129;
    # c.execute(sql, winner)
    # c.execute("SELECT num_matches from players where id = %s;"), (winner, )
    c.execute("SELECT num_matches from players where id=%s;", (winner,))
    for row in c.fetchall():
        newm = int(row[0]) + 1
    # increment the number
    sql = "UPDATE players SET num_matches = %s WHERE id = %s;"
    data = (newm, winner)
    c.execute(sql, data)
    db.commit()

    # find out number of matches for loser ID
    c.execute("SELECT num_matches from players where id=%s;", (loser,))
    # increment the number
    for row in c.fetchall():
        newm = row[0] + 1
    sql = "UPDATE players SET num_matches = %s WHERE id = %s;"
    data = (newm, loser)
    c.execute(sql, data)
    db.commit()

    db.close()


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
    db = connect()
    c = db.cursor()
    c.execute("""select players.name, players.ID, foo.numw,
        players.num_matches
        FROM (select players.ID,
        count(matches.winner) as numW
        from players left join matches on players.ID = matches.winner
        group by players.ID order by numW) as foo 
        join players on players.ID = foo.id order by numw desc;""")

    t = ()  # empty tuple
    o = list(t)  # master list
    w = []  # empty list
    for row in c.fetchall():
        w.append(str(row[1]))
        w.append(str(row[0]))
        if len(w) % 4 == 0:
            o.append(w)
            w = []
    t = tuple(o)

    db.close()
    return t
