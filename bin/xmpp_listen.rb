#!/usr/bin/ruby1.8

require 'rubygems'
require 'xmpp4r'
require 'iconv'

include Jabber

sender = JID.new(ARGV[0] + '@localhost/xkx')
recved_msg_pipe_name = '/tmp/xmpp_pipe_recved_' + ARGV[0]
sent_msg_pipe_name = '/tmp/xmpp_pipe_sent_' + ARGV[0]
# receiver= JID.new(ARGV[1]+"@localhost/xkx");
# conv = Iconv.new("UTF-8","GBK");

cl = Client.new(sender)
cl.connect("54.64.198.143")
cl.auth("123456")
cl.send(Presence.new)

system("rm "+recved_msg_pipe_name)
system("mkfifo "+recved_msg_pipe_name)
system("rm "+sent_msg_pipe_name)
system("mkfifo "+sent_msg_pipe_name)

recved_msg_file=File.open(recved_msg_pipe_name,"w+")
sent_msg_file=File.open(sent_msg_pipe_name,"r+")

mainthread = Thread.current

Thread.new do
  loop do
    begin
      Timeout::timeout(0.5) do
        receiver_name=sent_msg_file.gets
        sent_msg=sent_msg_file.gets
        msg = Message.new(JID.new(receiver_name.chomp+"@localhost/xkx"))
        msg.set_body(sent_msg);
        cl.send msg
        sleep 1
      end
    rescue Exception => e
      sleep 5
    end
  end
end

conv = Iconv.new("GBK","UTF-8")
cl.add_message_callback do |m|
  recved_msg_file.puts JID.new(m.from).node
  recved_msg_file.puts conv.iconv(m.body)
  recved_msg_file.flush
end

Thread.stop
cl.close
