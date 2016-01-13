import xbmc
import json
from random import shuffle
import sys

def executeLogCommand(cmd):
    raw_req = json.dumps(cmd)
    xbmc.log("JSONRPC request: {}".format(raw_req), xbmc.LOGDEBUG)

    raw_resp = xbmc.executeJSONRPC(raw_req)
    xbmc.log("JSONRPC result: {}".format(raw_resp), xbmc.LOGDEBUG)

    return json.loads(raw_resp)

ShowQueryCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetTVShows",
    "properties": ["title"],
    "sort": { "order": "ascending", "method": "label" },
    "id": "libTvShow"
}
showsResult = executeLogCommand(ShowQueryCmd)
shows = showsResult["result"]["tvshows"]
happy_endings = next(show for show in shows if show["label"] == "Happy Endings")

epListCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetEpisodes",
    "params": {"tvshowid": happy_endings["tvshowid"]},
    "id": "epList"
}
epsResult = executeLogCommand(epListCmd)
HE_eps = epsResult["result"]["episodes"]
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
    "id": "openPlayer"
}
playResult = executeLogCommand(playCmd)
ep_ids.remove(ep_ids[0])

playlistsCmd = {
    "jsonrpc": "2.0",
    "method": "Playlist.GetPlaylists",
    "id": "getPlaylists"
}
playlistsResult = executeLogCommand(playlistsCmd)
videoPlaylist = next(playlist for playlist in playlistsResult["result"] if playlist["type"] == "video")

activePlayersCmd = {
    "jsonrpc": "2.0",
    "method": "Player.GetActivePlayers",
    "id": "getActivePlayers"
}
activePlayersResult = executeLogCommand(activePlayersCmd)
activeVideoPlayer = next(player for player in activePlayersResult["result"] if player["type"] == "video")

if not activeVideoPlayer and videoPlaylist:
    xbmc.log("error! Could not get a single video player and playlist! Exiting...")
    sys.exit()

addAllEpsBatchCmd = [
    {
        "jsonrpc": "2.0",
        "method": "Playlist.Add",
        "id": "queueEp{}".format(ep_id),
        "params": {
            "playlistid": videoPlaylist["playlistid"],
            "item": {
                "episodeid": ep_id
            }
        }
    } for ep_id in ep_ids
]
addAllEpsResult = executeLogCommand(addAllEpsBatchCmd)
