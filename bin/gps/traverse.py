#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sqlite3
import os
import sys
import traceback

from .common import open_database
from .get_path import MudRoom
from ..common import Tintin
from ..common import logger

TRAVERSE_WEIGHT = "1,-1,1,-1,-1,1,1,1"
def traverse_bfs(mud, roomno, location=None):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno
    if location == None:
        bfs_max_count = 10
    else:
        bfs_max_count = 100
        
    while len(stack) != 0:
        bfs_max_count = bfs_max_count-1
        if bfs_max_count<0:
            break
        
        (dst_room_no,dst_room_name) = stack.pop(0)

        if location == None or dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(mud.get_path(last_room_no, dst_room_no))
                last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        for link in mud.neighbours[dst_room_no]:
            if link.is_boundary == 0 and link.linkroomno not in visited:
                stack.append((link.linkroomno,link.linkroomname))

    traverse_path.extend(mud.get_path(last_room_no, roomno))
    return traverse_path

def traverse_dfs(mud, roomno, location=None):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno

    while len(stack) != 0:
        (dst_room_no,dst_room_name) = stack.pop()

        if location == None or dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(mud.get_path(last_room_no, dst_room_no))
                last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        for link in mud.neighbours[dst_room_no]:
            if link.is_boundary == 0 and link.src_room_zone == link.dst_room_zone and link.linkroomno not in visited:
                stack.append((link.linkroomno,link.linkroomname))

    traverse_path.extend(mud.get_path(last_room_no, roomno))
    return traverse_path
    
if __name__ == "__main__":
    conn = open_database()
    roomno = int(sys.argv[1])
    if len(sys.argv) == 4:
        location = sys.argv[2]
    else:
        location = None

    mud = MudRoom(conn, TRAVERSE_WEIGHT)
    traverse_path = traverse_bfs(mud, roomno, location)
    traverse_path.extend(traverse_dfs(mud, roomno, location))
        
    tt = Tintin()
    tt.write("#list {gps_path} create {%s}" % (";".join(traverse_path)))
