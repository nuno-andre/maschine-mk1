from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_CC_TYPE
from _Framework.SliderElement import SliderElement
from _Framework.ButtonElement import ButtonElement

from .MIDI_Map import debug_out
from .KnobSection import KnobSection
from .MonoNavSection import MonoNavSection
from .Maschine import Maschine
from .buttons import MonoGatedButton, PadButton

# import time
# import Live
# from _Framework.ControlSurface import ControlSurface, _scheduled_method
# from _Framework.InputControlElement import *
# from _Framework.ButtonElement import ON_VALUE, OFF_VALUE
# from _Framework.ButtonMatrixElement import ButtonMatrixElement
# from MaschineMixerComponent import MaschineMixerComponent


class MaschineMk1(Maschine):
    """Control Script for Maschine Studio.
    """
    __module__ = __name__

    def __init__(self, c_instance):
        super().__init__(c_instance)

    def create_pad_button(self, scene_index, track_index, color_source):
        return PadButton(True, 0, scene_index, track_index)

    def create_gated_button(self, identifier, hue):
        return MonoGatedButton(True, MIDI_CC_TYPE, identifier)

    def _init_maschine(self):
        self._jogwheel = KnobSection(self._modeselect, self._editsection)
        self._note_repeater.registerKnobHandler(self._jogwheel)
        self._mixer.set_touch_mode(2)
        self._device_component.set_touch_mode(2)
        self._set_up_machine_knobs()
        self._nav_section = MonoNavSection(self._modeselect)

    def _set_up_machine_knobs(self):
        master_track = self.song().master_track
        self.prehear_knob = SliderElement(MIDI_CC_TYPE, 0, 43)
        self.prehear_knob.connect_to(self.song().master_track.mixer_device.cue_volume)
        self._stop_tap_button = ButtonElement(True, MIDI_CC_TYPE, 1, 111)
        self._do_combined_stop_tap.subject = self._stop_tap_button
        self._undo__redo_button = ButtonElement(True, MIDI_CC_TYPE, 2, 85)
        self._do_undo_redo.subject = self._undo__redo_button

    @subject_slot('value')
    def _do_combined_stop_tap(self, value):
        if value:
            if self.isShiftDown():
                self.song().stop_all_clips(0)
            else:
                self.song().stop_all_clips(1)

    @subject_slot('value')
    def _do_undo_redo(self, value):
        if value:
            if self.isShiftDown():
                if self.song().can_redo == 1:
                    self.song().redo()
                    self.show_message(str('REDO'))
            elif self.song().can_undo == 1:
                self.song().undo()
                self.show_message(str('UNDO'))

    def _final_init(self):
        debug_out('########## LIVE 11 MASCHINE Mk1 (UNOFFICIAL) V 2.01 #############')

    def is_monochrome(self):
        return True

    def _click_measure(self):
        pass

    def preferences_name(self):
        return 'MaschineMk1'

    def apply_preferences(self):
        super().apply_preferences()
        pref_dict = self._pref_dict
        self._session.set_step_advance(1)

    def store_preferences(self):
        super().store_preferences()

    def update_display(self):
        with self.component_guard():
            with self._is_sending_scheduled_messages():
                self._task_group.update(0.1)
            self._modeselect.notify_mono(self.blink_state)
            self.blink_state = (self.blink_state + 1) % 4
            self.display_task.tick()
            self.update_undo_redo(False)
