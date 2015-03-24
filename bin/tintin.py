#!/usr/bin/env python
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

        
