
class Component:
    def __init__(self):
        self.gameobject_id = 0

    def get_default():
        raise Exception("No default function implemented")

    def awake(self):
        pass

    def start(self):
        pass

    def update(self, delta_time, *args):
        pass

    def on_event(self, delta_time, event):
        pass

    def on_key_pressed(self, delta_time, on_key_pressed):
        pass

    def __repr__(self) -> str:
        return type(self).__name__

def component_less_then(component_instance, component_type):
    return type(component_instance).__name__ < component_type.__name__

def component_greater_then(component_instance, component_type):
    return type(component_instance).__name__ > component_type.__name__