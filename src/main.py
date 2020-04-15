from asciimatics.event import KeyboardEvent
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, StopApplication, NextScene
import sys
import src.models as models
import src.views as views


# Event handler for global keys
def global_shortcuts(event):
    if isinstance(event, KeyboardEvent):
        key = event.key_code
        if key == Screen.KEY_F1:
            raise NextScene("Main")
        elif key == Screen.KEY_F2:
            raise NextScene("Commits")
        elif key == Screen.KEY_F3:
            raise NextScene("Working Copy")
        elif key == Screen.ctrl("a"):
            raise NextScene("Shortcuts")
        elif key == Screen.ctrl("x"):
            raise StopApplication("User terminated app")


def main(screen, scene):
    scenes = [
        Scene([views.BranchListView(screen, branch_model)], -1, name="Main"),
        Scene([views.CommitView(screen, commit_model)], -1, name="Commits"),
        Scene([views.CommitOptionsView(screen, commit_model)], -1, name="Commit Options"),
        Scene([views.CommitFilesView(screen, commit_model)], -1, name="View Commit Details"),
        Scene([views.CommitFileDiffView(screen, commit_model)], -1, name="View Commit Diff"),
        Scene([views.WorkingCopyView(screen, working_copy_model)], -1, name="Working Copy"),
        Scene([views.ShortcutsView(screen)], -1, name="Shortcuts"),
        Scene([views.ExceptionView(screen, branch_model)], -1, name="Error")
    ]

    screen.play(scenes, stop_on_resize=True, start_scene=scene, allow_int=True, unhandled_input=global_shortcuts)


branch_model = models.GitBranchModel()
commit_model = models.GitCommitModel()
working_copy_model = models.WorkingCopyModel()
last_scene = None
while True:
    try:
        Screen.wrapper(main, catch_interrupt=True, arguments=[last_scene])
        sys.exit(0)
    except ResizeScreenError as e:
        last_scene = e.scene
