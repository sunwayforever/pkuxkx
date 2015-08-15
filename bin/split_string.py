#!/usr/bin/env python3
# -*- coding: utf-8 -*-  

import sys
from .common import Tintin

if __name__ == "__main__":
    tt = Tintin()
    orig_string = sys.argv[1]
    chunk_size = int(sys.argv[2])
    ret = [orig_string[i:i+chunk_size] for i in range(0, len(orig_string), chunk_size) ]
    tt.write("#list split_string create {"+";".join(ret)+"};")
    


