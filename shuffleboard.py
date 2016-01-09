import xbmcaddon
import xbmcgui
import xbmc
import json

addon       = xbmcaddon.Addon()
addonname   = addon.getAddonInfo('name')

ShowQueryCmd = '{"jsonrpc": "2.0", "method": "VideoLibrary.GetTVShows", "properties": ["title"], "sort": { "order": "ascending", "method": "label" }, "id": "libTvShow" }'
shows = xbmc.executeJSONRPC(ShowQueryCmd)

xbmc.log("Got some shows!", xbmc.LOGDEBUG)
xbmc.log("{} of them, to be exact!".format(len(shows)), xbmc.LOGDEBUG)
xbmc.log("Here's the response: {}".format(json.loads(shows)), xbmc.LOGDEBUG)

xbmcgui.Dialog().ok(addonname, shows)
