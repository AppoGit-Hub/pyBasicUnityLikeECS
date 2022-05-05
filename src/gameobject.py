import extra
from component import *
from constant import *

class GameObject:
    def __init__(self, components_instances):
        self._components : list[Component] = []
        for component in components_instances:
            self.add_component(component)

    def awake(self):
        for component in self._components:
            component.awake()

    def start(self):
        for component in self._components:
            component.start()

    def update(self, delta_time, *args):
        for component in self._components:
            component.update(delta_time, *args)

    def on_event(self, delta_time, event):
        for component in self._components:
            component.on_event(delta_time, event)

    def on_key_pressed(self, delta_time, on_key_pressed):
        for component in self._components:
            component.on_key_pressed(delta_time, on_key_pressed)    

    def add_component(self, component_instance : Component):
        extra.insert_type(self._components, component_instance, type(component_instance), component_less_then, component_greater_then)
        component_instance.gameobject_id = id(self)

    def _get_component_index(self, component_type : Component):
        index = extra.search(self._components, component_type, component_less_then, component_greater_then)
        if index < len(self._components) and isinstance(self._components[index], component_type):
            return index, NO_ERROR
        else:
            return index, ITEM_NOT_FOUND

    def get_component(self, component_type : Component):
        index, error = self._get_component_index(component_type)
        if error == NO_ERROR:
            return self._components[index], NO_ERROR
        else:
            return None, ITEM_NOT_FOUND

    def has_component(self, component_type : Component) -> bool:
        index, error = self._get_component_index(component_type)
        return error == NO_ERROR

    def ensure_component(self, component_type : Component):
        index, error = self._get_component_index(component_type)
        if error == ITEM_NOT_FOUND:
            self.add_component(component_type)
            
        return self.get_component(component_type)
    
    def remove_component(self, component_type : Component) -> int:
        index, error = self._get_component_index(component_type)
        if error == NO_ERROR:
            del self._components[index]
        return error

    def __repr__(self) -> str:
        text = ""
        for component in self._components:
            text += str(component) + "-"
        return text

def gameobject_less_then(gameobject_a : GameObject, gameobject_b : GameObject):
    return id(gameobject_a) < id(gameobject_b)

def gameobject_greater_then(gameobject_a : GameObject, gameobject_b : GameObject):
    return id(gameobject_a) > id(gameobject_b) 

def gameobject_id_less_then(gameobject_a : GameObject, gameobject_id : int):
    return id(gameobject_a) < gameobject_id

def gameobject_id_greater_then(gameobject_a : GameObject, gameobject_id : int):
    return id(gameobject_a) > gameobject_id