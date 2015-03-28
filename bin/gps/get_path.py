#!/usr/bin/env python3
import sqlite3
import os
import sys
import traceback

from .common import open_database
from ..tintin import Tintin
from ..util import logger

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
    logger.info ("%s -> %s" %(src,dst))
    if (src == dst):
        return []

    src_set = set([src])
    dst_set = set([dst])

    while True:
        updated = False
        sql = "update mud_entrance_weight set weight = weight - 1 where weight > 0 and roomno in (%s)" % (",".join([str(i) for i in src_set]))
        cursor = conn.execute(sql)
        if cursor.rowcount > 0:
            updated = True

        sql = "select A.linkroomno, A.roomno from mud_entrance as A left join mud_entrance_weight as B on A.roomno = B.roomno and A.linkroomno = B.linkroomno \
        where A.roomno in (%s) and ifnull(B.weight,0) = 0" % (",".join([str(i) for i in src_set]))

        rows = conn.execute(sql).fetchall()
        orig_src_set = src_set
        if rows:
            src_set = src_set.union(set([r[0] for r in rows]))
        
        if (not updated and len(src_set.difference(orig_src_set)) != 0):
            updated = True

        sql = "update mud_entrance_weight set weight = weight - 1 where weight > 0 and linkroomno in (%s)" % (",".join([str(i) for i in dst_set]))
        cursor = conn.execute(sql)
        if not updated and cursor.rowcount > 0:
            updated = True

        sql = "select A.roomno, A.linkroomno from mud_entrance as A left join mud_entrance_weight as B on A.roomno = B.roomno and A.linkroomno = B.linkroomno \
        where A.linkroomno in (%s) and ifnull(B.weight,0) = 0" % (",".join([str(i) for i in dst_set]))

        rows = conn.execute(sql).fetchall()
        orig_dst_set = dst_set
        if rows:
            dst_set = dst_set.union(set([r[0] for r in rows]))
        
        if (not updated and len(dst_set.difference(orig_dst_set)) != 0):
            updated = True

        if not updated:
            # not connected
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
    logger.debug("get_path: %s -> %s, weight: %s" % (from_room, to_room, weight))
    if not to_room.isdigit():
        tmp = to_room.split("@")
        if (len(tmp) == 2):
            sql = "select roomno from mud_room where roomname = '%s' and zone like '%%%s%%'" % (tmp[0], tmp[1])
        else:
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
    if (dst_room == -1):
        tt.write ("#list gps_path create {};\n")
    elif (int(from_room) == dst_room):
        tt.write ("#list gps_path create {#cr};\n")
    else:
        paths = shortest_path(conn,int(from_room),dst_room)
        tt.write ("#list gps_path create {%s};\n" % (";".join(paths)))

if __name__ == "__main__":
    conn = open_database()
    get_path(conn, sys.argv[1], sys.argv[2], sys.argv[3])
