#!/usr/bin/env python3
import sys
import re
import os
import time
import uuid
from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout
from urllib.request import urlopen
from threading import Thread
import socket

class Bot(ClientXMPP):
    def __init__(self, jid):
        ClientXMPP.__init__(self, jid+'@localhost/xkx', "123456")
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            print ("xmpp message: %s:%s\n" % (msg['from'],msg['body']))

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]  
            
def remove_old_file():
    ten_minute_ago = time.time() - 600
    folder = '/var/www/image_pkuxkx/'
    os.chdir(folder)
    for somefile in os.listdir('.'):
        st=os.stat(somefile)
        mtime=st.st_mtime
        if mtime < ten_minute_ago:
            os.unlink(somefile)
            
def send_image_async(xmpp, url, char_id):
    try:
        remove_old_file()
        html = urlopen(url,timeout=5).readline().decode('utf-8')
        m = re.match(".*img src=\"(.*)\" alt",html)
        if not m:
            return
        file_name = str(uuid.uuid4())
        handle = urlopen("http://pkuxkx.net/antirobot/"+m.group(1),timeout=5)
        image_file = open("/var/www/image_pkuxkx/%s.png"%(file_name),"wb")
        image_file.write(handle.read())
        image_file.close()
        xmpp.send_message(mto="messenger@v587.info/xkx", mbody="http://%s:8080/image_pkuxkx/%s.png"%(get_ip_address(), file_name), mtype='chat')
    except:
        pass
    
if __name__ == '__main__':
    socket.setdefaulttimeout(10)
    char_id = sys.argv[1]
    xmpp = Bot(char_id)
    xmpp.connect(("bandwagon.v587.info",5222))
    xmpp.process(block=False)
    while (True):
        line = sys.stdin.readline()
        m = re.match("status: (.*)", line)
        if m:
            status = m.group(1)
            xmpp.send_presence(pstatus=status, pshow='xa')
        else:
            xmpp.send_message(mto="messenger@localhost/xkx", mbody=line, mtype='chat')
            m = re.match("http://pkuxkx.net/antirobot/robot.php", line)
            if m:
                Thread(target=send_image_async,args=[xmpp,line,char_id]).start()
