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
def get_neighbors(mud, roomno):
    stack = [roomno,-1]
    visited = set()
    bfs_max_count = 8

    while len(stack) != 0:
        if bfs_max_count<0:
            break
        dst_room_no = stack.pop(0)
        if dst_room_no == -1:
            stack.append(-1)
            bfs_max_count = bfs_max_count-1
            continue
        visited.add(dst_room_no)
        for link in mud.neighbours[dst_room_no]:
            if link.is_boundary == 0 and link.linkroomno not in visited:
                stack.append(link.linkroomno)
            
    return visited

def traverse_bfs(mud, roomno, location):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno
    if location == "nil":
        bfs_max_count = 10
    else:
        bfs_max_count = 50
        
    while len(stack) != 0:
        bfs_max_count = bfs_max_count-1
        if bfs_max_count<0:
            break
        
        (dst_room_no,dst_room_name) = stack.pop(0)

        if location == "nil" or dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(mud.get_path(last_room_no, dst_room_no))
                last_room_no = dst_room_no
            
        visited.add(dst_room_no)

        for link in mud.neighbours[dst_room_no]:
            if link.is_boundary == 0 and link.linkroomno not in visited:
                stack.append((link.linkroomno,link.linkroomname))

    traverse_path.extend(mud.get_path(last_room_no, roomno))
    return traverse_path

def traverse_dfs(mud, roomno, location, candidate=None):
    traverse_path = []
    stack = [(roomno,"NULL")]
    visited = set()
    last_room_no = roomno
    while len(stack) != 0:
        (dst_room_no,dst_room_name) = stack.pop()

        if location == "nil" or dst_room_name == location:
            if last_room_no != dst_room_no:
                traverse_path.extend(mud.get_path(last_room_no, dst_room_no))
                last_room_no = dst_room_no
            
        visited.add(dst_room_no)
        
        for link in mud.neighbours[dst_room_no]:
            if link.is_boundary == 1 or link.linkroomno in visited:
                continue
            
            if candidate is not None:
                if link.linkroomno in candidate:
                    stack.append((link.linkroomno,link.linkroomname))
            else:
                if link.src_room_zone == link.dst_room_zone:
                    stack.append((link.linkroomno,link.linkroomname))    

    traverse_path.extend(mud.get_path(last_room_no, roomno))
    return traverse_path
    
if __name__ == "__main__":
    conn = open_database()
    roomno = int(sys.argv[1])
    location = sys.argv[2]
    mode = sys.argv[3]

    mud = MudRoom(conn, TRAVERSE_WEIGHT)
    if mode == "bfs":
        traverse_path = traverse_bfs(mud, roomno, location)
    elif mode == "dfs":
        candidate = get_neighbors(mud,roomno)
        traverse_path = traverse_dfs(mud, roomno, location, candidate)
    else:
        traverse_path = traverse_bfs(mud, roomno, location)
        traverse_path.extend(traverse_dfs(mud, roomno, location))
        
    tt = Tintin()
    tt.write("#list {gps_path} create {%s}" % (";".join(traverse_path)))
