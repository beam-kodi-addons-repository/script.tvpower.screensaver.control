import os,sys
import xbmc, xbmcaddon
import time
import subprocess

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
    xbmc.log("### " + __scriptname__ + ": " + str(message), level=xbmc.LOGDEBUG)

class TVPowerContorl(object):

    target_time_for_execution = 0

    def __init__(self):
        self.load_settings()

    def load_settings(self):
        log("loading settings")
        self.turn_off_activated = bool(__addon__.getSetting("turn_off_activated"))
        self.turn_off_after = int(__addon__.getSetting("turn_off_wait_time"))
        self.stop_player_on_turn_off = bool(__addon__.getSetting("turn_off_stop"))
        self.turn_off_action = __addon__.getSetting("turn_off_action")

        self.turn_on_deactivated = bool(__addon__.getSetting("turn_on_deactivated"))
        self.turn_on_player_start = bool(__addon__.getSetting("turn_on_player"))

        self.cec_method = __addon__.getSetting("cec_method")
        self.cec_client_command = __addon__.getSetting("cec_client_path")

    turn_off_tv_after = 1 # read from settings
    turn_on_tv_on_player_start = True

    def stop_player(self):
        log("stop player")
        if xbmc.Player().isPlaying() == True: xbmc.Player().stop()

    def turn_off_hook_action(self):
        log(["turn off post action", self.turn_off_action])
        if self.turn_off_action == "none":
            return False
        elif self.turn_off_action == "restart":
            xbmc.executebuiltin('XBMC.RestartApp()')
        elif self.turn_off_action == "reboot":
            xbmc.restart()
        elif self.turn_off_action == "shutdown":
            xbmc.shutdown()
        return True

    def turn_off_tv(self):
        log(["turn_off_tv", self.turn_off_activated])
        if self.turn_off_activated == False: return False
        # do action
        if self.cec_method == "kodi":
            xbmc.executebuiltin('XBMC.CECStandby()')
        elif self.cec_method == "cec-client":
            subprocess.call("echo 'standby 0' | " + self.cec_client_command + " -s", shell=True)
            
        if self.stop_player_on_turn_off == True: self.stop_player()
        self.turn_off_hook_action()
        return True

    def turn_on_tv(self):
        log(["turn_on_tv", self.turn_on_deactivated])
        if self.turn_on_deactivated == False: return False
        # do action
        if self.cec_method == "kodi":
            xbmc.executebuiltin('XBMC.CECActivateSource()')
        elif self.cec_method == "cec-client":
            subprocess.call("echo 'on 0' | " + self.cec_client_command + " -s", shell=True)

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
        if event == "screen_saver_activated": self.target_time_for_execution = time.time() + (self.turn_off_after * 60)

        if monitor.screensaver_running == True and self.target_time_for_execution > 0 and self.target_time_for_execution <= time.time():
            self.target_time_for_execution = 0
            self.execute_command("screen_saver_activated_target_time_ago")

class KodiMonitor(xbmc.Monitor):

    screensaver_running = False

    def onSettingsChanged(self):
        global __addon__
        __addon__ = xbmcaddon.Addon()
        tvpower.load_settings()

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
