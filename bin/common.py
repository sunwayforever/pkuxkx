#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3
import logging

from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.NOTSET)

_handler = RotatingFileHandler('/tmp/pkuxkx.log', maxBytes=10*1024*1024,backupCount=5)
_handler.setFormatter(logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s"))
logger.addHandler(_handler)

def open_gps_database():
    return sqlite3.connect("db/rooms.db")

import uuid

class Tintin:
    def __init__ (self):
        self._file_name = "/tmp/pkuxkx_"+uuid.uuid4().hex
        self._tmpfile = open(self._file_name, "w")
        
    def write (self, command):
        self._tmpfile.write(command)

    def __del__ (self):
        self._tmpfile.close();
        print (self._file_name)

        
