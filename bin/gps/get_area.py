#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import *
from ..tintin import Tintin
from ..util import logger

def get_area(conn, desc):
    desc = fixup_area(desc)
    sql = "select distinct(zone) from mud_room";
    rows = conn.execute(sql).fetchall()
    zone=""
    actual_zone=""
    for row in rows:
        current_zone=os.path.commonprefix([row[0],desc])
        if len(current_zone) > len(zone):
            zone = current_zone
            actual_zone=row[0]
    return actual_zone;

if __name__ == "__main__":
    conn = open_database()
    area = get_area(conn, sys.argv[1])

    tt = Tintin()
    tt.write ("#var gps.area %s;" % (area))

