#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import open_database

if __name__ == "__main__":
    conn = open_database()
    conn.execute("delete from mud_room_2")
    sql = "select * from mud_room"
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        desc = row[3].replace(" ","")
        tmp = desc.find("你可以看看")
        if tmp != -1:
            desc = desc[:tmp]
        sql = "insert into mud_room_2 values (%d, '%s', '%s', '%s', '%s', '%s', '%s','')" % (row[0],row[1], row[2], desc, row[4],row[5],row[6]);
        conn.execute(sql)
    cursor.close()
    conn.commit()
    conn.close()
    
