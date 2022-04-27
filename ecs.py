from pymunk import Space
import extra

CURRENT_CLASS = 0
BASE_CLASS = 1

NO_ERROR = 0
ITEM_NOT_FOUND = 1

class Component:
    def __init__(self):
        self.gameobject_id = 0

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

class Scene:
    def __init__(self, space):
        self._gameobjects : list[GameObject] = []
        self._known : GameObject = GameObject([])
        self.space : Space = space

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
    
    def find_gameobject_by_id(self, gameobject_id : int):
        index = extra.search(self._gameobjects, gameobject_id, gameobject_id_less_then, gameobject_id_greater_then)
        if index < len(self._gameobjects) and id(self._gameobjects[index]) == gameobject_id:
            return index, NO_ERROR
        else:
            return None, ITEM_NOT_FOUND


def scene_less_then(scene_a : Scene, scene_b : Scene):
    return id(scene_a) < id(scene_b)

def scene_greater_then(scene_a : Scene, scene_b : Scene):
    return id(scene_a) > id(scene_b)

class SceneManager:
    _current_loaded_scene : Scene = None
    _all_scenes : list[Scene] = []

    def get_component_current_scene(gameobject_id : int, component_type : Component):
        component : Component = None
        current_scene : Scene = SceneManager._current_loaded_scene
        index, error = current_scene.find_gameobject_by_id(gameobject_id)
        if error == NO_ERROR:
            gameobject, error = current_scene.get_gameobject_by_index(index)
            if error == NO_ERROR:
                component, error = gameobject.get_component(component_type)
                if error == ITEM_NOT_FOUND:
                    raise Exception(f"component {component_type} doesnt exist in gameobject {gameobject}")
            else:
                raise Exception(f"gameobject of index {index} doesnt exist in scene {current_scene}")
        else:
            raise Exception(f"gameobject of id {gameobject_id} doesnt exist in scene {current_scene}")

        return component
    
    def get_known_current_scene(component_type : Component):
        current_scene : Scene = SceneManager._current_loaded_scene
        component, error = current_scene.get_known(component_type)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"component {component_type} doesnt exist on known in scene {current_scene}")
        return component

    def _find_scene_index(scene : Scene):
        index = extra.search(SceneManager._all_scenes, scene, scene_less_then, scene_greater_then)
        if index < len(SceneManager._all_scenes) and SceneManager._all_scenes[index] == scene:
            return index, NO_ERROR
        else:
            return -1, ITEM_NOT_FOUND

    def set_current_scene(scene : Scene):
        SceneManager._current_loaded_scene = scene
        scene.awake()
        scene.start()

    def awake_global(scene : Scene):
        for gameobject in scene._gameobjects: 
            for component in gameobject._components:
                component.awake()

    def awake_current_scene():
        SceneManager.awake_global(SceneManager._current_loaded_scene)

    def start_global(scene : Scene):
        for gameobject in scene._gameobjects:
            for component in gameobject._components:
                component.start()        

    def start_current_scene():
        SceneManager.start_global(SceneManager._current_loaded_scene)
    
    def update_global(scene : Scene, delta_time : float, *args):
        for gameobject in scene._gameobjects:
            for component in gameobject._components:
                component.update(delta_time, *args)       

    def update_current_scene(delta_time : float, *args):
        SceneManager.update_global(SceneManager._current_loaded_scene, delta_time, *args)

    def update_space_global(scene : Scene, delta_time : float):
        scene.space.step(delta_time)

    def update_space_current_scene(delta_time : float):
        SceneManager.update_space_global(SceneManager._current_loaded_scene, delta_time)

    def invoke_event_global(scene : Scene, delta_time : float, event):
        for gameobject in scene._gameobjects:
            for component in gameobject._components:
                component.on_event(delta_time, event) 

    def invoke_event_current_scene(delta_time : float, event):
        SceneManager.invoke_event_global(SceneManager._current_loaded_scene, delta_time, event)
    
    def invoke_key_pressed_global(scene : Scene, delta_time : float, key_pressed : list):
        for gameobject in scene._gameobjects:
            for component in gameobject._components:
                component.on_key_pressed(delta_time, key_pressed)

    def invoke_key_pressed_current_scene(delta_time : float, key_pressed : list):
        SceneManager.invoke_key_pressed_global(SceneManager._current_loaded_scene, delta_time, key_pressed)
