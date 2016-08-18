import sys
import xbmc, xbmcaddon, xbmcgui
import time

if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json

__addon__         = xbmcaddon.Addon()
__scriptname__    = __addon__.getAddonInfo('name')

def log(message):
    xbmc.log("### " + __scriptname__ + ": " + str(message), level=xbmc.LOGNOTICE)
