from _Framework.MixerComponent import MixerComponent

from .MaschineChannelStripComponent import MaschineChannelStripComponent

# import Live


class MaschineMixerComponent(MixerComponent):
    """Class encompassing several channel strips to form a mixer.
    """

    def __init__(self, num_tracks, num_returns=0, with_eqs=False, with_filters=False):
        super().__init__(num_tracks, num_returns, with_eqs, with_filters)
        self.num_tracks = num_tracks

    def set_touch_mode(self, touchchannel):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.set_touch_mode(touchchannel)

    def _create_strip(self):
        return MaschineChannelStripComponent()

    def enter_clear_mode(self):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.enter_clear()

    def exit_clear_mode(self):
        for index in range(self.num_tracks):
            strip = self.channel_strip(index)
            strip.exit_clear()

    def disconnect(self):
        super().disconnect()
