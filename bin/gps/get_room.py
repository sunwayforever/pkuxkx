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
    "扬州城暗道":1484,
    "杀手帮消魂屋":400,
    "华山寝室":1107,
    "无量山书房":3478,
    "华山村小棚子":1067,
    "慕容小路":2665,
    "中原大驿道":718,
    "桃花岛小木屋":2618,
    "曲阜大驿道":661,
    "峨嵋派洞穴":1731,
    "泉州杂货铺":2120,
    "灵州车马店二楼":1366,
    "建康府北长江渡口":2580,
    "归云庄马房":2350,
    "闽南密道":2157,
    "闽南密室":2157,
    "闽南密室房梁":2157,
    "成都川西土路":1528,
    "南昌山路":2061,
    "襄阳民宅":458,
    "苏州城客店二楼":2287,
    "昆明客店内室":1948,
    "全真教浴堂":1143,
    "白驼武器库":3002,
    "张家口天字号房":2887,
    "张家口地字号房":2887,
    "江州客店内室":2064,
    "中原客店二楼":714,
    "南昌客店内室":2082,
    "镇江府客店内室":2424,
    "洛阳城大官道":817,
    "丝绸之路莫高窟":2778,
}

def get_room(conn, desc):
    room = fixup_room(desc)
    # gt yz
    # gt 醉仙楼
    sql = "select roomno from mud_room where abbr = '%s' or roomname = '%s'" % (room, room)
    row = conn.execute(sql).fetchone()
    if row:
        return row[0]

    desc = fixup_area(desc)
    if desc in room_alias:
        return room_alias[desc]

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

