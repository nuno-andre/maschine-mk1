from _Framework.SubjectSlot import subject_slot
from _Framework.InputControlElement import MIDI_NOTE_OFF_STATUS, MIDI_NOTE_ON_STATUS

from ._base import MaschineMode, find_drum_device
from ..MIDI_Map import AUTO_NAME, DEFAULT_DRUM_COLOR, PAD_MODE, PAD_TRANSLATIONS

# import re
# from itertools import imap
# from warnings import onceregistry
# import Live
# from _Framework.Util import find_if, clamp
# from _Framework.ButtonElement import *
# from _Framework.ControlSurface import ControlSurface, _scheduled_method
# from _Framework.InputControlElement import *
# from MIDI_Map import *


def color_by_name(name):
    for match in AUTO_NAME:
        if match[0].search(name):
            return match[1]

    return DEFAULT_DRUM_COLOR


class DrumPad:

    def __init__(self, index, *args, **kwargs):
        self.index = index
        self._color = ((0, 100, 20), (0, 127, 127))
        self.selected = False
        self._pad = None
        self._button = None

    def set_color(self, color):
        self._color = color

    def set_pad(self, pad):
        self._pad = pad

    def set_button(self, button):
        self._button = button
        button._pad = None

    def send_color(self):
        if self.selected:
            self._button.send_color_direct(self._color[1])
        else:
            self._button.send_color_direct(self._color[0])

    def get_color(self):
        return self._color[1 if self.selected else 0]


