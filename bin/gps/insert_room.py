#!/usr/bin/env python3
import sqlite3
import os
import sys
from .common import open_database

def insert_room (conn, room, desc, exits, zone):
    sql = "insert into mud_room values (NULL, '%s', '%s', '%s', '%s', NULL, NULL)" % (room, desc, exits, zone)
    conn.execute(sql)
    conn.commit()

if __name__ == "__main__":
    conn = open_database()
    insert_room (conn, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    conn.close()


