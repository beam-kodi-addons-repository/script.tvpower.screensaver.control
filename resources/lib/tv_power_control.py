import os,sys
import xbmc, xbmcaddon
import time

from utilities import log, exec_shell_command
from tvrc_main import tvrc_process_settings_string

class TVPowerControl(object):

    target_time_for_execution = 0
    turn_off_executed_at = 0
    at_least_ones_player_launched = False
    post_action_executed = False
    screensaver_running = False

    def __init__(self, addon, monitor, external_run = False):
        self.addon = addon
        self.monitor = monitor
        self.external_run = external_run
        self.load_settings()

    def load_settings(self):
        log("Loading settings")
        self.turn_off_activated = self.addon.getSetting("turn_off_activated") == 'true'
        self.turn_off_after = int(self.addon.getSetting("turn_off_wait_time"))
        self.stop_player_on_turn_off = self.addon.getSetting("turn_off_stop") == 'true'
        
        self.turn_off_action = self.addon.getSetting("turn_off_action")
        self.turn_off_player_ones_launched = self.addon.getSetting("turn_off_player_ones_launched") == 'true'

        self.turn_on_deactivated = self.addon.getSetting("turn_on_deactivated") == 'true'
        self.turn_on_player_start = self.addon.getSetting("turn_on_player") == 'true'

        self.turn_on_method = self.addon.getSetting("turn_on_method")
        self.turn_off_method = self.addon.getSetting("turn_off_method")
        self.cec_client_command = self.addon.getSetting("cec_client_path")
        self.turn_on_command = self.addon.getSetting("turn_on_command_path")
        self.turn_off_command = self.addon.getSetting("turn_off_command_path")
        self.turn_on_internal_command = self.addon.getSetting("turn_on_internal_command")
        self.turn_off_internal_command = self.addon.getSetting("turn_off_internal_command")

        self.turn_on_condition = self.addon.getSetting("turn_on_condition") == 'true'
        self.turn_on_condition_command = self.addon.getSetting("turn_on_condition_path")
        self.turn_off_condition = self.addon.getSetting("turn_off_condition") == 'true'
        self.turn_off_condition_command = self.addon.getSetting("turn_off_condition_path")

        self.suppress_wake_up = int(self.addon.getSetting("suppress_wake_up"))

    def hook_stop_player(self):
        log(["Stop player hook?",self.stop_player_on_turn_off])
        if self.stop_player_on_turn_off == False: return False
        if xbmc.Player().isPlaying() == True:
            xbmc.Player().stop()
        return True

    def hook_turn_off_action(self):
        log(["Turn off post action?", self.turn_off_action])
        if self.turn_off_action == "none": return False

        while self.scan_running():
            log(["scan running","waiting"])
            time.sleep(10)

        self.post_action_executed = True

        if self.turn_off_action == "restart":
            xbmc.executebuiltin('XBMC.RestartApp()')
        elif self.turn_off_action == "quit":
            xbmc.executebuiltin('XBMC.Quit()')
        elif self.turn_off_action == "reboot":
            xbmc.restart()
        elif self.turn_off_action == "shutdown":
            xbmc.shutdown()

        return True

    def turn_on_off_condition(self, action):
        if action == 'turn_on':
            if self.turn_on_condition == True:
                result = exec_shell_command(self.turn_on_condition_command)
                log(["Checking ON condition with result", result])
                return result == 0
        elif action == 'turn_off':
            if self.turn_off_condition == True:
                result = exec_shell_command(self.turn_off_condition_command)
                log(["Checking OFF condition with result", result])
                return result == 0
        else:
            return True


    def turn_off_tv(self):
        log(["Turn OFF TV via", self.turn_off_method])

        self.turn_off_executed_at = time.time()
        self.hook_stop_player()

        if self.turn_on_off_condition("turn_off") == False: 
            log(["Turn OFF action canceled due to condition"])
            return False

        self.turn_off_executed_at = time.time()

        # do action
        if self.turn_off_method == "kodi":
            xbmc.executebuiltin('XBMC.CECStandby()')
        elif self.turn_off_method == "cec-client":
            exec_shell_command("echo 'standby 0' | " + self.cec_client_command + " -s")
        elif self.turn_off_method == "command":
            exec_shell_command(self.turn_off_command)
        elif self.turn_off_method == "internal":
            tvrc_process_settings_string("turn_off", self.turn_off_internal_command)

        self.turn_off_executed_at = time.time()
        self.hook_turn_off_action()

        return True

    def turn_on_tv(self):
        log(["Turn ON TV via", self.turn_on_method])

        if self.turn_on_off_condition("turn_on") == False: 
            log(["Turn ON action canceled due to condition"])
            return False

        # do action
        if self.turn_on_method == "kodi":
            xbmc.executebuiltin('XBMC.CECActivateSource()')
        elif self.turn_on_method == "cec-client":
            exec_shell_command("echo 'on 0' | " + self.cec_client_command + " -s")
        elif self.turn_on_method == "command":
            exec_shell_command(self.turn_on_command)
        elif self.turn_on_method == "internal":
            tvrc_process_settings_string("turn_on", self.turn_on_internal_command)


        return True

    def execute_command(self, event):
        log(["Execute command on EVENT", event])

        if event == "screen_saver_activated_target_time_ago":
            log(["Turn OFF TV target time?", self.turn_off_activated])
            if self.turn_off_player_ones_launched == True and self.at_least_ones_player_launched == False:
                log("Player wasn't launched, skipping Turn OFF")
            else:
                self.turn_off_tv()
            
        elif event == "screen_saver_deactivated":
            self.screensaver_running = False
            if self.suppress_wake_up != 0 and (self.turn_off_executed_at + self.suppress_wake_up) > time.time():
                log("Turn off TV or stoping player should deactivate screensaver, suppressing wake up actions and activate screensaver again")
                xbmc.executebuiltin("XBMC.ActivateScreensaver()")
            elif self.post_action_executed == True:
                log("Post action executed, suppressing wake up action")
            else:
                log(["Turn ON TV on screensaver deactivated?", self.turn_on_deactivated])
                if self.turn_on_deactivated == True: self.turn_on_tv()

        elif event == "player_stared":
            self.at_least_ones_player_launched = True
            if self.turn_on_player_start == True: self.turn_on_tv()

        elif event == "screen_saver_activated": 
            self.screensaver_running = True
            if self.suppress_wake_up != 0 and (self.turn_off_executed_at + self.suppress_wake_up) > time.time():
                log("Screen saver activated by me, turn off TV not scheduled")
                self.turn_off_executed_at = 0
            else:
                self.target_time_for_execution = time.time() + (self.turn_off_after * 60)
                log(["Turn off TV scheduled on", time.ctime(self.target_time_for_execution)])

        # screen_saver_activated
        # screen_saver_deactivated
        # screen_saver_activated_target_time_ago
        # player_stared

    def check_monitor(self, event = None):
        if self.monitor == None: return False
        if event != None: self.execute_command(event)

        if self.screensaver_running == True and self.target_time_for_execution > 0 and self.target_time_for_execution <= time.time():
            self.target_time_for_execution = 0
            self.execute_command("screen_saver_activated_target_time_ago")

    def scan_running(self):
        #check if any type of scan is currently running
        if(xbmc.getCondVisibility('Library.IsScanningVideo') or xbmc.getCondVisibility('Library.IsScanningMusic')):
            return True
        else:
            return False
