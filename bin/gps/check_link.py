#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import open_database
from ..tintin import Tintin

if __name__ == "__main__":
    tt = Tintin()
    tt.write ("#delay {1} {\n");
    tt.write ("#echo {[1;31m---------------------------------------[2;37;0m};\n")
    
    conn = open_database()
    sql = "select src_room_name, src_room_zone from room_and_entrance where src_room_no = %d limit 1" %(int(sys.argv[1]))
    cursor = conn.execute(sql)
    row = cursor.fetchone()
    if not row:
        tt.write("#echo {no link};")
        tt.write("#echo {[1;31m---------------------------------------[2;37;0m};\n")
        tt.write ("};");
        exit(0)
    zone = row[1]
    tt.write("#echo {(%d) %s @ %s:};\n" % (int(sys.argv[1]),row[0], row[1]))
    tt.write ("#echo {[1;31m---------------------------------------[2;37;0m};\n")
    sql = "select dst_room_zone, dst_room_name, dst_room_no, direction from room_and_entrance where src_room_no = %d" %(int(sys.argv[1]))
    cursor = conn.execute(sql)
    rows = cursor.fetchall()

    for row in rows:
        if row[0] == zone:
            tt.write ("#echo {(%d): %s: {%s}};\n" % (row[2], row[1], row[3]))
        else:
            tt.write ("#echo {(%d): %s @ %s : {%s}};\n" % (row[2], row[0], row[1], row[3]))
    tt.write ("#echo {[1;31m---------------------------------------[2;37;0m};\n")
    tt.write ("};");
