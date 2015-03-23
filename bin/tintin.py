#!/usr/bin/env python
import uuid

class Tintin:
    def __init__ (self):
        self._file_name = "/tmp/pkuxkx_"+uuid.uuid4().hex
        self._tmpfile = open(self._file_name, "w")
        
    def command (self, command):
        self._tmpfile.write(command)
        
    def RETURN (self):
        self._tmpfile.close();
        print (self._file_name)
        
