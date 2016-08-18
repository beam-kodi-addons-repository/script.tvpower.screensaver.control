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

def log(message):
    xbmc.log("### " + __scriptname__ + ": " + str(message), level=xbmc.LOGNOTICE)

class TVPowerContorl(object):

    target_time_for_execution = 0
    turn_off_tv_after = 1 # read from settings
    turn_on_tv_on_player_start = True

    def turn_off_tv(self):
        log("turn_off_tv")
        if xbmc.Player().isPlaying() == True: xbmc.Player().stop()
        # xbmc.restart() - restart PC
        return True

    def turn_on_tv(self):
        log("turn_on_tv")
        return True

    def execute_command(self, event):
        log(["Execute", event])
        if event == "screen_saver_activated_target_time_ago":
            self.turn_off_tv()
        elif event == "screen_saver_deactivated":
            self.turn_on_tv()
        elif event == "player_stared" and self.turn_on_tv_on_player_start:
            self.turn_on_tv()
      
        # screen_saver_activated
        # screen_saver_deactivated
        # screen_saver_activated_target_time_ago
        # player_stared

    def check_monitor(self, event = None):
        log(["Check monitor", monitor.screensaver_running])
        if event != None: self.execute_command(event)
        if event == "screen_saver_activated": self.target_time_for_execution = time.time() + (self.turn_off_tv_after * 60)

        if monitor.screensaver_running == True and self.target_time_for_execution > 0 and self.target_time_for_execution <= time.time():
            self.target_time_for_execution = 0
            self.execute_command("screen_saver_activated_target_time_ago")

class KodiMonitor(xbmc.Monitor):

    screensaver_running = False

    def onSettingsChanged(self):
        global __addon__
        __addon__ = xbmcaddon.Addon()

    def onNotification(self, sender, method, data):
        log([method,data])
        if method == "Player.OnPlay": tvpower.check_monitor("player_stared")

    def onScreensaverActivated(self):
        log("onScreensaverActivated")
        self.screensaver_running = True
        tvpower.check_monitor("screen_saver_activated")

    def onScreensaverDeactivated(self):
        log("onScreensaverDeactivated")
        self.screensaver_running = False
        tvpower.check_monitor("screen_saver_deactivated")

if (__name__ == "__main__"):
    log("Starting.. " + __version__)
    monitor = KodiMonitor()
    tvpower = TVPowerContorl()
    while not monitor.abortRequested():
        if monitor.waitForAbort(10): break
        tvpower.check_monitor()
    del monitor
    log("Stopped.. " + __version__)
