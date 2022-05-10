from src.scene import *

class SceneManager:
    _current_loaded_scene : Scene = None
    _all_scenes : list[Scene] = []

    def _get_component_current_scene(gameobject_id : int, component_type : Component):
        component : Component = None
        current_scene : Scene = SceneManager._current_loaded_scene
        gameobject, error = current_scene.find_gameobject_by_id(gameobject_id)
        if error == ITEM_NOT_FOUND:
            return component, gameobject, error
        component, error = gameobject.get_component(component_type)
        if error == ITEM_NOT_FOUND:
            return component, gameobject, error
        return component, gameobject, error

    def get_component_current_scene(gameobject_id : int, component_type : Component):
        component, gameobject, error = SceneManager._get_component_current_scene(gameobject_id, component_type)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"component of type {component_type} on {gameobject_id} doesnt exist")
        return component
    
    def remove_component_current_scene(gameobject_id : int, component_type : Component):
        current_scene : Scene = SceneManager._current_loaded_scene
        gameobject, error = current_scene.find_gameobject_by_id(gameobject_id)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"gameobject of id {gameobject_id} wasnt found on scene {current_scene}")        
        error = gameobject.remove_component(component_type)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"component of type {component_type} on {gameobject_id} doesnt exist")

    def has_component_current_scene(gameobject_id : int, component_type : Component) -> bool:
        component, gameobject, error = SceneManager._get_component_current_scene(gameobject_id, component_type)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"component of type {component_type} on {gameobject_id} doesnt exist")
        return error == NO_ERROR

    def ensure_component_current_scene(gameobject_id : int, component_type : Component):
        component, gameobject, error = SceneManager._get_component_current_scene(gameobject_id, component_type)
        if error == ITEM_NOT_FOUND:
            gameobject.add_component(component_type.get_default())
        return gameobject.get_component(component_type)

    def get_known_current_scene(component_type : Component):
        current_scene : Scene = SceneManager._current_loaded_scene
        component, error = current_scene.get_known(component_type)
        if error == ITEM_NOT_FOUND:
            raise Exception(f"component {component_type} doesnt exist on known in scene {current_scene}")
        return component

    def add_gameobject_current_scene(gameobject : GameObject):
        current_scene : Scene = SceneManager._current_loaded_scene
        current_scene.add_gameobject(gameobject)        

    def remove_gameobejct_current_scene(gameobject : GameObject):
        current_scene : Scene = SceneManager._current_loaded_scene
        current_scene.remove_gameobject(gameobject)

    def set_current_scene(scene : Scene):
        SceneManager._current_loaded_scene = scene

    def add_current_scene(scene : Scene):
        SceneManager._all_scenes.append(scene)

    def awake_global(scene : Scene):
        scene.awake()

    def awake_current_scene():
        SceneManager.awake_global(SceneManager._current_loaded_scene)

    def start_global(scene : Scene):
        scene.start()

    def start_current_scene():
        SceneManager.start_global(SceneManager._current_loaded_scene)
    
    def update_global(scene : Scene, delta_time : float, *args):
        scene.update(delta_time, *args)   

    def update_current_scene(delta_time : float, *args):
        SceneManager.update_global(SceneManager._current_loaded_scene, delta_time, *args)

    def update_space_global(scene : Scene, delta_time : float):
        scene.space.step(delta_time)

    def update_space_current_scene(delta_time : float):
        SceneManager.update_space_global(SceneManager._current_loaded_scene, delta_time)

    def invoke_event_global(scene : Scene, delta_time : float, event):
        scene.on_event(delta_time, event)

    def invoke_event_current_scene(delta_time : float, event):
        SceneManager.invoke_event_global(SceneManager._current_loaded_scene, delta_time, event)
    
    def invoke_key_pressed_global(scene : Scene, delta_time : float, key_pressed : list):
        scene.on_key_pressed(delta_time, key_pressed)

    def invoke_key_pressed_current_scene(delta_time : float, key_pressed : list):
        SceneManager.invoke_key_pressed_global(SceneManager._current_loaded_scene, delta_time, key_pressed)