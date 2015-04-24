#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import sys
from ..common import open_gps_database
from ..common import Tintin
from ..common import logger

def locate(conn, all_desc,exits):
    exits = exits.replace(",",";")
    exits = exits+";"
    roomnos = set()
    logger.error("locate %s"%(all_desc))
    for room_desc in all_desc.split(":"):
        desc_list = room_desc.split(",")
        logger.error("locate for %s returns desc_list: %s "%(room_desc, str(desc_list)))
        for desc in desc_list:
            sql = "select roomno from mud_room where description like '%%%s%%' and exits = '%s'" % (desc,exits)
            rows = conn.execute(sql).fetchall()
            if rows:
                logger.error("query for %s returns %s" %(desc,str(rows)))
                if len(roomnos) != 0:
                    roomnos =  roomnos.intersection(set(rows))
                    logger.error("after intersection, roomnos  %s" %(str(roomnos)))
                else:
                    roomnos = set(rows)
                
    if len(roomnos) == 1:
        return roomnos.pop()
    else:
        return -1
                    
            
if __name__ == "__main__":
    desc = sys.argv[1]
    exits = sys.argv[2]

    conn = open_gps_database()

    roomno = locate(conn,desc,exits)
    tt = Tintin()
    tt.write ("#var task.roomno %d;\n" % (roomno))

    if (roomno != -1):
        sql = "select roomname, zone from mud_room where roomno = %d" %(roomno)
        row = conn.execute(sql).fetchone()
        tt.write ("#var task.roomname %s;\n" % (row[0]))
        tt.write ("#var task.zone %s;\n" % (row[1]))
        

    
