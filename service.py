import os,sys
import xbmc, xbmcaddon
import time

if sys.version_info < (2, 7):
    import simplejson as json
else:
    import json

__addon__         = xbmcaddon.Addon()
__cwd__           = __addon__.getAddonInfo('path')
__scriptname__    = __addon__.getAddonInfo('name')
__version__       = __addon__.getAddonInfo('version')
__language__      = __addon__.getLocalizedString
__resource_path__ = os.path.join(__cwd__, 'resources', 'lib')
__resource__      = xbmc.translatePath(__resource_path__).decode('utf-8')

sys.path.append (__resource__)

from utilities import log

class KodiMonitor(xbmc.Monitor):

    sef.screensaver_running = False

    def onSettingsChanged(self):
        global __addon__
        __addon__ = xbmcaddon.Addon()

    def onNotification(self, sender, method, data):
        log([method,data])
        # parsed_data = json.loads(data)

    def onScreensaverActivated(self):
        log("screen saver on")
        self.screensaver_running = True

    def onScreensaverDeactivated(self):
        log("screen saver off")
        self.screensaver_running = False


if (__name__ == "__main__"):
    log("Starting.. " + __version__)
    monitor = KodiMonitor()
    while not monitor.abortRequested():
	    if monitor.waitForAbort(10): break
    del monitor
    log("Stopped.. " + __version__)
