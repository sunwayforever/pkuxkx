#!/usr/bin/env ruby

require 'rubygems'
require 'xmpp4r'
require 'iconv'

include Jabber
$cl = nil;
$conv_to_mud = Iconv.new("GBK","UTF-8")
$conv_from_mud = Iconv.new("GBK","UTF-8")

def xmpp_login (sender_name)
  sender = JID.new(sender_name + '@localhost/xkx')

  $cl = Client.new(sender)
  $cl.connect("54.64.198.143")
  $cl.auth("123456")
  $cl.send(Presence.new)

  $cl.add_message_callback do |m|
    puts "xmpp message: %s:%s"%[JID.new(m.from).node,$conv_to_mud.iconv(m.body)]
  end
end

def xmpp_send(receiver_name, sent_msg)
  begin
    msg = Message.new(JID.new("messenger@localhost/xkx"))
    msg.set_body($conv_from_mud.iconv(receiver_name+": "+sent_msg))
    $cl.send msg
  rescue Exception => e
  end
end
