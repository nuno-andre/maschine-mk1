from _Framework.SceneComponent import SceneComponent
from _Framework.Util import nop

from .ModClipSlotComponent import ModClipSlotComponent

# import Live
# from _Framework.Util import in_range


class ModSceneComponent(SceneComponent):
    """Special Scene Component for Maschine.
    """
    clip_slot_component_type = ModClipSlotComponent

    def __init__(self, num_slots=0, tracks_to_use_callback=nop, *args, **kwargs):
        super().__init__(num_slots, tracks_to_use_callback, *args, **kwargs)
