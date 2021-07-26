import requests
from datetime import datetime

class SteamApi:

    def _steam2IdTo64bitSteamId(self, id_string):
        """STEAM_1:1:23227168 -> 64-bit representation
        See: https://developer.valvesoftware.com/wiki/SteamID
        """
        _, y, z = id_string.split(':')
        individual_steam_account_base_id = 76561197960265728
        steamid64 = individual_steam_account_base_id + int(y) + (int(z) * 2)
        return steamid64

    api_base_url = "https://api.steampowered.com/ISteamUser/"

    def __init__(self, steam_api_key):
        self.key = steam_api_key


    def GetPlayerSummary(self, steam2id):
        steamid = self._steam2IdTo64bitSteamId(steam2id)
        try:
            url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={self.key}&format=json&steamids={steamid}"
            r = requests.get(url)
            return r.json()['response']['players'][0]
        except Exception as e:
            print("GetPlayerSummary failed:", e)
            print("Request was done to:", url)
            return {}

    def GetNumberOfFriends(self, steam2id):
        steamid = self._steam2IdTo64bitSteamId(steam2id)
        url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={self.key}&format=json&steamid={steamid}"
        r = requests.get(url)
        num_friends = -1
        try:
            num_friends = len(r.json()['friendslist']['friends'])
        except:
            pass
        return num_friends

    def GetPlayerBans(self, steam2id):
        steamid = self._steam2IdTo64bitSteamId(steam2id)
        url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v0001/?key={self.key}&format=json&steamids={steamid}"
        r = requests.get(url)
        return r.json()['players'][0]

    def GetNumHours(self, steam2id):
        steamid = self._steam2IdTo64bitSteamId(steam2id)
        url = f"https://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=624820&key={self.key}&format=json&steamid={steamid}"
        r = requests.get(url)
        return r.json()

