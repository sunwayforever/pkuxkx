##!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sqlite3
import os
import sys

class Link:
    def __init__(self,roomno,linkroomno,direction,weight_type,is_boundary, linkroomname, src_room_zone, dst_room_zone):
        self.roomno = roomno
        self.linkroomno = linkroomno
        self.direction = direction
        self.weight_type = weight_type
        self.is_boundary = is_boundary
        self.linkroomname = linkroomname
        self.src_room_zone = src_room_zone
        self.dst_room_zone = dst_room_zone
        

class MudRoom:
    def __init__ (self,conn, weights):
        self.neighbours = {}
        self.rev_neighbours = {}
        self.weights = weights
        self.conn = conn
        self.weights_info = {}
        self.__load_data()

    def __load_data(self):
        sql = "select src_room_no, dst_room_no, direction, weight_type, is_boundary, dst_room_name, src_room_zone, dst_room_zone from room_and_entrance"
        rows = self.conn.execute(sql).fetchall()
        for row in rows:
            link = Link(row[0],row[1],row[2],row[3],row[4], row[5], row[6], row[7])
            if not row[0] in self.neighbours:
                self.neighbours[row[0]]=[]
            self.neighbours[row[0]].append(link)
                
            if not row[1] in self.rev_neighbours:
                self.rev_neighbours[row[1]]=[]
            self.rev_neighbours[row[1]].append(link)

        weights_list = [int(x) for x in self.weights.split(",")]
        for i,w in enumerate(weights_list, start=1):
            sql = "select roomno, linkroomno from mud_entrance where weight_type = %d" % (i)
            rows = self.conn.execute(sql).fetchall()
            for row in rows:
                self.weights_info[(row[0],row[1])] = w

        sql = "select roomno, linkroomno from mud_entrance where weight_type = 0"
        rows = self.conn.execute(sql).fetchall()
        for row in rows:
            self.weights_info[(row[0],row[1])] = 1

        self.weights_info_saved = self.weights_info.copy()
            
    def get_path(self, src, dst):
        return self.__shortest_path(src,dst)
    
    def __shortest_path(self, src, dst):
        INF = 1000
        if (src == dst):
            return []
        distance = [INF]*4000
        parent = [None]*4000
        distance[src] = 0

        src_set = set([src])
        found = False

        while not found:
            shortest_link = []
            shortest_distance = INF

            for i in src_set:
                for link in self.neighbours[i]:
                    if link.linkroomno in src_set:
                        continue
                    weight = self.weights_info[(i,link.linkroomno)]
                    if weight < 0:
                        continue
                    if weight < shortest_distance:
                        shortest_distance = weight
                        shortest_link = [link]
                    elif weight == shortest_distance:
                        shortest_link.append(link)

                        # now shortest_link contains all the shortest links from src_set
            if len(shortest_link) == 0:
                break

            for link in shortest_link:
                s = link.roomno
                d = link.linkroomno
                src_set.add(d)
                if (distance[d] > distance[s]+self.weights_info[(s, d)]):
                    distance[d] = distance[s]+self.weights_info[(s, d)]
                    parent[d] = link
                if d == dst:
                    found = True
        if not found:
            return []

        ret = []
        tail = dst;
        while tail != src:
            ret.insert(0,parent[tail].direction)
            tail = parent[tail].roomno
        return ret

weights = "50,100,10,50,100,80,0,150"
# weights = "1,-1,1,-1,-1,1,1,1"
conn = sqlite3.connect("/home/sunway/.tt/db/rooms.db")
mud = MudRoom(conn, weights)

print (";".join(mud.get_path(260, 2270)))
