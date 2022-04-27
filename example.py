from ecs import Component, GameObject, Scene, SceneManager
from pymunk import Space

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
        self.position : Vector = SceneManager.get_component_current_scene(self.gameobject_id, Vector)

    def update(self, delta_time):
        self.position.x += 1
        self.position.y += 1

# Example:

gameobject_a = GameObject([
    Vector(10, 5),
    Move()
])

scene_a = Scene(Space())
scene_a.add_gameobject(gameobject_a)
SceneManager.set_current_scene(scene_a)

scene_b = Scene(Space())

gameobject_b = GameObject([
    Vector(0, 5),
    Move()
])

gameobject_c = GameObject([
    Vector(0, 10),
    Move()
])

scene_b.add_gameobject(gameobject_b)
scene_b.add_gameobject(gameobject_c) 

print("Runing Scene A")
# run sceneA (by default, first scene added)
SceneManager.start_current_scene()
for _ in range(0, 5):
    SceneManager.update_current_scene(0.16)


SceneManager.set_current_scene(scene_b)

print("Runing Scene B")
# run sceneB
SceneManager.start_current_scene()
for _ in range(0, 5):
    SceneManager.update_current_scene(0.16)