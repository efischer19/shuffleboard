from common import *
from utils import (
    executeLogCommand
)
import json
from random import shuffle

class Channel(object):
    """
    An abstraction around a playlist as defined on disk.
    """

    def __init__(self, filename):
        self.loadFromDisk(filename)

    def loadFromDisk(self, filename):
        file_handle = open(filename, 'r')
        str_data = file_handle.read()
        self.data = json.loads(str_data)
        self.loadPlaylist()

    def loadPlaylist(self):
        # Only handling tv shows right now
        if self.data and self.data.get('type', None) == TYPE_TV_SHOW:
            self.loadEpisodes()

class TvShowChannel(Channel):
    _tvshowid = None
    _label = None

    def __init__(self, filename):
        super(TvShowChannel, self).__init__(filename)

    @property
    def label(self):
        if not self._label:
            self._label = self.data.get('show', None)
        return self._label

    @property
    def tvshowid(self):
        if not self._tvshowid:
            # TODO: write tvshowid on save as well
            loaded_id = self.data.get('tvshowid', None)
            if loaded_id is not None:
                self._tvshowid = loaded_id
            elif not self.label:
                # TODO: add error handling here once it exists
                return
            else:
                showsResult = executeLogCommand(GET_ALL_SHOWS_COMMAND)
                shows = showsResult["result"]["tvshows"]
                current_show = next(show for show in shows if show["label"] == self.label)
                self._tvshowid = current_show['tvshowid']
        return self._tvshowid

    @property
    def shuffle(self):
        return self.data and self.data.get('mode', None) == 'shuffle'

    @property
    def playlist(self):
        if not self._playlist:
            self.loadEpisodes()
        return self._playlist

    def loadEpisodes(self):
        epListCmd = {
            "jsonrpc": "2.0",
            "method": "VideoLibrary.GetEpisodes",
            "params": {"tvshowid": self.tvshowid},
            "id": "epList"
        }
        epsResult = executeLogCommand(epListCmd)
        current_eps = epsResult["result"]["episodes"]
        self._playlist = [('episodeid', ep["episodeid"]) for ep in current_eps]
        if self.shuffle:
            shuffle(self._playlist)
