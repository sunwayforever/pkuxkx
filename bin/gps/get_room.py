#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import open_database
from ..tintin import Tintin
from ..util import logger

def get_room(conn, desc):
    sql = "select distinct(zone) from mud_room";
    rows = conn.execute(sql).fetchall()
    zone=""
    actual_zone=""
    for row in rows:
        current_zone=os.path.commonprefix([row[0],desc])
        if len(current_zone) > len(zone):
            zone = current_zone
            actual_zone=row[0]
    actual_room = desc[len(zone):]
    
    sql = "select roomno from mud_room where roomname like '%%%s%%' and zone = '%s'" % (actual_room, actual_zone)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]
    else:
        sql = "select distinct(dst_room_zone) from room_and_entrance where src_room_zone = '%s' and direction not glob '*[^A-z]*'" % (actual_zone)
        zones = ",".join(["'%s'" % (row[0]) for row in conn.execute(sql).fetchall()])

        sql = "select roomno from mud_room where roomname like '%%%s%%' and zone in (%s)" % (actual_room, zones)
        row = conn.execute(sql).fetchone();
        if row:
            return row[0]
        else:
            return -1

if __name__ == "__main__":
    conn = open_database()
    roomno = get_room(conn, sys.argv[1])

    tt = Tintin()
    tt.write ("#var gps.roomno %d;" % (roomno))

