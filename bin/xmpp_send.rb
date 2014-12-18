#!/usr/bin/env ruby
require 'rubygems'
require "iconv"

pipe_name="/tmp/xmpp_pipe_sent_"+ARGV[0]
pipe_file=File.open(pipe_name,"w+")

pipe_file.puts ARGV[1]

conv = Iconv.new("UTF-8","GBK");
msg=conv.iconv(ARGV[2])
pipe_file.puts msg

pipe_file.flush
