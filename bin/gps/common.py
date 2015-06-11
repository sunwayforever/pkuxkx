#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sqlite3
from ..common import open_gps_database

def open_database():
    return open_gps_database()
    
def fixup_area(desc):
    if re.match("^(长江|黄河)[^南北]",desc):
        desc =  desc[:2]+"南岸"+desc[2:]
    elif re.match("^建康府.城",desc):
        desc = desc[:4]+desc[5:]
    elif re.match("^白驼山",desc):
        desc = desc[:2]+desc[3:]
    elif re.match("^小山村",desc):
        desc = "华山村"+desc[3:]
    elif re.match("^华山",desc):
        desc = "华山派"+desc[2:]
    elif re.match("^姑苏慕容",desc):
        desc = desc[2:]
    elif re.match("^福州",desc):
        desc = "闽南"+desc[2:]
    elif re.match("^杭州",desc):
        desc = "临安"+desc[2:]
    elif re.match("^大理城中",desc):
        desc = "大理城"+desc[4:]
    elif re.match("^峨嵋",desc):
        if not re.match("^峨嵋后山",desc):
            desc = "峨嵋派"+desc[2:]
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
