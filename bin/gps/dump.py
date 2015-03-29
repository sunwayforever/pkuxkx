#!/usr/bin/env python3
# -*- coding: utf-8 -*-  
import pydot
import sys
import sqlite3
from .common import open_database

if __name__ == "__main__":
    graph = pydot.Dot(graph_type="graph")
    s = {}
    sql = "select src_room_name, dst_room_name, src_room_no, dst_room_no from room_and_entrance where src_room_zone = '扬州城'"
    conn = open_database()
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        src_node = s.get (row[2])
        dst_node = s.get(row[3])
        if not src_node:
            src_node = pydot.Node(row[0])
            s[row[2]] = src_node
            graph.add_node(src_node)
        if not dst_node:
            dst_node = pydot.Node(row[1])
            s[row[3]] = dst_node
            graph.add_node(dst_node)
        graph.add_edge(pydot.Edge(src_node, dst_node))
    graph.write_png ("test.png")
