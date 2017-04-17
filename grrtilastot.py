# -*- coding: UTF-8 -*-
import psycopg2
from pprint import pprint
from random import randint
from time import strftime
from datetime import datetime, timedelta


def helppi():
    help_text = "Katso tilastot '/kirjaa tilastot'.\n" + \
                "Käytä '/kirjaa koko', jossa koko on listassa [rpieni, pieni, iso].\n" + \
                "(rpieni = 0.25l; pieni = 0.33l; iso = 0.5l).\n" + \
                "Käytä '/kirjaa poistatiedot', jos haluat poistaa merkintäsi."
    return help_text


def beer_records(commands, msg):

    sender_id = msg["from"]["id"]
    chat_id = msg["chat"]["id"]

    beer_sizes = {"rpieni": 0.25, "pieni": 0.33, "iso": 0.5}

    if msg["chat"]["type"] == "private":
        if commands[0] in ["tilasto", "tilastot"]:
            return sender_id, print_stats("private", chat_id)
        elif commands[0] in beer_sizes.keys():
            record_beer(sender_id, msg["from"]["first_name"], beer_sizes[commands[0]])
            return sender_id, "Olut kirjattu!"
        elif commands[0] == "poistatiedot":
            remove_my_data(sender_id)
            return sender_id, "Tietosi ovat poistettu kannasta."

    elif msg["chat"]["type"] == "group":
        if commands[0] in ["tilasto", "tilastot"]:
            return chat_id, print_stats("group", chat_id)

    return sender_id, helppi()


def record_beer(user_id, username, litres):
    """Records beer to the Grr<3 drinking records.
    """

    connection, cursor = open_db_con()

    try:
        # Run SELECT for user_id
        cursor.execute("SELECT * FROM GRRTABLE WHERE grrid = %s", (user_id,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            # Create new drinker in database with their Telegram id as grrid.
            # INSERT INTO GRRTABLE Values (user_id,username,1,litres);
            cursor.execute("INSERT INTO GRRTABLE VALUES (%s,%s,%s,%s)", (user_id, username, 1, litres,))
        else:
            # Add new beer for user_id.
            # UPDATE GRRTABLE SET litres = litres + 0.33, beers = beers +1 where grrid = '123';
            cursor.execute("UPDATE GRRTABLE SET litres = litres + %s, beers = beers + 1 WHERE grrid = %s", (litres, user_id))
        print(rows)
    except Exception as e:
        print("Uh oh, something wrong with statements.")
        print(e)

    connection.commit()
    cursor.close()
    connection.close()


def remove_my_data(user_id):
    """Removes user data from table of the given user_id.
    """
    connection, cursor = open_db_con()

    try:
        cursor.execute("DELETE FROM GRRTABLE WHERE grrid = %s", (user_id,))
    except Exception as e:
        print("Uh oh, something wrong with statements.")
        print(e)

    connection.commit()
    cursor.close()
    connection.close()


def print_stats(chat_type, chat_id):
    """Returns statistics.
    Returns ONLY group stats when queried in group.
    Returns both group and private stats when queried in private.
    """

    connection, cursor = open_db_con()
    beers = 0
    litres = 0
    stats = "Kantahaku ei onnistunut"
    personal = ""

    try:
        cursor.execute("SELECT * FROM GRRTABLE")
        rows = cursor.fetchall()
        # pprint(rows)

        for row in rows:
            if row[0] == chat_id:
                personal = row
            beers = beers + row[2]
            litres = litres + row[3]

        stats = "Grr<3:n tilastoissa on {} juomaria. He ovat juoneet yhteensä {} olutta ({} litraa).".format(len(rows), beers, litres)
        if chat_type == "private":
            if len(personal) > 1:
                stats = stats + "\nOlet kirjannut Grr<3:n tilastoihin yhteensä {} olutta ({} litraa).".format(personal[2], personal[3])
            else:
                stats = stats + "\nSinulla ei ole merkintöjä kannassa."

    except Exception as e:
        print("Uh oh, something wrong with statements.")
        print(e)

    cursor.close()
    connection.close()
    return stats


def open_db_con():
    try:
        connect_str = "connection string"
        # use our connection values to establish a connection
        conn = psycopg2.connect(connect_str)
        # create a psycopg2 cursor that can execute queries
        cursor = conn.cursor()
    except Exception as e:
        print("Uh oh, can't connect. Invalid db name, user or password?")
        print(e)
    return conn, cursor
