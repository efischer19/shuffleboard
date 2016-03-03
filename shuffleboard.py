from resources.utils import (
    playPlaylist,
)
from resources.channel import (
    TvShowChannel,
)
from resources.common import *

currentChannel = TvShowChannel(CURRENT_CHANNEL)
playPlaylist(currentChannel.playlist)
