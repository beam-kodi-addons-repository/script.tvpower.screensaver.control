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

from tv_power_control import TVPowerContorl

tvpower = TVPowerContorl(__addon__, None, True)

def log(message):
    xbmc.log("### TV power controller: " + str(message), level=xbmc.LOGNOTICE)

if len(sys.argv) < 2: log("No arguments")

for action in sys.argv:
    if action == "tv_on":
        log("Command execute TV_ON")
        tvpower.turn_on_tv()
    elif action == "tv_off":
        log("Command execute TV_OFF")
        tvpower.turn_off_tv()
    elif action == "screen_saver":
        log("Command execute SCREEN SAVER")
        xbmc.executebuiltin("XBMC.ActivateScreensaver()")