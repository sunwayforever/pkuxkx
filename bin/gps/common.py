#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sqlite3

def open_database():
    return sqlite3.connect("db/rooms.db")
    
def fixup_area(desc):
    if re.match("^(长江|黄河)[^南北]",desc):
        desc =  desc[:2]+"南岸"+desc[2:]
    elif re.match("^建康府.城",desc):
        desc = desc[:4]+desc[5:]
    elif re.match("^白驼山",desc):
        desc = desc[:2]+desc[3:]
    elif re.match("^小山村",desc):
        desc = "华山村"+desc[3:]
    return desc
    
