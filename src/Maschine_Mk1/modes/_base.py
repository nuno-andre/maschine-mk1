from _Framework.CompoundComponent import CompoundComponent

from ..MIDI_Map import OTHER_MODE

# import Live
# from _Framework.SubjectSlot import subject_slot
# from _Framework.ControlSurfaceComponent import ControlSurfaceComponent
# from _Framework.ControlSurface import ControlSurface, _scheduled_method
# from _Framework.InputControlElement import *
# from _Framework.ButtonElement import ButtonElement
# from MIDI_Map import *
# from PadScale import *
# from MaschineSessionComponent import MaschineSessionComponent


def find_drum_device(track):
    for device in track.devices:
        if device.can_have_drum_pads:
            return device


class MaschineMode(CompoundComponent):
    __module__ = __name__

    def __init__(self, button_index=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._active = False
        self._alternate_mode = None
        self.button_index = button_index

    def get_color(self, value, column_index, row_index):
        pass

    def notify(self, blink_state):
        pass

    def notify_mono(self, blink_state):
        pass

    def navigate(self, dir, modifier, alt_modifier=False):
        pass

    def unbind(self):
        pass

    def is_lock_mode(self):
        return True

    def enter(self):
        raise NotImplementedError(self.__class__)

    def exit(self):
        raise NotImplementedError(self.__class__)

    def enter_edit_mode(self, type):
        pass

    def exit_edit_mode(self, type):
        pass

    def get_mode_id(self):
        return OTHER_MODE

    def enter_clear_state(self):
        pass

    def exit_clear_state(self):
        pass

    def disconnect(self):
        super().disconnect()

    def fitting_mode(self, track):
        return self

    def set_alternate_mode(self, mode):
        self._alternate_mode = mode

    def isShiftDown(self):
        return self.canonical_parent.isShiftDown()

    def handle_push(self, value):
        pass

    def refresh(self):
        pass

    def _device_changed(self):
        pass

    def update(self):
        pass
