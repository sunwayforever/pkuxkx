#!/usr/bin/env ruby
require 'sqlite3'
require 'iconv'

conv = Iconv.new('UTF-8', 'GBK')

$db = SQLite3::Database.new('pinyin.db')

def get_pinyin (name)
  ret = ""
  name.each_char {|v|
    sql = "select pinyin from pinyin where char = \"#{v}\""
    rows = $db.execute(sql)
    if rows
      ret << rows[0][0]
    end
  }
  return ret
end

def get_xing (name)
  ret = ""
  sql = "select pinyin from xing where char = \"#{name}\""
  rows = $db.execute(sql)
  if rows.empty?
    return get_pinyin(name)
  else
    return rows[0][0]
  end
end

def get_fuxing (name)
  sql = "select pinyin from fuxing where char = \"#{name}\""
  rows = $db.execute(sql)
  if rows.empty?
    return nil
  else
    return rows[0][0]
  end  
end

surname_py = ""
name_py = ""

name = conv.iconv(ARGV[0])
surname_py = get_fuxing(name[0,2])
if surname_py
  name_py = get_pinyin(name[2,name.length])
else
  surname_py = get_xing(name[0])
  name_py = get_pinyin(name[1,name.length])
end

puts surname_py+" "+name_py
    
  
