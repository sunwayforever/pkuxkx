#!/usr/bin/env ruby
# coding: utf-8
require 'iconv'

conv = Iconv.new('UTF-8', 'GBK')
conv2 = Iconv.new('GBK', 'UTF-8')
fh = File.new("/tmp/pkuxkx_burden", "w")
fh.puts "#class burden_tmp open;"
fh.puts "@mapcreate{burden};"
for str in conv.iconv(ARGV[0]).split (/  +/)
  if (/([一二三四五六七八九十百千万]+).(.*?)\(.*?\)/ =~ str)
    item_name = $2
    item_count = $1
  elsif (/(.*?)\(.*?\)/ =~ str)
    item_name = $1
    item_count = "一"
  end
  tmp = "@mapset{burden;#{item_name};#{item_count}};"
  fh.puts conv2.iconv(tmp)
end
fh.puts "#class burden_tmp close;"
fh.close
