import xbmcaddon
import os

"""
This file is intended to be accessed everywhere in shuffleboard via
'from commom import *', so all variables should be of form __foo__ or FOO.

This is to allow for ease of use, without cluttering up namespaces. If a
variable is not needed in all files, it should not be declared in this file.
If a piece of code thinks it needs a new __foo__ or FOO variable, it should
probably be declared here instead.
"""

# Contextual underscore variables
__settings__   = xbmcaddon.Addon(id='script.shuffleboard')
__cwd__        = __settings__.getAddonInfo('path')

# Constants
DEFAULT_CHANNEL = os.path.join(__cwd__, 'resources', 'channels', 'main.json')
TYPE_TV_SHOW = 'tvshow'

# Common API commands
GET_ALL_SHOWS_COMMAND = {
    "jsonrpc": "2.0",
    "method": "VideoLibrary.GetTVShows",
    "properties": ["title"],
    "sort": { "order": "ascending", "method": "label" },
    "id": "libTvShow"
}
