#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
from ..common import open_gps_database

def open_database():
    return open_gps_database()

area_alias = {
    "白驼山":"白驼","小山村":"华山村","福州":"闽南","杭州提督府":"临安提督府","杭州":"临安府","大理城中":"大理城",
    "西湖梅庄":"梅庄","西湖":"临安府西湖","桃源":"桃源县","全真":"全真教","苏州":"苏州城","扬州":"扬州城",
    "晋阳":"晋阳城","镇江":"镇江府","北京":"北京城","姑苏慕容":"慕容","建康府南城":"建康府南",
    "建康府北城":"建康府北","长江南岸":"长江南岸","长江北岸":"长江北岸","长江":"长江南岸",
    "黄河南岸":"黄河南岸","黄河北岸":"黄河北岸","黄河":"黄河南岸","峨嵋后山":"峨嵋后山",
    "峨嵋":"峨嵋派","洛阳":"洛阳城",
}

def fixup_area(desc):
    for (k,v) in area_alias.items():
        if re.match("^%s"%(k),desc):
            desc = "%s%s"%(v,desc[len(k)])
            break
    return desc

def fixup_room(room):
    if re.match(".*泥人.*",room):
        room = "泥人铺"
    elif re.match(".*甜蜜小屋.*",room):
        room = "甜蜜小屋"
    return room

def get_zone(conn, room):
    sql = "select zone from mud_room where roomno = %d" % (room)
    row = conn.execute(sql).fetchone()
    if row:
        return row[0]
    else:
        return "nil"
