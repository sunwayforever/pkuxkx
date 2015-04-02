#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sqlite3
import os
import sys
import traceback

from .common import open_database
from .get_path import shortest_path_no_weight
from ..tintin import Tintin
from ..util import logger

def traverse(conn, roomno, location = None):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno

    if location is not None:
        sql = "select distinct(dst_room_zone) from room_and_entrance where src_room_zone = \
        (select zone from mud_room where roomno = %d) and direction not glob '*[^A-z]*'" % (roomno)

        zones = ",".join(["'%s'" % (row[0]) for row in conn.execute(sql).fetchall()])
    
    while len(stack) != 0:
        (dst_room_no,dst_room_name) = stack.pop()

        if location is None or dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(shortest_path_no_weight(conn, last_room_no, dst_room_no))

            last_room_no = dst_room_no
        
        visited.add(dst_room_no)

        if location is not None:
            sql = "select dst_room_no, dst_room_name from room_and_entrance where src_room_no = %d and dst_room_zone in (%s) \
            and direction not glob '*[^A-z]*'" % (dst_room_no, zones)
        else:
            sql = "select dst_room_no, dst_room_name from room_and_entrance where src_room_no = %d and src_room_zone = dst_room_zone \
            and direction not glob '*[^A-z]*'" % (dst_room_no)

        for row in conn.execute(sql).fetchall():
            if row[0] not in visited:
                stack.append((row[0],row[1]))

    traverse_path.extend(shortest_path_no_weight(conn, last_room_no, roomno))
    return traverse_path
    
if __name__ == "__main__":
    conn = open_database()

    if len(sys.argv) == 3:
        traverse_path = traverse(conn, int(sys.argv[1]), sys.argv[2])
    else:
        traverse_path = traverse(conn, int(sys.argv[1]))
        
    tt = Tintin()
    tt.write("#list {gps_path} create {%s}" % (";".join(traverse_path)))
