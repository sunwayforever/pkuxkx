#!/usr/bin/env python3
import sqlite3
import os
import sys

if __name__ == "__main__":
    conn = sqlite3.connect("db/rooms.db")
    tmpfile = open("/tmp/gps.tin", "w")
    tmpfile.write ("#echo {[1;31m---------------------------------------[2;37;0m}\n")
    
    sql = "select src_room_name, src_room_zone from room_and_entrance where src_room_no = %d limit 1" %(int(sys.argv[1]))
    cursor = conn.execute(sql)
    row = cursor.fetchone()
    zone = row[1]
    tmpfile.write("#echo {%s @ %s:}\n" % (row[0], row[1]))
    tmpfile.write ("#echo {[1;31m---------------------------------------[2;37;0m}\n")
    sql = "select dst_room_zone, dst_room_name, dst_room_no, direction from room_and_entrance where src_room_no = %d" %(int(sys.argv[1]))
    cursor = conn.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == zone:
            tmpfile.write ("#echo {(%d): %s: {%s}}\n" % (row[2], row[1], row[3]))
        else:
            tmpfile.write ("#echo {(%d): %s @ %s : {%s}}\n" % (row[2], row[0], row[1], row[3]))
    tmpfile.write ("#echo {[1;31m---------------------------------------[2;37;0m}\n")
    tmpfile.close();
