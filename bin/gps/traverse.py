#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sqlite3
import os
import sys
import traceback

from .common import open_database
from .get_path import get_path
from ..tintin import Tintin
from ..util import logger

def traverse_bfs(conn, roomno):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno
    bfs_max_count = 8
    while len(stack) != 0:
        bfs_max_count = bfs_max_count-1
        if bfs_max_count<0:
            break
        
        (dst_room_no,dst_room_name) = stack.pop(0)

        if last_room_no != dst_room_no:
            traverse_path.extend(get_path(conn, last_room_no, dst_room_no,"1,-1,1,-1,-1,1,1"))
            last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        sql = "select dst_room_no, dst_room_name from room_and_entrance where src_room_no = %d and type not in (2,4,5)" % (dst_room_no)

        for row in conn.execute(sql).fetchall():
            if row[0] not in visited:
                stack.append((row[0],row[1]))

    traverse_path.extend(get_path(conn, last_room_no, roomno,"1,-1,1,-1,-1,1,1"))
    return traverse_path

def traverse_dfs(conn, roomno):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno
        
    while len(stack) != 0:
        (dst_room_no,dst_room_name) = stack.pop()

        if last_room_no != dst_room_no:
            traverse_path.extend(get_path(conn, last_room_no, dst_room_no,"1,-1,1,-1,-1,1,1"))
            last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        sql = "select dst_room_no, dst_room_name from room_and_entrance where src_room_no = %d and src_room_zone = dst_room_zone \
        and type not in (2,4,5)" % (dst_room_no)

        for row in conn.execute(sql).fetchall():
            if row[0] not in visited:
                stack.append((row[0],row[1]))

    traverse_path.extend(get_path(conn, last_room_no, roomno,"1,-1,1,-1,-1,1,1"))
    return traverse_path


def traverse_location(conn, roomno, location):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno

    sql = "select distinct(dst_room_zone) from room_and_entrance where src_room_zone = \
    (select zone from mud_room where roomno = %d) and type not in (2,4,5)" % (roomno)

    zones = ",".join(["'%s'" % (row[0]) for row in conn.execute(sql).fetchall()])
        
    while len(stack) != 0:
        (dst_room_no,dst_room_name) = stack.pop()

        if dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(get_path(conn, last_room_no, dst_room_no,"1,-1,1,-1,-1,1,1"))
            last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        sql = "select dst_room_no, dst_room_name from room_and_entrance where src_room_no = %d and dst_room_zone in (%s) \
        and type not in (2,4,5)" % (dst_room_no, zones)

        for row in conn.execute(sql).fetchall():
            if row[0] not in visited:
                stack.append((row[0],row[1]))

    traverse_path.extend(get_path(conn, last_room_no, roomno,"1,-1,1,-1,-1,1,1"))
    return traverse_path
    
if __name__ == "__main__":
    conn = open_database()

    if len(sys.argv) == 3:
        traverse_path = traverse_location(conn, int(sys.argv[1]), sys.argv[2])
    else:
        traverse_path = traverse_bfs(conn, int(sys.argv[1]))
        traverse_path.extend(traverse_dfs(conn,int(sys.argv[1])))
        
    tt = Tintin()
    tt.write("#list {gps_path} create {%s}" % (";".join(traverse_path)))
