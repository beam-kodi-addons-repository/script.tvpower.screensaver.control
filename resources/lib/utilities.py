import xbmc
import subprocess, exceptions, traceback

def log(message, log_level=xbmc.LOGNOTICE):
    if log_level == "info": log_level = xbmc.LOGNOTICE
    if log_level == "debug": log_level = xbmc.LOGDEBUG
    if log_level == "error": log_level = xbmc.LOGERROR
    if log_level == "warn": log_level = xbmc.LOGWARNING
    xbmc.log("### TV power controller: " + str(message), level=log_level)

def exec_shell_command(command):
    try:
        # proc = subprocess.Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
        # out, err = proc.communicate()
        # return_code = proc.returncode
        # return return_code, out, err
        return_code = subprocess.call(command, shell=True)
    except Exception, err:
        log(traceback.format_exc(), log_level="error")
        return_code = 0 # TODO: return error value and add setting to caller how to handle errors
    return return_code
