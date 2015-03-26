#!/usr/bin/env python3
import sqlite3
import os
import sys
import traceback

from .common import open_database
from ..tintin import Tintin


def shortest_path_no_weight(conn, src, dst):
    if (src == dst):
        return []

    src_set = set([src])
    dst_set = set([dst])

    while True:
        sql = "select linkroomno, roomno from mud_entrance as A where A.roomno in (%s)"  % (",".join([str(i) for i in src_set]))

        rows = conn.execute(sql).fetchall()
        if rows:
            src_set = src_set.union(set([r[0] for r in rows]))
        else:
            return []

        sql = "select roomno, linkroomno from mud_entrance as A where A.linkroomno in (%s)"  % (",".join([str(i) for i in dst_set]))

        rows = conn.execute(sql).fetchall()
        if rows:
            dst_set = dst_set.union(set([r[0] for r in rows]))
        else:
            return []

        intersection = src_set.intersection(dst_set)
        if (intersection):
            if src in intersection and dst in intersection:
                sql = "select direction from mud_entrance where roomno = %d and linkroomno = %d" %(src, dst)
                row = conn.execute(sql).fetchone()
                return [row[0]]
            else:
                middle = intersection.pop()
                ret = shortest_path_no_weight(conn, src, middle)
                ret.extend(shortest_path_no_weight(conn, middle, dst))
                return ret

def shortest_path(conn, src, dst):
    if (src == dst):
        return []

    src_set = set([src])
    dst_set = set([dst])

    while True:
        sql = "update mud_entrance_weight set weight = weight - 1 where weight != 0 and roomno in (%s)" % (",".join([str(i) for i in src_set]))
        conn.execute(sql)

        sql = "select linkroomno, roomno from mud_entrance as A where A.roomno in (%s) and \
        ifnull((select weight from mud_entrance_weight as w where w.roomno = A.roomno and w.linkroomno = A.linkroomno),0) = 0"  % (",".join([str(i) for i in src_set]))

        rows = conn.execute(sql).fetchall()
        if rows:
            src_set = src_set.union(set([r[0] for r in rows]))
        else:
            return []

        sql = "update mud_entrance_weight set weight = weight - 1 where weight != 0 and linkroomno in (%s)" % (",".join([str(i) for i in dst_set]))
        conn.execute(sql)

        sql = "select roomno, linkroomno from mud_entrance as A where A.linkroomno in (%s) and \
        ifnull((select weight from mud_entrance_weight as w where w.roomno = A.roomno and w.linkroomno = A.linkroomno),0) = 0"  % (",".join([str(i) for i in dst_set]))

        rows = conn.execute(sql).fetchall()
        if rows:
            dst_set = dst_set.union(set([r[0] for r in rows]))
        else:
            return []

        intersection = src_set.intersection(dst_set)
        if (intersection):
            if src in intersection and dst in intersection:
                sql = "select direction from mud_entrance where roomno = %d and linkroomno = %d" %(src, dst)
                row = conn.execute(sql).fetchone()
                return [row[0]]
            else:
                middle = intersection.pop()
                ret = shortest_path(conn, src, middle)
                ret.extend(shortest_path(conn, middle, dst))
                return ret

def get_path(conn, from_room, to_room, weight):
    if not to_room.isdigit():
        sql = "select roomno from mud_room where abbr = '%s' or roomname = '%s'" % (to_room, to_room)
        cursor = conn.execute(sql)
        row = cursor.fetchone()
        if row:
            dst_room = row[0]
        else:
            dst_room = -1
    else:
        dst_room = int(to_room)

    try:
        conn.execute ("drop table mud_entrance_weight")
    except:
        pass
    conn.execute ("create temp table mud_entrance_weight (roomno int, linkroomno int, weight int)")

    # about the path type:
    # 1. gps.clear 2. gps.guohe 3. gps.delay 4. gps.zuoche
    weights = [int(x) for x in weight.split(",")]
    for i,w in enumerate(weights, start=1):
        conn.execute("insert into mud_entrance_weight select roomno, linkroomno, %d from mud_entrance where type = %d" % (w, i))

    tt = Tintin()
    if (int(from_room) == dst_room):
        tt.write ("#list gps_path create {#cr};\n")
    else:
        paths = shortest_path(conn,int(from_room),dst_room)
        tt.write ("#list gps_path create {%s};\n" % (";".join(paths)))

if __name__ == "__main__":
    conn = open_database()
    while True:
        try:
            line = sys.stdin.readline()
            args = line.split(":")
            if len(args) == 3:
                get_path(conn, args[0], args[1], args[2])
        except Exception:
            traceback.print_exc(file=open("/tmp/gpslog","w"))
