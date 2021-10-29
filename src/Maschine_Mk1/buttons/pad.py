from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS, MIDI_NOTE_TYPE

from ..MIDI_Map import CLIPNOTEMAP, NON_FEEDBACK_CHANNEL, OFF_COLOR

# import time
# import Live
# from _Framework.InputControlElement import *
# from _Framework.ButtonElement import *
# from MIDI_Map import *


class PadButton(ButtonElement):
    """Colored Maschine Pads.
    """
    __module__ = __name__

    def __init__(self, is_momentary, channel, row_index, column_index):
        super().__init__(is_momentary, MIDI_NOTE_TYPE, channel, CLIPNOTEMAP[row_index][column_index])
        self._is_enabled = True
        self._row_index = row_index
        self._column_index = column_index
        self.last_value = None
        self.blink_state = 0

    def get_identifier(self):
        return self._msg_identifier

    def reset(self):
        self.last_value = None

    def turn_off(self):
        if self.last_value != 0 or self.last_value == None:
            self.last_value = 0
            self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, 0))

    def turn_on(self):
        if not self.last_value:
            self.last_value = 127
            self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, 127))

    def refresh(self):
        if self.last_value:
            self.send_value(self.last_value, True)

    def blink_value(self):
        return self.blink_state

    def set_send_note(self, note):
        if 0 <= note < 128 and isinstance(note, int):
            self._msg_identifier = note
            if not self._is_enabled:
                self.canonical_parent._translate_message(
                    self._msg_type,
                    self._original_identifier,
                    self._original_channel,
                    self._msg_identifier,
                    self._msg_channel,
                )

    def set_to_notemode(self, notemode):
        self._is_enabled = not notemode
        if notemode:
            self.set_channel(0)
            self._is_being_forwarded = False
        else:
            self.set_channel(NON_FEEDBACK_CHANNEL)
            self._is_being_forwarded = True

    def send_value(self, value, force_send=False):
        assert value != None
        assert isinstance(value, int)
        assert value in range(128)
        if force_send or self._is_being_forwarded:
            self.send_c_midi(value, True)

    def send_color_direct(self, color):
        scolor = color == None and OFF_COLOR or color
        self.send_c_midi(scolor[3])

    def send_c_midi(self, value, force=False):
        if self.last_value != value or force:
            self.last_value = value
            self.send_midi((MIDI_NOTE_ON_STATUS, self._original_identifier, value))

    def disconnect(self):
        super().disconnect()
        self._is_enabled = None
        self._report_input = None
        self._column_index = None
        self._row_index = None
