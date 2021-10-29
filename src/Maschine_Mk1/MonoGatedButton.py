from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement

# import time
# import Live
# from MIDI_Map import *


class MonoGatedButton(ButtonElement):
    """Special button class that has on, off, color an can also be a
    None Color Button.
    """
    __module__ = __name__

    def __init__(self, is_momentary, midi_type, identifier):
        super().__init__(is_momentary, midi_type, 0, identifier)
        self._msg_identifier = identifier
        self.last_value = 0
        self.hue = 0

    def set_color(self, hue):
        self.send_value(127, True)

    def send_color(self, value):
        self.send_value(value)

    def switch_off(self):
        self.send_value(0)

    def activate(self):
        pass

    def update(self):
        pass

    def turn_on(self):
        self.send_value(127, True)

    def turn_off(self):
        self.send_value(0, True)

    def disconnect(self):
        InputControlElement.disconnect(self)