class DrumMode(MaschineMode):
    __subject_events__ = 'pressed_pads',

    def __init__(self, button_index, monochrome=False, *args, **kwargs):
        super().__init__(button_index, *args, **kwargs)
        self.track = None
        self.device = None
        self._is_monochrome = monochrome
        if monochrome:
            self._update_pad_edit = self._update_pad_edit_mono
        else:
            self._update_pad_edit = self._update_pad_edit_color
        self._visible_drum_pad_slots = None
        self._visible_drum_pads = None
        self._pads = tuple(DrumPad(i) for i in range(16))
        self._selected_pad = None
        self._in_edit_mode = False
        self._editmode = None
        if self.canonical_parent.is_monochrome():
            self.pad_to_color = self.__pad_to_onoff
        else:
            self.pad_to_color = self.__pad_to_color

    def set_edit_mode(self, editmode):
        self._editmode = editmode

    def get_color(self, value, column, row):
        indx = value != 0 and 1 or 0  # TODO
        note_index = row * 4 + column
        return self._pads[note_index].get_color()

    def get_mode_id(self):
        return PAD_MODE

    def __pad_to_onoff(self, pad):
        if pad and len(pad.chains):
            return ((0, 0, 0, 1, 0), (0, 0, 0, 1, 0))

        return ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0))

    def __pad_to_color(self, pad):
        if pad:
            chains = pad.chains
            if len(chains) == 0:
                return ((0, 0, 1), (0, 0, 127))

            name = pad.name
            return color_by_name(name)

        return ((0, 90, 70), (0, 127, 127))

    def navigate(self, dir_, modifier, alt_modifier=False):
        if self.device and self.device.view:
            self.device.view.drum_pads_scroll_position = max(
                0, min(28, self.device.view.drum_pads_scroll_position + dir_))

    def enter(self):
        self._active = True
        self.assign_track_device()
        self._in_edit_mode = False
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                note_index = row * 4 + column
                pad_index = (3 - row) * 4 + column
                pad = self._pads[pad_index]
                button.set_to_notemode(True)
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_ON_STATUS, button.get_identifier())] = button
                self.canonical_parent._forwarding_registry[(MIDI_NOTE_OFF_STATUS, button.get_identifier())] = button
                button.set_send_note(PAD_TRANSLATIONS[note_index][2])
                button.send_color_direct(pad.get_color())

        self.track = self.song().view.selected_track
        self._on_name_changed.subject = self.device.view.selected_drum_pad

    def _get_note_set(self):
        in_notes = set()
        cs = self.song().view.highlighted_clip_slot
        if cs.has_clip and cs.clip.is_midi_clip:
            notes = cs.clip.get_notes(0.0, 0, cs.clip.length, 127)
            for note in notes:
                in_notes.add(note[0])

        return in_notes

    def _update_pad_edit_color(self, pad, in_notes):
        if pad._pad.note in in_notes:
            pad._button.send_color_direct(pad._color[1])
        else:
            pad._button.send_color_direct(pad._color[0])

    def _update_pad_edit_mono(self, pad, in_notes):
        if pad._pad.note in in_notes:
            pad._button.send_value(127, True)
        else:
            pad._button.send_value(0, True)

    @subject_slot('notes')
    def _on_notes_changed(self):
        cs = self.song().view.highlighted_clip_slot
        if self._in_edit_mode:
            if cs.has_clip and cs.clip.is_midi_clip:
                in_notes = set()
                notes = cs.clip.get_notes(0.0, 0, cs.clip.length, 127)
                for note in notes:
                    in_notes.add(note[0])

                for pad in self._pads:
                    self._update_pad_edit(pad, in_notes)

    def _action_clear(self, value, button):
        if value > 0:
            pad = self._pads[(button.get_identifier() - 12)]
            self._editmode.edit_note(pad._pad.note)

    def enter_clear_state(self):
        cs = self.song().view.highlighted_clip_slot
        in_notes = set()

        if cs.has_clip and cs.clip.is_midi_clip:
            clip = cs.clip
            notes = clip.get_notes(0.0, 0, clip.length, 127)
            self._on_notes_changed.subject = clip
            for note in notes:
                in_notes.add(note[0])
        else:
            self._on_notes_changed.subject = None

        self._in_edit_mode = True
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                note_index = row * 4 + column  # TODO
                pad_index = (3 - row) * 4 + column
                pad = self._pads[pad_index]
                self._update_pad_edit(pad, in_notes)
                button.set_to_notemode(False)
                button.add_value_listener(self._action_clear, True)

    def exit_clear_state(self):
        self._in_edit_mode = False
        self._on_notes_changed.subject = None
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                note_index = row * 4 + column
                pad_index = (3 - row) * 4 + column
                pad = self._pads[pad_index]
                button.set_to_notemode(True)
                button.send_color_direct(pad.get_color())
                button.remove_value_listener(self._action_clear)

    def update_pads(self):
        if self._active:
            if self._in_edit_mode:
                in_notes = self._get_note_set()
                for pad in self._pads:
                    self._update_pad_edit(pad, in_notes)

            else:
                for dpad in self._pads:
                    dpad.send_color()

    def refresh(self):
        if self._active:
            for dpad in self._pads:
                dpad._button.reset()
                dpad.send_color()

    def assign_pads(self):
        self._visible_drum_pads = None
        self._selected_pad = None
        if self.device:
            self._visible_drum_pads = self.device.visible_drum_pads
            selected_drum_pad = self.device.view.selected_drum_pad
            self._on_name_changed.subject = selected_drum_pad
            index = 0
            for pad in self._visible_drum_pads:
                if pad == selected_drum_pad:
                    self._pads[index].selected = True
                    self._selected_pad = self._pads[index]
                else:
                    self._pads[index].selected = False
                self._pads[index].set_color(self.pad_to_color(pad))
                self._pads[index].set_pad(pad)
                index += 1

        else:
            for dpad in self._pads:
                dpad.set_color(((0, 0, 40), (0, 0, 40)))
                dpad.set_pad(None)

            for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
                pad_index = (3 - row) * 4 + column
                self._pads[pad_index].set_button(button)
                if not self._in_edit_mode:
                    self._pads[pad_index].send_color()

    def assign_track_device(self):
        if self.device and self.device.view:
            self._on_scroll_index_changed.subject = None
            self._on_selected_drum_pad_changed.subject = None
            self._on_chains_changed.subject = None
            self._on_name_changed.subject = None
        self.track = self.song().view.selected_track
        self.device = find_drum_device(self.track)
        if self.device:
            self._on_scroll_index_changed.subject = self.device.view
            self._on_selected_drum_pad_changed.subject = self.device.view
            self._on_chains_changed.subject = self.device
            self._on_name_changed.subject = self.device
        self.assign_pads()

    def index_of(self, pad):
        for index in range(16):
            if self._pads[index]._pad == pad:
                return index

        return -1

    @subject_slot('name')
    def _on_name_changed(self):
        if self._active and self.device:
            self.assign_pads()
            self.update_pads()

    def _device_changed(self):
        if self._active:
            self.assign_track_device()
            self.update_pads()

    @subject_slot('chains')
    def _on_chains_changed(self):
        if self._active and self.device:
            self.assign_pads()
            self.update_pads()

    @subject_slot('selected_drum_pad')
    def _on_selected_drum_pad_changed(self):
        if self._active and self.device:
            if self._selected_pad:
                self._selected_pad.selected = False
                self._selected_pad.send_color()
            selected_drum_pad = self.device.view.selected_drum_pad
            self._on_name_changed.subject = selected_drum_pad
            new_index = self.index_of(selected_drum_pad)
            if 0 <= new_index < 16:
                self._selected_pad = self._pads[new_index]
                self._selected_pad.selected = True
                self._selected_pad.send_color()

    @subject_slot('drum_pads_scroll_position')
    def _on_scroll_index_changed(self):
        if self._active and self.device:
            self.assign_pads()
            self.update_pads()

    def fitting_mode(self, track):
        if not track:
            return self

        drum_device = find_drum_device(track)
        if drum_device == None and self._alternate_mode != None:
            return self._alternate_mode
        return self

    def on_selected_track_changed(self):
        if self._active:
            self.track = self.song().view.selected_track
            self.assign_track_device()
            self.update_pads()

    def exit(self):
        self._active = False
        self._on_scroll_index_changed.subject = None
        self._on_selected_drum_pad_changed.subject = None
        self._on_chains_changed.subject = None
        self._on_name_changed.subject = None
        self.device = None
        self.track = None

    def disconnect(self):
        self.exit()
        self.track = None
        self.device = None
        self._visible_drum_pad_slots = None
        self._visible_drum_pads = None
        self._pads = None
        self._selected_pad = None
        self._in_edit_mode = False
        self._editmode = None
        super(MaschineMode, self).disconnect()
