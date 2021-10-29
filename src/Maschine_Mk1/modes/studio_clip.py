from ._base import MaschineMode
from ..MIDI_Map import CLIP_MODE


class StudioClipMode(MaschineMode):
    __module__ = __name__

    def __init__(self, button_index, *args, **kwargs):
        super().__init__(button_index, *args, **kwargs)

    def get_color(self, value, column_index, row_index):
        session = self.canonical_parent._session
        scene = session.scene(row_index)
        clip_slot = scene.clip_slot(column_index)._clip_slot
        color = session.get_color(clip_slot)
        cindex = value == 0 and 1 or 0
        return color[cindex]

    def notify(self, blink_state):
        self.canonical_parent._session.notify(blink_state)

    def notify_mono(self, blink_state):
        self.canonical_parent._session.notify_mono(blink_state)

    def enter_edit_mode(self, type):
        self.canonical_parent._session.set_enabled(False)

    def exit_edit_mode(self, type):
        self.canonical_parent._session.set_enabled(True)

    def get_mode_id(self):
        return CLIP_MODE

    def navigate(self, dir_, modifier, alt_modifier=False):
        if modifier:
            if dir_ == 1:
                self.canonical_parent._session.bank_up()
            else:
                self.canonical_parent._session.bank_down()
        elif dir_ == 1:
            self.canonical_parent._session.bank_right()
        else:
            self.canonical_parent._session.bank_left()

    def enter(self):
        self._active = True
        for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
            if button:
                button.set_to_notemode(False)
                scene = self.canonical_parent._session.scene(row)
                clip_slot = scene.clip_slot(column)
                clip_slot.set_launch_button(button)

    def refresh(self):
        if self._active:
            for button, (column, row) in self.canonical_parent._bmatrix.iterbuttons():
                if button:
                    button.reset()
                    button.refresh()

    def exit(self):
        self._active = False
        self.canonical_parent._deassign_matrix()
        self.canonical_parent._session.set_clip_launch_buttons(None)
