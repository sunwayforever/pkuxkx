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
    pattern = "([零一二三四五六七八九十百千万]+)[串事册丘乘下丈丝两举具美包厘刀分列则剂副些匝队陌陔部出个介令份伙件任倍儋卖亩记双发叠节茎莛荮落蓬蔸巡过进通造遍道遭对尊头套弓引张弯开庄床座庹帖帧席常幅幢口句号台只吊合名吨和味响骑门间阕宗客家彪层尾届声扎打扣把抛批抔抱拨担拉抬拃挂挑挺捆掬排捧掐搭提握摊摞撇撮汪泓泡注浔派湾溜滩滴级纸线组绞统绺综缕缗场块坛垛堵堆堂塔墩回团围圈孔贴点煎熟车轮转载辆料卷截户房所扇炉炷觉斤笔本朵杆束条杯枚枝柄栋架根桄梃样株桩梭桶棵榀槽犋爿片版歇手拳段沓班文曲替股肩脬腔支步武瓣秒秩钟钱铢锊铺锤锭锱章盆盏盘眉眼石码砣碗磴票罗畈番窝联缶耦粒索累緉般艘竿筥筒筹管篇箱簇角重身躯酲起趟面首项领顶颗顷袭群袋](.*?)\(.*?\)"
    prog = re.compile(pattern)
    
    for item in re.split("  +", sys.argv[1]):
        m = prog.match(item)
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
