#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import open_database

def insert_link(conn, src_room_no, dst_room_no, direction, reversed_direction):
    if direction != "":
        sql = "insert or replace into mud_entrance values (%d, %d, '%s', NULL)" % (src_room_no, dst_room_no, direction)
        conn.execute(sql)
    if reversed_direction != "":
        sql = "insert or replace into mud_entrance values (%d, %d, '%s', NULL)" % (dst_room_no, src_room_no, reversed_direction)
        conn.execute(sql)
    conn.commit()

if __name__ == "__main__":
    conn = open_database()
    insert_link(conn, int(sys.argv[1]), int(sys.argv[2]), sys.argv[3], sys.argv[4])
    conn.close()
