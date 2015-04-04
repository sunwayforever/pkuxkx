#!/usr/bin/env python3
import sqlite3
import os
import sys
import re

from .common import *
from ..tintin import Tintin
from ..util import logger

def get_room(conn, desc):
    desc = fixup_area(desc)
    # gt yz
    # gt 醉仙楼
    sql = "select roomno from mud_room where abbr = '%s' or roomname = '%s'" % (desc, desc)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]

    # gt 扬州醉仙楼
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

    sql = "select roomno from mud_room where roomname = '%s' and zone = '%s'" % (actual_room, actual_zone)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]
    
    sql = "select roomno from mud_room where roomname like '%%%s%%' and zone = '%s'" % (actual_room, actual_zone)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]
    
    sql = "select distinct(dst_room_zone) from room_and_entrance where src_room_zone = '%s' and type not in (2,4,5)" % (actual_zone)
    zones = ",".join(["'%s'" % (row[0]) for row in conn.execute(sql).fetchall()])

    sql = "select roomno from mud_room where roomname = '%s' and zone in (%s)" % (actual_room, zones)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]

    sql = "select roomno from mud_room where roomname like '%%%s%%' and zone in (%s)" % (actual_room, zones)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]
    
    return -1

if __name__ == "__main__":
    conn = open_database()
    roomno = get_room(conn, sys.argv[1])

    tt = Tintin()
    tt.write ("#var gps.roomno %d;" % (roomno))

