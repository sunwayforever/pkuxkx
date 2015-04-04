#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3

def open_database():
    return sqlite3.connect("db/rooms.db")
    
