#!/usr/bin/env ruby
require 'sqlite3'
require 'iconv'

conv = Iconv.new('UTF-8', 'GBK')
rconv = Iconv.new('GBK', 'UTF-8')

request_exits = ARGV.shift.split(',').sort!.join('|')
keys = conv.iconv(ARGV.shift)
# keys = ARGV.shift

db = SQLite3::Database.new('/home/sunway/.tt/archive/task_room_utf8.db')
sql = 'select name,zone,map from task_room where 1'
keys.each_char do |key|
  sql << " and desc like '%#{key}%'"
end

sql << " and exits == '#{request_exits}'"
sql << ' limit 3'

rows = db.execute(sql)
rows.each do |row|
  puts rconv.iconv(row[0])
  puts rconv.iconv(row[1])
  puts rconv.iconv(row[2])
  puts '----'
end

