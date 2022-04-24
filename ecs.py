
class Component:
    def __init__(self):
        self.id = 0

    def awake(self):
        pass

    def start(self):
        pass

    def update(self, deltaTime, *args):
        pass

    def onEvent(self, deltaTime, event):
        pass

    def onKeyPressed(self, deltaTime, onKeyPressed):
        pass

GameObject = dict[type : Component]
KNOWN_ID = 0

def components_to_gameObject(id, components : list[Component]) -> GameObject:
    gameObject : GameObject = {}
    for component in components:
        component.id = id
        gameObject.update({type(component) : component})   
    return gameObject

class Scene:
    _current_loaded_scene_id : int = 0
    _next_scene_id : int = 0
    _all_scenes : dict = {}
    def __init__(self):
        self.nextGameobjectID = 0
        self.sceneID = Scene._next_scene_id
        Scene._all_scenes.update({self.sceneID : {} })
        self.addGameObject([])
        Scene._next_scene_id += 1

    def addKnownGlobal(sceneID : int, component : Component):
        Scene.addComponentGlobal(sceneID, KNOWN_ID, component)

    def addKnownCurrentScene(component : Component):
        Scene.addKnownGlobal(Scene._current_loaded_scene_id, component)

    def addKnown(self, component : Component):
        Scene.addKnownGlobal(self.sceneID, component)

    def getKnownGlobal(sceneID : int, component : Component):
        return Scene.getComponentGlobal(sceneID, KNOWN_ID, component)

    def getKnownCurrentScene(component : Component):
        return Scene.getKnownGlobal(Scene._current_loaded_scene_id, component)

    def getKnown(self, component : Component):
        return Scene.getKnownGlobal(self.sceneID, component)

    def addGameObjectGlobal(sceneID : int, gameObject : list[Component]) -> int:
        nextGameobjectID = 0
        if (len(Scene._all_scenes[sceneID]) > 0):
            nextGameobjectID = list(Scene._all_scenes[sceneID].keys())[-1] + 1
        Scene._all_scenes[sceneID].update({
            nextGameobjectID : components_to_gameObject(nextGameobjectID, gameObject)
        })
        for component in gameObject: component.awake()
        for component in gameObject: component.start()
        return nextGameobjectID

    def addGameObjectCurrentScene(gameObject : list[Component]):
        return Scene.addGameObjectGlobal(Scene._current_loaded_scene_id, gameObject)

    def addGameObject(self, gameObject : list[Component]):
        return  Scene.addGameObjectGlobal(self.sceneID, gameObject)

    def removeGameObjectGlobal(sceneID : int, gameObjectID : int):
        scene : dict = Scene._all_scenes[sceneID]
        scene.pop(gameObjectID, None)

    def removeGameObjectCurrentScene(gameObjectID : int):
        Scene.removeGameObjectGlobal(Scene._current_loaded_scene_id, gameObjectID)

    def removeGameObject(self, gameObjectID : int):
        Scene.removeGameObjectGlobal(self.sceneID, gameObjectID)

    def addComponentGlobal(sceneID : int, gameObjectID : int, componentInstance : Component):
        gameObject = Scene._all_scenes[sceneID][gameObjectID]
        gameObject.update({type(componentInstance) : componentInstance})      

    def addComponentCurrentScene(gameObjectID : int, componentInstance : Component):
        Scene.addComponentGlobal(Scene._current_loaded_scene_id, gameObjectID, componentInstance)

    def addComponent(self, gameObjectID : int, componentInstance : Component):
        Scene.addComponentGlobal(self.sceneID, gameObjectID, componentInstance)

    def ensureComponentGlobal(sceneID : int, gameObjectID : int, componentInstance : Component):
        if not Scene.hasComponentGlobal(sceneID, gameObjectID, componentInstance):
            Scene.addComponentGlobal(sceneID, gameObjectID, componentInstance)
        return Scene.getComponentGlobal(sceneID, gameObjectID, componentInstance)

    def ensureComponentCurrentScene(gameObjectID : int, componentInstance : Component):
        Scene.ensureComponentGlobal(Scene._current_loaded_scene_id, gameObjectID, componentInstance)

    def ensureComponent(self, gameObjectID : int, componentInstance : Component):
        Scene.ensureComponentGlobal(self.sceneID, gameObjectID, componentInstance)

    def hasComponentGlobal(sceneID : int, gameObjectID : int, componentInstance : Component):
        return componentInstance in Scene._all_scenes[sceneID][gameObjectID]

    def hasComponentCurrentScene(gameObjectID : int, componentInstance : Component):
        return componentInstance in Scene._all_scenes[Scene._current_loaded_scene_id][gameObjectID]

    def hasComponent(self, gameObjectID : int, componentInstance : Component):
        return componentInstance in Scene._all_scenes[self.sceneID][gameObjectID]

    def getComponentGlobal(sceneID : int, gameObjectID : int, type : type) -> Component:
        return Scene._all_scenes[sceneID][gameObjectID][type]

    def getComponentCurrentScene(gameObjectID : int, type : type):
        return Scene.getComponentGlobal(Scene._current_loaded_scene_id, gameObjectID, type) 

    def getComponent(self, gameObjectID : int, type : type):
        return Scene.getComponentGlobal(self.sceneID, gameObjectID,type)

    def setLoadScene(scene : 'Scene'):
        Scene._current_loaded_scene_id = scene.sceneID
        scene.awake()
        scene.start()

    def awakeGlobal(sceneID : int):
        for gameObject in list(Scene._all_scenes[sceneID].values()): 
            for component in gameObject.values():
                component.awake()

    def awakeCurrentScene():
        Scene.awakeGlobal(Scene._current_loaded_scene_id)

    def awake(self):
        Scene.awakeGlobal(self.sceneID)

    def startGlobal(sceneID : int):
        for gameObject in list(Scene._all_scenes[sceneID].values()):
            for component in gameObject.values():
                component.start()        

    def startCurrentScene():
        Scene.startGlobal(Scene._current_loaded_scene_id)

    def start(self):
        Scene.startGlobal(self.sceneID)
    
    def updateGlobal(sceneID : int, deltaTime : float, *args):
        for gameObject in list(Scene._all_scenes[sceneID].values()):
            for component in gameObject.values():
                component.update(deltaTime, *args)       

    def updateCurrentScene(deltaTime : float, *args):
        Scene.updateGlobal(Scene._current_loaded_scene_id, deltaTime, *args)

    def update(self, deltaTime : float, *args):
        Scene.updateGlobal(self.sceneID, deltaTime, *args)

    def invokeEventGlobal(sceneID : int, deltaTime, event):
        for gameObject in list(Scene._all_scenes[sceneID].values()):
            for component in gameObject.values():
                component.onEvent(deltaTime, event) 

    def invokeEventCurrentScene(deltaTime : float, event):
        Scene.invokeEventGlobal(Scene._current_loaded_scene_id, deltaTime, event)

    def invokeEvent(self, deltaTime : float, event):
        Scene.invokeEventGlobal(self.sceneID, deltaTime, event)
    
    def invokeKeyPressedGlobal(sceneID : int, deltaTime : float, keyPressed : list):
        for gameObject in list(Scene._all_scenes[sceneID].values()):
            for component in gameObject.values():
                component.onKeyPressed(deltaTime, keyPressed)

    def invokeKeyPressedCurrentScene(deltaTime : float, keyPressed : list):
        Scene.invokeKeyPressedGlobal(Scene._current_loaded_scene_id, deltaTime, keyPressed)
    
    def invokeKeyPressed(self, deltaTime : float, keyPressed : list):
        Scene.invokeKeyPressedGlobal(self.sceneID, deltaTime, keyPressed)