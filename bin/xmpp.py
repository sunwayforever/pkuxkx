#!/usr/bin/env python3
import sys
import re
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from urllib.request import urlopen

class Bot(ClientXMPP):
    def __init__(self, jid, password):
        ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print ("xmpp message: %s:%s\n" % (msg['from'],msg['body']))

def send_image(xmpp, url):
    html = urlopen(url).readline().decode('utf-8')
    m = re.match(".*img src=\"(.*)\" alt",html)
    if m:
        image_url = "http://pkuxkx.net/antirobot/"+m.group(1)
        xmpp.send_message(mto="messenger@v587.info/xkx", mbody=image_url, mtype='chat')
        
if __name__ == '__main__':
    xmpp = Bot(sys.argv[1]+'@v587.info/xkx', '123456')
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
                send_image(xmpp, line)

