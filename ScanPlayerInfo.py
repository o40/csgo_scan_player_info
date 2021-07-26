from Tailer.Tailer import Tailer
from SteamApi.SteamApi import SteamApi
from CsGoCommunicator.CsGoCommunicator import CsGoCommunicator

import re
import json
from datetime import datetime

def _get_steam2_id_from_string(console_log_string):
    prog = re.compile(r"STEAM_(\d):(\d):(\d*)")
    result = prog.search(console_log_string)
    if result:
        return result.group()
    return None


def _public_profile(summary):
    return summary['communityvisibilitystate'] == 3


def _get_bans_info(bans):
    num_vac_bans = bans['NumberOfVACBans']
    days_since_last_ban = bans['DaysSinceLastBan']

    if num_vac_bans == 0:
        return "has no VAC bans"
    else:
        return f"has {num_vac_bans} VAC ban ({days_since_last_ban} days ago)"

def _get_account_age_in_years(summary):
    time_created = datetime.utcfromtimestamp(summary['timecreated'])
    time_now = datetime.now()
    return (time_now - time_created).days


def _get_summary_string(summary, numfriends, bans):
    name = summary['personaname']


    if _public_profile(summary):
        country_code = summary.get('loccountrycode', '?')

        if numfriends < 0:
            numfriends = '?'

        days = _get_account_age_in_years(summary)
        ban_info = _get_bans_info(bans)

        return f"{name} ({country_code}) created steam account {days} days ago, has {numfriends} friends, and {ban_info}"
    else:
        return f"{name} has a private profile"


def _get_settings():
    with open("settings.json") as settings_file:
        settings = json.load(settings_file)
        return settings['path'], settings['key'], settings['command']


console_log_path, steam_api_key, command = _get_settings()

sa = SteamApi(steam_api_key)
com = CsGoCommunicator(command)

for line in Tailer.Tail(console_log_path):
    steam2id = _get_steam2_id_from_string(line)
    if steam2id:
        try:
            player_summary_json = sa.GetPlayerSummary(steam2id)
            player_num_friends = sa.GetNumberOfFriends(steam2id)
            player_bans = sa.GetPlayerBans(steam2id)
            summary_string = _get_summary_string(player_summary_json, player_num_friends, player_bans)
            print(summary_string)
            com.SendMessage(summary_string)
        except Exception as e:
            print("Failed to parse", steam2id)
            print(e)
            pass