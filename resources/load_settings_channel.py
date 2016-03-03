from common import *
from channel import (
    TvShowChannel,
)

# Get current channel as defined in settings
currentChannel = TvShowChannel(CURRENT_CHANNEL)

# Load its values into the other settings
SETTINGS.setSetting('show', currentChannel.label)
SETTINGS.setSetting('shuffle', 'true' if currentChannel.shuffle else 'false')
SETTINGS.setSetting('filename', SETTINGS.getSetting('current_channel'))
