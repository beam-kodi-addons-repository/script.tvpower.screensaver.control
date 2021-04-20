from utilities import log
from tvrc_baseclass import BaseTVRemoteControl
import socket
import base64

class TVRC_SamsungPre2016(BaseTVRemoteControl):

    app_name = "Kodi Remote Control"
    app_desc = "TV power controller"
    app_id = "script.tvpower.screensaver.control"

    @classmethod
    def ident_desc(cls):
        return "Remote Control pre-2016 Samsung TVs. Params: Hostname"

    def __init__(self, host):
        self.host = host

    def turn_off(self):
        self.__push_key("KEY_POWEROFF")

    def __push_key(self, key):
        sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sck.connect((self.host, 55000))
        msg = chr(0x64) + chr(0x00) +\
            chr(len(base64.b64encode(self.app_id)))   + chr(0x00) + base64.b64encode(self.app_id) +\
            chr(len(base64.b64encode(self.app_desc))) + chr(0x00) + base64.b64encode(self.app_desc) +\
            chr(len(base64.b64encode(self.app_name))) + chr(0x00) + base64.b64encode(self.app_name)
        pkt = chr(0x00) * 3 + chr(len(msg)) + chr(0x00) + msg  
        sck.send(pkt)
        msg = chr(0x00) * 3 + chr(len(base64.b64encode(key))) + chr(0x00) + base64.b64encode(key)
        pkt = chr(0x00) * 3 + chr(len(msg)) + chr(0x00) + msg  
        sck.send(pkt)
        sck.close()
