import xbmc
import xbmcaddon
import json
from random import shuffle
import sys
import os

# define some stuff
__settings__   = xbmcaddon.Addon(id='script.shuffleboard')
__cwd__        = __settings__.getAddonInfo('path')
CHANNEL_DEF_FILE = os.path.join(__cwd__, 'resources', 'channels', 'main.json')

def executeLogCommand(cmd):
    """
    Helper for executing commands, with logging if debug mode on.
    """
    raw_req = json.dumps(cmd)
    xbmc.log("JSONRPC request: {}".format(raw_req), xbmc.LOGDEBUG)

    raw_resp = xbmc.executeJSONRPC(raw_req)
    xbmc.log("JSONRPC result: {}".format(raw_resp), xbmc.LOGDEBUG)

    return json.loads(raw_resp)

# Get the name of the show to use from the channel file
file_handle = open(CHANNEL_DEF_FILE, 'r')
str_data = file_handle.read()
channel_data = json.loads(str_data)
show_name = channel_data["show"]

# Get the tvshow definition from Kodi library
ShowQueryCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetTVShows",
    "properties": ["title"],
    "sort": { "order": "ascending", "method": "label" },
    "id": "libTvShow"
}
showsResult = executeLogCommand(ShowQueryCmd)
shows = showsResult["result"]["tvshows"]
current_show = next(show for show in shows if show["label"] == show_name)

# Get all episodes of selected show from Kodi library, and shuffle them
epListCmd = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetEpisodes",
    "params": {"tvshowid": current_show["tvshowid"]},
    "id": "epList"
}
epsResult = executeLogCommand(epListCmd)
current_eps = epsResult["result"]["episodes"]
ep_ids = [ep["episodeid"] for ep in current_eps]
shuffle(ep_ids)

# Play the first in list of items we've just created
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

# Get the currently playing playlist from Kodi
playlistsCmd = {
    "jsonrpc": "2.0",
    "method": "Playlist.GetPlaylists",
    "id": "getPlaylists"
}
playlistsResult = executeLogCommand(playlistsCmd)
videoPlaylist = next(playlist for playlist in playlistsResult["result"] if playlist["type"] == "video")

# Get the currently active video player from Kodi
activePlayersCmd = {
    "jsonrpc": "2.0",
    "method": "Player.GetActivePlayers",
    "id": "getActivePlayers"
}
activePlayersResult = executeLogCommand(activePlayersCmd)
activeVideoPlayer = next(player for player in activePlayersResult["result"] if player["type"] == "video")

# Error out if things aren't going according to plan
if not activeVideoPlayer and videoPlaylist:
    xbmc.log("error! Could not get a single video player and playlist! Exiting...")
    sys.exit()

# Add the remainder of our shuffled items to the current playlist
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

# Tell the active player to turn on 'Reapeat All" mode
repeatAllCmd = {
    "jsonrpc": "2.0",
    "method": "Player.SetRepeat",
    "params": {
        "playerid": activeVideoPlayer,
        "repeat": "all",
    },
    "id": "repeatAll"
}
repeatAllResult = executeLogCommand(repeatAllCmd)
