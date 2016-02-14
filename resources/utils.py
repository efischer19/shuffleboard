"""
Utility functions for use in shuffleboard.

Will be further organized as the file grows.
"""
import sys
import json
import xbmc

def executeLogCommand(cmd):
    """
    Helper for executing commands, with logging if debug mode on.
    """
    raw_req = json.dumps(cmd)
    xbmc.log("JSONRPC request: {}".format(raw_req), xbmc.LOGDEBUG)

    raw_resp = xbmc.executeJSONRPC(raw_req)
    xbmc.log("JSONRPC result: {}".format(raw_resp), xbmc.LOGDEBUG)

    return json.loads(raw_resp)

def playPlaylist(playlist):
    # Play the first item
    playCmd = {
        "jsonrpc": "2.0",
        "params": {
            "item": {
                playlist[0][0]: playlist[0][1]
            },
        },
        "method": "Player.Open",
        "id": "openPlayer"
    }
    playResult = executeLogCommand(playCmd)
    playlist.remove(playlist[0])

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
    activeVideoPlayer = next(player["playerid"] for player in activePlayersResult["result"] if player["type"] == "video")

    # Error out if things aren't going according to plan
    if not activeVideoPlayer and videoPlaylist:
        xbmc.log("error! Could not get a single video player and playlist! Exiting...")
        sys.exit()

    # Add the remainder of our items to the current playlist
    addAllBatchCmd = [
        {
            "jsonrpc": "2.0",
            "method": "Playlist.Add",
            "id": "queueEp{}".format(item[1]),
            "params": {
                "playlistid": videoPlaylist["playlistid"],
                "item": {
                    item[0]: item[1]
                }
            }
        } for item in playlist
    ]
    addAllEpsResult = executeLogCommand(addAllBatchCmd)

    # Tell the active player to turn on 'Repeat All" mode
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
