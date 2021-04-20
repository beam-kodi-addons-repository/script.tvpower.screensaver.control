import os,sys
import xbmc, xbmcaddon

__addon__         = xbmcaddon.Addon()
__cwd__           = __addon__.getAddonInfo('path')
__scriptname__    = __addon__.getAddonInfo('name')
__version__       = __addon__.getAddonInfo('version')
__language__      = __addon__.getLocalizedString
__resource_path__ = os.path.join(__cwd__, 'resources', 'lib')
__resource__      = xbmc.translatePath(__resource_path__).decode('utf-8')

sys.path.append (__resource__)

from tv_power_control import TVPowerControl
from utilities import log

class KodiMonitor(xbmc.Monitor):

    def onSettingsChanged(self):
        tvpower.load_settings()

    def onNotification(self, sender, method, data):
        if method == "Player.OnPlay": tvpower.check_monitor("player_stared")

    def onScreensaverActivated(self):
        tvpower.check_monitor("screen_saver_activated")

    def onScreensaverDeactivated(self):
        tvpower.check_monitor("screen_saver_deactivated")

if (__name__ == "__main__"):
    log("Starting monitor.. " + __version__)
    monitor = KodiMonitor()
    tvpower = TVPowerControl(__addon__, monitor)
    while not monitor.abortRequested():
        if monitor.waitForAbort(10): break
        tvpower.check_monitor()
    del monitor
    log("Stopped monitor.. " + __version__)
