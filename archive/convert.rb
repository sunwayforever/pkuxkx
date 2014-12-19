#!/usr/bin/env ruby
require 'sqlite3'
require 'iconv'

rconv = Iconv.new('UTF-8', 'GBK')

db = SQLite3::Database.new('/home/sunway/.tt/pinyin.db')
sql = 'select * from pinyin'
rows = db.execute(sql)
db.execute("delete from pinyin2")
db.execute("begin")
rows.each do |row|
  char = rconv.iconv(row[0])
  db.execute("insert into pinyin2 values (\"#{char}\", \"#{row[1]}\")")
end
db.execute("commit")

sql = 'select * from fuxing'
rows = db.execute(sql)
db.execute("delete from fuxing2")
db.execute("begin")
rows.each do |row|
  char = rconv.iconv(row[0])
  db.execute("insert into fuxing2 values (\"#{char}\", \"#{row[1]}\")")
end
db.execute("commit")
