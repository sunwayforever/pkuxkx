#!/usr/bin/env python3
import sqlite3
import os
import sys

def insert_room (conn, zone, room, desc, exits):
    sql = "insert into mud_room values (NULL, NULL, %s, %s, %s, NULL, %s, NULL, NULL)" % (room, desc, exits, zone)
    conn.execute(sql)

if __name__ == "__main__":
    conn = sqlite3.connect("db/rooms.db")
    insert_room (conn, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])


