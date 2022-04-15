
class Component:
    def __init__(self):
        self.id = 0

    def start(self):
        pass

    def update(self):
        pass

GameObject = dict[type : Component]

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
        Scene._all_scenes.update({self.sceneID : {}})
        Scene._next_scene_id += 1

    def addGameObjectGlobal(sceneID : int, gameObject : list[Component]) -> int:
        nextGameobjectID = Scene._all_scenes[sceneID].nextGameobjectID
        Scene._all_scenes[sceneID].update({
            nextGameobjectID : components_to_gameObject(nextGameobjectID, gameObject)
        })
        nextGameobjectID += 1
        return nextGameobjectID - 1

    def addGameObjectCurrentScene(gameObject : list[Component]):
        return Scene.addGameObjectGlobal(Scene._next_scene_id, gameObject)

    def addGameObject(self, gameObject : list[Component]):
        return  Scene.addGameObjectGlobal(self.sceneID, gameObject)

    def removeGameObjectGlobal(sceneID : int, gameObjectID : int):
        del Scene._all_scenes[sceneID][gameObjectID]

    def removeGameObjectCurrentScene(gameObjectID : int):
        Scene.removeGameObjectGlobal(Scene._current_loaded_scene_id, gameObjectID)

    def removeGameObject(self, gameObjectID : int):
        Scene.removeGameObjectGlobal(self.sceneID, gameObjectID)

    def addComponentGlobal(sceneID : int, gameObjectID : int, componentInstance : int):
        gameObject = Scene._all_scenes[sceneID][gameObjectID]
        gameObject.update({type(componentInstance) : componentInstance})      

    def addComponentCurrentScene(gameObjectID : int, componentInstance : int):
        Scene.addComponentGlobal(Scene._current_loaded_scene_id, gameObjectID, componentInstance)

    def addComponent(self, gameObjectID : int, componentInstance : int):
        Scene.addComponentGlobal(self.sceneID, gameObjectID, componentInstance)

    def getComponentGlobal(sceneID : int, gameObjectID : int, type : type) -> Component:
        return Scene._all_scenes[sceneID][gameObjectID][type]

    def getComponentCurrentScene(gameObjectID : int, type : type):
        return Scene.getComponentGlobal(Scene._current_loaded_scene_id, gameObjectID, type) 

    def getComponent(self, gameObjectID : int, type : type):
        return Scene.getComponentGlobal(self.sceneID, gameObjectID,type)

    def setLoadScene(scene : 'Scene'):
        Scene._current_loaded_scene_id = scene.sceneID

    def startGlobal(sceneID : int):
        for gameObject in Scene._all_scenes[sceneID].values():
            for component in gameObject.values():
                component.start()        

    def startCurrentScene():
        Scene.startGlobal(Scene._current_loaded_scene_id)

    def start(self):
        Scene.startGlobal(self.sceneID)
    
    def updateGlobal(sceneID : int):
        for gameObject in  Scene._all_scenes[sceneID].values():
            for component in gameObject.values():
                component.update()       

    def updateCurrentScene():
        Scene.updateGlobal(Scene._current_loaded_scene_id)

    def update(self):
        Scene.updateGlobal(self.sceneID)