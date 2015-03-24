#!/usr/bin/env python3
import sqlite3
import os
import sys
from ..tintin import Tintin

def detect_room (conn, zone, room, desc, exits):
    sql = "select roomno from mud_room where roomname = '%s' and description = '%s' and exits = '%s'" % (room, desc, exits)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]
    sql = "select roomno from mud_room where zone = '%s' and roomname = '%s' and description = '%s' and exits = '%s'" % (zone, room, desc, exits)
    row = conn.execute(sql).fetchone()
    if not row:
        return -1;
    return row[0];

if __name__ == "__main__":
    conn = sqlite3.connect("db/rooms.db")
    roomno = detect_room (conn, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    tt = Tintin()
    tt.write ("#var gps.roomno %d;" % (roomno))

