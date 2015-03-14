#!/usr/bin/env python3
import sys
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout

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

if __name__ == '__main__':
    xmpp = Bot(sys.argv[1]+'@localhost/xkx', '123456')
    xmpp.connect(("45.62.101.109",5222))
    xmpp.process(block=False)
    while (True):
        line = sys.stdin.readline()
        xmpp.send_message(mto="messenger@localhost/xkx", mbody=line, mtype='chat')

