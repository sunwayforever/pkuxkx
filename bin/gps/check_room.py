#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import open_database
from ..tintin import Tintin
from ..util import logger

def check_room (conn, zone, room, desc, exits):
    sql = "select roomno from mud_room where roomname = '%s'" % (room)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]
    
    sql = "select roomno from mud_room where roomname = '%s' and description = '%s'" % (room, desc)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]
    
    sql = "select roomno from mud_room where roomname = '%s' and description = '%s' and exits = '%s'" % (room, desc, exits)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]
    
    sql = "select roomno from mud_room where zone = '%s' and roomname = '%s' and description = '%s' and exits = '%s'" % (zone, room, desc, exits)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]

    return -1;

if __name__ == "__main__":
    conn = open_database()
    roomno = check_room (conn, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

    tt = Tintin()
    tt.write ("#var gps.roomno %d;" % (roomno))

