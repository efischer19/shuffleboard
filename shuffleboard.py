import xbmcaddon
import xbmcgui
import xbmc
import json

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

playListCmd = {
    "jsonrpc": "2.0",
    "method": "Playlist.GetPlaylists",
    "id": "play_happy_endings"
}
raw_resp = xbmc.executeJSONRPC(json.dumps(playListCmd))
xbmc.log(raw_resp, xbmc.LOGDEBUG)

playCmd = {
    "jsonrpc": "2.0",
    "params": {
        "item": {
            "playlistid": 1
        },
        "options": {
            "repeat": "all",
            "shuffled": True
        }
    },
    "method": "Player.Open",
    "id": "play_happy_endings"
}
raw_cmd = json.dumps(playCmd)
xbmc.log(raw_cmd, xbmc.LOGDEBUG)
raw_resp = xbmc.executeJSONRPC(raw_cmd)
xbmc.log(raw_resp, xbmc.LOGDEBUG)
