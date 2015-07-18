#!/usr/bin/env python3
import sqlite3
import os
import sys
import re

from .common import *
from ..common import Tintin
from ..common import logger

room_alias = {
    "襄阳官道":498,
    "古墓墓道":1036,
    "丐帮暗道":1484,
    "扬州暗道":1484,
    "杀手帮消魂屋":400,
    "华山寝室":1107,
    "无量山书房":3478,
}
def get_room(conn, desc):
    if desc in room_alias:
        return room_alias[desc]
    room = fixup_room(desc)
    # gt yz
    # gt 醉仙楼
    sql = "select roomno from mud_room where abbr = '%s' or roomname = '%s'" % (room, room)
    row = conn.execute(sql).fetchone()
    if row:
        return row[0]

    desc = fixup_area(desc)
    # gt 扬州醉仙楼
    sql = "select distinct(zone) from mud_room"
    rows = conn.execute(sql).fetchall()
    actual_zone=""
    for row in rows:
        if desc.startswith (row[0]):
            current_zone=row[0]
            if len(current_zone) > len(actual_zone):
                actual_zone = current_zone
    actual_room = desc[len(actual_zone):]
    actual_room = fixup_room(actual_room)

    sql = "select roomno from mud_room where roomname = '%s' and zone = '%s'" % (actual_room, actual_zone)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]

    sql = "select roomno from mud_room where roomname = '%s'" % (actual_room)
    rows = conn.execute(sql).fetchall();
    if len(rows) == 1:
        return rows[0][0]
    
    sql = "select roomno from mud_room where roomname like '%%%s%%' and zone = '%s'" % (actual_room, actual_zone)
    row = conn.execute(sql).fetchone();
    if row:
        return row[0]
    
    # sql = "select distinct(dst_room_zone) from room_and_entrance where src_room_zone = '%s' and is_boundary = 0" % (actual_zone)
    # zones = ",".join(["'%s'" % (row[0]) for row in conn.execute(sql).fetchall()])

    # sql = "select roomno from mud_room where roomname = '%s' and zone in (%s)" % (actual_room, zones)
    # row = conn.execute(sql).fetchone();
    # if row:
    #     return row[0]

    # sql = "select roomno from mud_room where roomname like '%%%s%%' and zone in (%s)" % (actual_room, zones)
    # row = conn.execute(sql).fetchone();
    # if row:
    #     return row[0]
    
    return -1

if __name__ == "__main__":
    conn = open_database()
    roomno = get_room(conn, sys.argv[1])

    tt = Tintin()
    tt.write ("#var gps.roomno %d;" % (roomno))

