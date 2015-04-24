#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from .common import Tintin

if __name__ == '__main__':
    tt = Tintin()
    tt.write("#class burden_tmp kill;\n")
    tt.write("#class burden_tmp open;\n")
    tt.write("@mapcreate{burden};\n")

    for item in re.split("  +", sys.argv[1]):
        m = re.match("([一二三四五六七八九十百千万]+).(.*?)\(.*?\)", item)
        if m:
            item_name = m.group(2)
            item_count = m.group(1)
        else:
            m = re.match("(.*?)\(.*?\)",item)
            if m:
                item_name = m.group(1)
                item_count = "一"
        tt.write("@mapset{burden;%s;%s};\n" % (item_name, item_count))
    tt.write("#class burden_tmp close;\n")
