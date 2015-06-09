#!/usr/bin/env python3
import sqlite3
import os
import sys
from .common import open_database
from .insert_room import insert_room

def update_room (conn, roomno, zone, room, desc, exits):
    if roomno != 0:
        sql = "insert or replace into mud_room values (%d, '%s', '%s', '%s', '%s', NULL, NULL)" % (roomno, room, desc, exits, zone)
        conn.execute(sql)
        conn.commit()
    else:
        sql = "select roomno from mud_room where roomname = '%s' and exits = '%s' and zone = '%s'" % (room, exits, zone)
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        if len(rows) == 1:
            return update_room(conn, rows[0][0], zone, room, desc, exits)
        elif len(rows) == 0:
            return insert_room(conn, room, desc, exits, zone)

if __name__ == "__main__":
    conn = open_database()
    update_room (conn, int(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    conn.close()


