from component import *
from constant import *

class GameObject:
    def __init__(self, components_instances):
        self._components : dict = {}
        for component in components_instances:
            self.add_component(component)

    def copy(self):
        components_copy : list[Component] = []
        for type, component in self._components.items():
            components_copy.append(component.copy())
        return GameObject(components_copy)

    def awake(self):
        for type, component in self._components.items():
            component.awake()

    def start(self):
        for type, component in self._components.items():
            component.start()

    def update(self, delta_time, *args):
        for type, component in self._components.items():
            component.update(delta_time, *args)

    def on_event(self, delta_time, event):
        for type, component in self._components.items():
            component.on_event(delta_time, event)

    def on_key_pressed(self, delta_time, on_key_pressed):
        for type, component in self._components.items():
            component.on_key_pressed(delta_time, on_key_pressed)    

    def add_component(self, component_instance : Component):
        self._components.update({type(component_instance) : component_instance})
        component_instance.gameobject_id = id(self)

    def get_component(self, component_type : Component) -> tuple[Component, int]:
        component_instance = self._components.get(component_type, ITEM_NOT_FOUND)
        return component_instance, component_instance

    def has_component(self, component_type : Component) -> bool:
        component_instance, error = self.get_component(component_type)
        return error == NO_ERROR

    def ensure_component(self, component_type : Component):
        component_instance, error = self.get_component(component_type)
        if error == ITEM_NOT_FOUND:
            self.add_component(component_type)
        return self.get_component(component_type)
    
    def remove_component(self, component_type : Component) -> int:
        component_instance, error = self.get_component(component_type)
        if error == NO_ERROR:
            self._components.pop(type(component_instance))
        return error
        
    """
    def __repr__(self) -> str:
        text = f"{id(self)}:"
        for component in self._components:
            text += str(component) + "-"
        return text
    """