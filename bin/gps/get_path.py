##!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sqlite3
import os
import sys
import heapq

from .common import *
from ..common import Tintin
from ..common import logger

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
        self.weights_info_saved = {}
        self.__load_data()
        self.__reset_weights()

    def __reset_weights(self):
        self.weights_info = self.weights_info_saved.copy()

    def __load_data(self):
        sql = "select max(roomno) from mud_room"
        row = self.conn.execute(sql).fetchone();
        self.max_room_no = int(row[0])+1
        
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
            self.weights_info[(row[0],row[1])] = 0

        self.weights_info_saved = self.weights_info.copy()
            
    def get_path(self, src, dst):
        self.__reset_weights();
        return self.__shortest_path_dijkstra(src,dst)

    def __shortest_path_dijkstra(self, src, dst):
        if (src == dst):
            return []

        pq = []
        distance = [-1] * self.max_room_no
        parent = [None] * self.max_room_no
        distance[src] = 0
        found = False
        heapq.heappush(pq, (0,src))
        
        while len(pq) != 0:
            i = heapq.heappop(pq)[1]
            for link in self.neighbours[i]:
                d = link.linkroomno
                weight = self.weights_info[(i,link.linkroomno)]
                if weight < 0:
                    continue;
                if distance[d] > distance[i]+weight or distance[d] == -1:
                    distance[d] = distance[i]+weight
                    parent[d] = link
                    heapq.heappush(pq, (distance[d],d))

        if not parent[dst]:
            return []

        ret = []
        tail = dst;
        while tail != src:
            ret.insert(0,parent[tail].direction)
            tail = parent[tail].roomno
        return ret
    
    def __shortest_path_test(self, src, dst):
        if (src == dst):
            return []

        distance = [-1]*self.max_room_no
        parent = [None]*self.max_room_no
        distance[src] = 0

        curr_set = set([src])
        found = False

        while not found:
            shortest_link = []
            shortest_distance = -1

            for i in curr_set:
                for link in self.neighbours[i]:
                    if link.linkroomno in curr_set:
                        continue;
                    weight = self.weights_info[(i,link.linkroomno)]
                    if weight < 0:
                        continue;
                    if weight < shortest_distance or shortest_distance == -1:
                        shortest_distance = weight
                        shortest_link = [link]
                    elif weight == shortest_distance:
                        shortest_link.append(link)

            if len(shortest_link) == 0:
                break

            for link in shortest_link:
                s = link.roomno
                d = link.linkroomno
                curr_set.add(d)
                if (distance[d] > distance[s]+self.weights_info[(s, d)] or distance[d] == -1):
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
    
    def __shortest_path_bfs(self, src, dst):
        if (src == dst):
            return []
        
        src_set = set([src])
        dst_set = set([dst])
            
        while True:
            updated = False
            tmp_set = set()
            for i in src_set:
                if not i in self.neighbours:
                    break
                for link in self.neighbours[i]:
                    current_weight = self.weights_info[(link.roomno,link.linkroomno)]
                    if  current_weight == 0:
                        if not link.linkroomno in src_set:
                            updated = True
                            tmp_set.add(link.linkroomno)
                    elif current_weight > 0:
                        updated = True
                        self.weights_info[(link.roomno,link.linkroomno)] = current_weight - 1
                        
            src_set=src_set.union(tmp_set)

            tmp_set = set()
            for i in dst_set:
                if not i in self.rev_neighbours:
                    break            
                for link in self.rev_neighbours[i]:
                    current_weight = self.weights_info[(link.roomno,link.linkroomno)]
                    if current_weight == 0:
                        if not link.roomno in dst_set:
                            updated = True
                            tmp_set.add(link.roomno)
                    elif current_weight > 0:
                        self.weights_info[(link.roomno,link.linkroomno)] = current_weight - 1
                        
            dst_set=dst_set.union(tmp_set)

            if not updated:
                return []

            intersection = src_set.intersection(dst_set)
            if (intersection):
                if src in intersection and dst in intersection:
                    for link in self.neighbours[src]:
                        if link.linkroomno == dst:
                            return [link.direction]
                else:
                    middle = intersection.pop()
                    ret = self.__shortest_path_bfs(src, middle)
                    ret.extend(self.__shortest_path_bfs(middle, dst))
                    return ret
        
def get_path(from_room, to_room, weights):
    if to_room == -1:
        return []
    
    global char_id
    has_sibao = os.path.isfile("/tmp/pkuxkx_sibao_%s.lock"%(char_id))

    conn = open_database()
    from_zone = get_zone(conn,from_room)
    to_zone = get_zone(conn,to_room)

    mud = MudRoom(conn, weights)

    if to_zone == "梅庄" and from_zone != to_zone:
        paths = mud.get_path(from_room, 3655)
        paths.append("gps.qu_sibao")
        paths.extend(mud.get_path(3655,to_room))
        return paths;

    if to_zone == "梅庄" and from_zone == to_zone:
        return mud.get_path(from_room, to_room)

    if has_sibao == True:
        paths = mud.get_path(from_room, 3655)
        paths.append("gps.huan_sibao")
        paths.extend(mud.get_path(3655,to_room))
        return paths;
    
    return mud.get_path(from_room, to_room)

if __name__ == "__main__":
    global char_id
    
    from_room = int(sys.argv[1])
    to_room = int(sys.argv[2])
    weights = sys.argv[3]
    char_id = sys.argv[4]

    paths = get_path(from_room,to_room,weights)
    
    tt = Tintin()
    tt.write ("#list gps_path create {%s};\n" % (";".join(paths)))
