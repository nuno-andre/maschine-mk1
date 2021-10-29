from .MaschineMk1 import MaschineMk1


def create_instance(c_instance):
    return MaschineMk1(c_instance)


from _Framework.Capabilities import controller_id, inport, outport  # noqa: E402


def get_capabilities():
    return {
        'controller_id': controller_id(
            vendor_id=9000,
            product_ids=[2],
            model_name='Maschine Mk2',
        ),
        'ports': [
            inport(props=['hidden', 'notes_cc', 'script']),
            inport(props=[]),
            outport(props=['hidden', 'notes_cc', 'sync', 'script']),
            outport(props=[]),
        ]
    }
