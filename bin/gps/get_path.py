#!/usr/bin/env python3
import sqlite3
import os
import sys
from ..tintin import Tintin

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
        # sql = "select linkroomno from mud_entrance where roomno in (%s)" % (",".join([str(i) for i in src_set]))
        rows = conn.execute(sql).fetchall()

        if rows:
            src_set = src_set.union(set([r[0] for r in rows]))
        else:
            return []

        sql = "update mud_entrance_weight set weight = weight - 1 where weight != 0 and linkroomno in (%s)" % (",".join([str(i) for i in dst_set]))
        conn.execute(sql)
        sql = "select roomno, linkroomno from mud_entrance as A where A.linkroomno in (%s) and \
        ifnull((select weight from mud_entrance_weight as w where w.roomno = A.roomno and w.linkroomno = A.linkroomno),0) = 0"  % (",".join([str(i) for i in dst_set]))
        # sql = "select roomno from mud_entrance where linkroomno in (%s)" % (",".join([str(i) for i in dst_set]))
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        if rows:
            dst_set = dst_set.union(set([r[0] for r in rows]))
        else:
            return []
        intersection = src_set.intersection(dst_set)
        if (intersection):
            if src in intersection:
                sql = "select direction from mud_entrance where roomno = %d and linkroomno = %d" %(src, dst)
                row = conn.execute(sql).fetchone()
                return [row[0]]
            else:
                middle = intersection.pop()
                ret = shortest_path(conn, src, middle)
                ret.extend(shortest_path(conn, middle, dst))
                return ret
        
if __name__ == "__main__":
    conn = sqlite3.connect("db/rooms.db")
    if not sys.argv[2].isdigit():
        sql = "select roomno from mud_room where abbr = '%s' or roomname = '%s'" % (sys.argv[2], sys.argv[2])
        cursor = conn.execute(sql)
        row = cursor.fetchone()
        if row:
            dst_room = row[0]
        else:
            dst_room = -1
    else:
        dst_room = int(sys.argv[2])

    conn.execute ("create temp table mud_entrance_weight (roomno int, linkroomno int, weight int)")
    conn.execute("insert into mud_entrance_weight select roomno, linkroomno, weight from mud_entrance where weight is not null")
    
    paths = shortest_path(conn,int(sys.argv[1]),dst_room)
    # paths = shortest_path(conn, 260, 283)
    tt = Tintin()
    tt.write ("#list shortest_path create {%s}\n" % (";".join(paths)))
