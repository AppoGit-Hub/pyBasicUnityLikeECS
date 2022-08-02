
class Component:
    def __init__(self):
        self.gameobject_id = 0

    def get_default(self):
        raise Exception("No default function implemented")

    def copy(self):
        return Component()

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