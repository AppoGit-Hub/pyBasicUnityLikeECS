import pymunk
from gameobject import *

class Scene:
    def __init__(self, space):
        self._gameobjects : list[GameObject] = []
        self._known : GameObject = GameObject([])
        self.space : pymunk.Space = space

    def awake(self):
        for gameobject in self._gameobjects:
            gameobject.awake()

    def start(self):
        for gameobject in self._gameobjects:
            gameobject.start()

    def update(self, delta_time, *args):
        for gameobject in self._gameobjects:
            gameobject.update(delta_time, *args)

    def on_event(self, delta_time, event):
        for gameobject in self._gameobjects:
            gameobject.on_event(delta_time, event)

    def on_key_pressed(self, delta_time, on_key_pressed):
        for gameobject in self._gameobjects:
            gameobject.on_key_pressed(delta_time, on_key_pressed)    

    def add_known(self, component_instance : Component):
        self._known.add_component(component_instance)

    def get_known(self, component_type : Component):
        return self._known.get_component(component_type)

    def add_gameobject(self, gameobject : GameObject):
        extra.insert(self._gameobjects, gameobject, gameobject_less_then, gameobject_greater_then)

    def remove_gameobject(self, gameobject : GameObject):
        index, error = self._find_gameobject_index(gameobject)
        if error == NO_ERROR:
            del self._gameobjects[index]
        return error

    def has_gameobject(self, gameobject : GameObject):
        index, error = self._find_gameobject_index(gameobject)
        return error == NO_ERROR

    def _find_gameobject_index(self, gameobject : GameObject):
        index = extra.search(self._gameobjects, gameobject, gameobject_less_then, gameobject_greater_then)
        if index < len(self._gameobjects) and self._gameobjects[index] == gameobject:
            return index, NO_ERROR
        else:
            return -1, ITEM_NOT_FOUND

    def get_gameobject_by_index(self, gameobject_index : int):
        if gameobject_index >= 0 and gameobject_index < len(self._gameobjects):
            return self._gameobjects[gameobject_index], NO_ERROR
        else:
            return None, ITEM_NOT_FOUND

    def find_gameobject_index_by_id(self, gameobject_id : int):
        index = extra.search(self._gameobjects, gameobject_id, gameobject_id_less_then, gameobject_id_greater_then)
        error = NO_ERROR
        if id(self._gameobjects[index]) == gameobject_id:
            error = ITEM_NOT_FOUND
        return index, error     

    def find_gameobject_by_id(self, gameobject_id : int):
        index, error = self.find_gameobject_index_by_id(gameobject_id)
        if error == ITEM_NOT_FOUND:
            return index, error
        gamobject, error = self.get_gameobject_by_index(index)
        if error == ITEM_NOT_FOUND:
            return index, error
        return gamobject, error


def scene_less_then(scene_a : Scene, scene_b : Scene):
    return id(scene_a) < id(scene_b)

def scene_greater_then(scene_a : Scene, scene_b : Scene):
    return id(scene_a) > id(scene_b)

