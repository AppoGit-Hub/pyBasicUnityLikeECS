import pymunk
from src.gameobject import *

class Scene:
    def __init__(self, space):
        self._gameobjects : dict[int, GameObject] = {}
        self._known : GameObject = GameObject([])
        self.space : pymunk.Space = space

    def awake(self):
        self._known.awake()
        for id, gameobject in self._gameobjects.items():
            gameobject.awake()

    def start(self):
        self._known.start()
        for id, gameobject in self._gameobjects.items():
            gameobject.start()

    def update(self, delta_time, *args):
        self._known.update(delta_time, *args)
        for id, gameobject in self._gameobjects.items():
            gameobject.update(delta_time, *args)

    def on_event(self, delta_time, event):
        self._known.on_event(delta_time, event)
        for id, gameobject in self._gameobjects.items():
            gameobject.on_event(delta_time, event)

    def on_key_pressed(self, delta_time, on_key_pressed):
        self._known.on_key_pressed(delta_time, on_key_pressed)
        for id, gameobject in self._gameobjects.items():
            gameobject.on_key_pressed(delta_time, on_key_pressed)    

    def add_known(self, component_instance : Component):
        self._known.add_component(component_instance)

    def get_known(self, component_type : Component):
        return self._known.get_component(component_type)

    def add_gameobject(self, gameobject : GameObject):
        self._gameobjects.update({id(gameobject) : gameobject})

    def remove_gameobject(self, gameobject : GameObject):
        error = self.has_gameobject(gameobject)
        if error == NO_ERROR:
            self._gameobjects.pop(id(gameobject))
        return error

    def has_gameobject(self, gameobject : GameObject):
        gameobject, error = self.find_gameobject_by_id(id(gameobject))
        return error == NO_ERROR

    def find_gameobject_by_id(self, gameobject_id : int):
        gameobject = self._gameobjects.get(gameobject_id, ITEM_NOT_FOUND)
        if gameobject == ITEM_NOT_FOUND:
            return gameobject, ITEM_NOT_FOUND
        else:
            return gameobject, NO_ERROR