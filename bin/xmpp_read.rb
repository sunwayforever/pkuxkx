#!/usr/bin/env ruby
require 'rubygems'
require 'timeout'

pipe_name="/tmp/xmpp_pipe_recved_"+ARGV[0]
file=File.open(pipe_name,"r")
begin
  Timeout::timeout(0.5) do
    puts file.gets
    puts file.gets
  end
rescue Exception => e
  puts "nil"
end
