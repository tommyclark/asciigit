from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import src.models as models
import src.views as views

def main(screen, scene):
    scenes = [
        Scene([views.ListView(screen, model)], -1, name="Main"),
        Scene([views.BranchView(screen, model)], -1, name="Edit Branch"),
        Scene([views.ExceptionView(screen, model)], -1, name="Error")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True)


model = models.GitModel()
last_scene = None
while True:
    try:
        Screen.wrapper(main, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
