from pybasicunitylikeecs.component import Component
from pybasicunitylikeecs.scenemanager import SceneManager
from pybasicunitylikeecs.scene import Scene
from pybasicunitylikeecs.gameobject import GameObject

class Vector(Component):
    def __init__(self, x, y):
        super().__init__()
        self.x = x 
        self.y = y
    
    def get_default(self):
        return Vector(0, 0)

class Mover(Component):
    def __init__(self):
        super().__init__()

    def get_default(self):
        return Mover()

    def start(self):
        self.vector : Vector = SceneManager.get_component_current_scene(self.gameobject_id, Vector)

    def update(self, delta_time, *args):
        self.vector.x += delta_time
        self.vector.y += delta_time

        print(f"X:{self.vector.x}, Y:{self.vector.y}")

object = GameObject([Vector(10, 5), Mover()])

mainScene = Scene()
mainScene.add_gameobject(object)
SceneManager.add_current_scene(mainScene)
SceneManager.set_current_scene(mainScene)

SceneManager.start_current_scene()
for _ in range(0, 10):
    SceneManager.update_current_scene(1)