from gameobject import *

class Scene:
    def __init__(self):
        self._gameobjects : dict[int, GameObject] = {}
        self._known : GameObject = GameObject([])

    def awake(self):
        self._known.awake()
        for id, gameobject in list(self._gameobjects.items()):
            gameobject.awake()

    def start(self):
        self._known.start()
        for id, gameobject in list(self._gameobjects.items()):
            gameobject.start()

    def update(self, delta_time, *args, **kargs):
        self._known.update(delta_time, *args)
        for id, gameobject in list(self._gameobjects.items()):
            gameobject.update(delta_time, *args, **kargs)

    def on_event(self, delta_time, event, *args, **kargs):
        self._known.on_event(delta_time, event, *args, **kargs)
        for id, gameobject in list(self._gameobjects.items()):
            gameobject.on_event(delta_time, event, *args, **kargs)

    def on_key_pressed(self, delta_time, on_key_pressed):
        self._known.on_key_pressed(delta_time, on_key_pressed)
        for id, gameobject in list(self._gameobjects.items()):
            gameobject.on_key_pressed(delta_time, on_key_pressed)    

    def add_known(self, component_instance : Component):
        self._known.add_component(component_instance)

    def get_known(self, component_type : Component):
        return self._known.get_component(component_type)

    def add_gameobject(self, gameobject : GameObject):
        self._gameobjects.update({id(gameobject) : gameobject})
        #gameobject.awake()
        #gameobject.start()

    def remove_gameobject_by_id(self, gameobject_id : int):
        can_remove = self.has_gameobject_by_id(gameobject_id)
        if can_remove:
            self._gameobjects.pop(gameobject_id)
        return can_remove

    def remove_gameobject(self, gameobject : GameObject):
        return self.remove_gameobject_by_id(id(gameobject))

    def has_gameobject_by_id(self, gameobject_id : int):
        gameobject, error = self.find_gameobject_by_id(gameobject_id)
        return error != ITEM_NOT_FOUND 

    def has_gameobject(self, gameobject : GameObject):
        return self.has_gameobject_by_id(id(gameobject))

    def find_gameobject_by_id(self, gameobject_id : int):
        gameobject = self._gameobjects.get(gameobject_id, ITEM_NOT_FOUND)
        return gameobject, gameobject