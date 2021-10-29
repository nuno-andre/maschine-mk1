from _Framework.CompoundComponent import CompoundComponent
from _Framework.ToggleComponent import ToggleComponent

# import Live
# from MIDI_Map import *


class MaschineTransport(CompoundComponent):
    """Class encapsulating all functions in Live's transport section.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        song = self.song()
        (
            self._automation_toggle,
            self._re_enable_automation_toggle,
            self._delete_automation,
            self._arrangement_overdub_toggle,
            self._back_to_arrange_toggle,
        ) = self.register_components(
            ToggleComponent('session_automation_record', song),
            ToggleComponent('re_enable_automation_enabled', song, read_only=True),
            ToggleComponent('has_envelopes', None, read_only=True),
            ToggleComponent('arrangement_overdub', song),
            ToggleComponent('back_to_arranger', song),
        )

    def set_back_arrange_button(self, button):
        self._back_to_arrange_toggle.set_toggle_button(button)

    def set_session_auto_button(self, button):
        self._automation_toggle.set_toggle_button(button)

    def set_arrangement_overdub_button(self, button):
        self._arrangement_overdub_toggle.set_toggle_button(button)

    def update(self):
        pass
