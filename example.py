from ecs import Component, Scene

class Vector(Component):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
    
    def __repr__(self) -> str:
        return f"X: {self.x}, Y: {self.y}"

class Move(Component):
    def __init__(self):
        super().__init__()
    
    def start(self):
        self.posComponent : Vector = Scene.getComponent(self.id, Vector)

    def update(self):
        print(self.posComponent)
        self.posComponent.x += 1
        self.posComponent.y += 1

# Example:
sceneA = Scene()
sceneA.addGameObject([Vector(10, 5), Move()])

sceneB = Scene()
gameObjectID = sceneB.addGameObject([Vector(0, 0), Move()])
sceneB.addGameObject([Vector(0, 10), Move()]) 

print("Runing Scene A")
# run sceneA (by default, first scene added)
Scene.startCurrentScene()
for _ in range(0, 5):
    Scene.updateCurrentScene()



Scene.setLoadScene(sceneB)
Scene.removeGameObjectCurrentScene(gameObjectID)

print("Runing Scene B")
# run sceneB
sceneB.start()
for _ in range(0, 5):
    sceneB.update()