import xbmcaddon
import xbmcgui
import xbmc
import json
from random import shuffle

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

ShowQueryCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetTVShows",
    "properties": ["title"],
    "sort": { "order": "ascending", "method": "label" },
    "id": "libTvShow"
}
raw_resp = xbmc.executeJSONRPC(json.dumps(ShowQueryCmd))
xbmc.log(raw_resp, xbmc.LOGDEBUG)
resp = json.loads(raw_resp)
shows = resp["result"]["tvshows"]
happy_endings = next(show for show in shows if show["label"] == "Happy Endings")

xbmc.log("Got some shows!", xbmc.LOGDEBUG)
xbmc.log("{} of them, to be exact!".format(len(shows)), xbmc.LOGDEBUG)
xbmc.log("Here's the response: {}".format(happy_endings), xbmc.LOGDEBUG)
xbmc.log("Trying to start now...", xbmc.LOGDEBUG)

epListCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetEpisodes",
    "params": {"tvshowid": happy_endings["tvshowid"]},
    "id": "epList"
}
raw_resp = xbmc.executeJSONRPC(json.dumps(epListCmd))
xbmc.log(raw_resp, xbmc.LOGDEBUG)
HE_eps = json.loads(raw_resp)["result"]["episodes"]
ep_ids = [ep["episodeid"] for ep in HE_eps]
shuffle(ep_ids)

playCmd = {
    "jsonrpc": "2.0",
    "params": {
        "item": {
            "episodeid": ep_ids[0]
        },
    },
    "method": "Player.Open",
    "id": "play_episode"
}
raw_cmd = json.dumps(playCmd)
xbmc.log(raw_cmd, xbmc.LOGDEBUG)
raw_resp = xbmc.executeJSONRPC(raw_cmd)
xbmc.log(raw_resp, xbmc.LOGDEBUG)
