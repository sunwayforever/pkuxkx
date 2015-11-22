#!/usr/bin/env python3
import sys
import re
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from urllib.request import urlopen
from threading import Thread
import socket

class Bot(ClientXMPP):
    def __init__(self, jid):
        ClientXMPP.__init__(self, jid+'@v587.info/xkx', "123456")
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print ("xmpp message: %s:%s\n" % (msg['from'],msg['body']))

def send_image_async(xmpp, url, char_id):
    try:
        html = urlopen(url,timeout=5).readline().decode('utf-8')
        m = re.match(".*img src=\"(.*)\" alt",html)
        if not m:
            return
        handle = urlopen("http://pkuxkx.net/antirobot/"+m.group(1),timeout=5)
        image_file = open("/var/www/image_pkuxkx/%s.png"%(char_id),"wb")
        image_file.write(handle.read())
        image_file.close()
        xmpp.send_message(mto="messenger@v587.info/xkx", mbody="http://v587.info:8080/image_pkuxkx/%s.png"%(char_id), mtype='chat')
    except:
        pass
    
    
if __name__ == '__main__':
    socket.setdefaulttimeout(10)
    char_id = sys.argv[1]
    xmpp = Bot(char_id)
    xmpp.connect(("v587.info",5222))
    xmpp.process(block=False)
    while (True):
        line = sys.stdin.readline()
        m = re.match("status: (.*)", line)
        if m:
            status = m.group(1)
            xmpp.send_presence(pstatus=status, pshow='xa')
        else:
            xmpp.send_message(mto="messenger@v587.info/xkx", mbody=line, mtype='chat')
            m = re.match("http://pkuxkx.net/antirobot/robot.php", line)
            if m:
                Thread(target=send_image_async,args=[xmpp,line,char_id]).start()
