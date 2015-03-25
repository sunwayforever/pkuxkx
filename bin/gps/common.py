#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

def open_database():
    if os.path.isfile("db/gps/rooms.db"):
        conn = sqlite3.connect("db/gps/rooms.db")
    else:
        conn = sqlite3.connect("db/gps_sample/rooms.db")
    return conn
    
