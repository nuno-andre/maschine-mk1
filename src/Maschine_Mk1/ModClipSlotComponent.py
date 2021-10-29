from _Framework.ClipSlotComponent import ClipSlotComponent
from _Framework.SubjectSlot import subject_slot

from .MIDI_Map import vindexof, CLIP_MODE

# import Live


class ModClipSlotComponent(ClipSlotComponent):
    """Clip Slot Component for Maschine.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_modifier(self, modifier):
        self._modifier = modifier

    @subject_slot('value')
    def _launch_button_value(self, value):
        if self.is_enabled():
            if self._modifier and self._modifier.hasModification(CLIP_MODE):
                self._modifier.edit_clip_slot(self, value)
            elif self._clip_slot != None and self._modifier and self._modifier.isShiftdown() and value != 0:
                track = self._clip_slot.canonical_parent
                scenes = self.song().scenes
                index = vindexof(track.clip_slots, self._clip_slot)
                scenes[index].fire()
            elif self._clip_slot != None and self._modifier and self._modifier.isClipAltDown() and value != 0:
                track = self._clip_slot.canonical_parent
                if track.is_foldable and value != 0:
                    if track.fold_state == 0:
                        track.fold_state = 1
                    else:
                        track.fold_state = 0
            elif self._clip_slot != None:
                self._do_launch_clip(value)

    def get_launch_button(self):
        return self._launch_button_value_slot.subject
