from _Framework.ButtonElement import ButtonElement
from _Framework.InputControlElement import InputControlElement

# import Live
# from _Framework.ButtonElement import *
# from _Framework.InputControlElement import *
# from MIDI_Map import *


class StateButton(ButtonElement):
    """Special button class that can be configured with custom on- and
    off-values.
    """
    __module__ = __name__

    def __init__(self, is_momentary, msg_type, channel, identifier):
        super().__init__(is_momentary, msg_type, channel, identifier)
        self._is_enabled = True
        self._is_notifying = False
        self._force_next_value = False

    def turn_off(self):
        self.send_value(0, True)

    def turn_on(self):
        self.send_value(127, True)

    def set_enabled(self, enabled):
        self._is_enabled = enabled

    def reset(self):
        self.send_value(0, True)

    def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
        if self._is_enabled:
            super().install_connections(
                install_translation_callback,
                install_mapping_callback,
                install_forwarding_callback,
            )
        elif self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
            install_translation_callback(
                self._msg_type,
                self._original_identifier,
                self._original_channel,
                self._msg_identifier,
                self._msg_channel,
            )


class ToggleButton(StateButton):
    __module__ = __name__

    def __init__(self, msg_type, channel, identifier):
        super().__init__(True, msg_type, channel, identifier)
        self._value = 0

    def turn_off(self):
        self._value = 0
        self.send_value(0, True)

    def turn_on(self):
        self._value = 1
        self.send_value(127, True)

    def receive_value(self, value):
        if value > 0:
            if self._value == 0:
                self._value = 1
                InputControlElement.receive_value(self, 127)
            else:
                self._value = 0
                InputControlElement.receive_value(self, 0)


# class ToggleButton(ButtonElement):
#     __module__ = __name__

#     def __init__(self, msg_type, channel, identifier):
#         super().__init__(True, msg_type, channel, identifier)
#         self._is_enabled = True
#         self._is_notifying = False
#         self._force_next_value = False
#         self._value = 0

#     def turn_off(self):
#         self._value = 0
#         self.send_value(0, True)

#     def turn_on(self):
#         self._value = 1
#         self.send_value(127, True)

#     def set_enabled(self, enabled):
#         self._is_enabled = enabled

#     def reset(self):
#         self.send_value(0, True)

#     def receive_value(self, value):
#         if value > 0:
#             if self._value == 0:
#                 self._value = 1
#                 InputControlElement.receive_value(self, 127)
#             else:
#                 self._value = 0
#                 InputControlElement.receive_value(self, 0)

#     def install_connections(self, install_translation_callback, install_mapping_callback, install_forwarding_callback):
#         if self._is_enabled:
#             super().install_connections(
#                 install_translation_callback,
#                 install_mapping_callback,
#                 install_forwarding_callback,
#             )
#         elif self._msg_channel != self._original_channel or self._msg_identifier != self._original_identifier:
#             install_translation_callback(
#                 self._msg_type,
#                 self._original_identifier,
#                 self._original_channel,
#                 self._msg_identifier,
#                 self._msg_channel,
#             )
