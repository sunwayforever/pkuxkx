#!/usr/bin/env python3
import sqlite3
import os
import sys

from .common import *
from ..common import Tintin
from ..common import logger

def get_area(conn, desc):
    desc = fixup_area(desc)
    sql = "select distinct(zone) from mud_room";
    rows = conn.execute(sql).fetchall()
    for row in rows:
        if desc.startswith (row[0]):
            return row[0]

if __name__ == "__main__":
    conn = open_database()
    area = get_area(conn, sys.argv[1])

    tt = Tintin()
    tt.write ("#var gps.area %s;" % (area))

