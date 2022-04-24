from utilities import log
from tvrc_baseclass import BaseTVRemoteControl
from tvrc_samsung_pre_2016 import TVRC_SamsungPre2016
import traceback

for subclass in BaseTVRemoteControl.__subclasses__():
    log(["Imported TVRC", subclass.ident()], log_level="debug")

def tvrc_process_settings_string(action, settings_string):
    settings_array = settings_string.split("|")
    tvrc_name = settings_array.pop(0)
    tvrc_params = settings_array
    
    if tvrc_name in globals():
        tvrc_obj = globals()[tvrc_name](*tvrc_params)
    else:
        log(["TVRC module not found", tvrc_name])
        return False

    try:
        if action == "turn_off":
            tvrc_obj.turn_off()
        elif action == "turn_on":
            tvrc_obj.turn_on()
        else:
            log(["Unknown TVRC action", action], "warn")
            return False
    except Exception as err:
        log(traceback.format_exc(), log_level="error")
        return False

    return True