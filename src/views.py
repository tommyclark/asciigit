from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox
from asciimatics.exceptions import NextScene, StopApplication
from git import GitCommandError


class View(Frame):
    def __init__(self, model, screen, height, width, data=None, on_load=None,
                 has_border=True, hover_focus=False, name=None, title=None,
                 x=None, y=None, has_shadow=False, reduce_cpu=False, is_modal=False,
                 can_scroll=True):
        super(View, self).__init__(screen=screen,
                                   height=height,
                                   width=width,
                                   data=data,
                                   on_load=on_load,
                                   has_border=has_border,
                                   hover_focus=hover_focus,
                                   name=name,
                                   title=title,
                                   x=x,
                                   y=y,
                                   has_shadow=has_shadow,
                                   reduce_cpu=reduce_cpu,
                                   is_modal=is_modal,
                                   can_scroll=can_scroll)
        self._model = model
        self.nav_header = None
        self.set_theme("tlj256")

    def add_navigation_header(self):
        self.nav_header = Layout([1, 1, 1, 1])
        self.add_layout(self.nav_header)
        self.nav_header.add_widget(Button("Branches", self._open_branch_view), 0)
        self.nav_header.add_widget(Button("History", self._open_commits_view), 1)
        self.nav_header.add_widget(Button("Commit", self._open_working_copy_view), 2)
        self.nav_header.add_widget(Button("Quit", self._quit), 3)

    def add_divider(self):
        divider_layout = Layout([100])
        self.add_layout(divider_layout)
        divider_layout.add_widget(Divider())

    def add_shortcut_panel(self):
        layout0 = Layout([100])
        _header = TextBox(1, as_string=True)
        _header.disabled = True
        _header.custom_colour = "label"
        _header.value = "Press ctrl-a to see a list of shortcuts. Press ctrl-x to quit."
        self.add_layout(layout0)
        layout0.add_widget(_header, 0)

    @staticmethod
    def _open_branch_view():
        raise NextScene("Main")

    @staticmethod
    def _open_commits_view():
        raise NextScene("Commits")

    @staticmethod
    def _open_working_copy_view():
        raise NextScene("Working Copy")

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class BranchListView(View):
    def __init__(self, screen, model):
        super(BranchListView, self).__init__(model,
                                             screen,
                                             screen.height * 9 // 10,
                                             screen.width * 9 // 10,
                                             on_load=self._reload_list,
                                             hover_focus=True,
                                             can_scroll=False,
                                             title="Branches")
        self._model = model

        # Create the form for displaying the list of branches.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.list_branches(),
            name="branches",
            add_scroll_bar=True,
            on_select=self.__checkout)

        self.add_navigation_header()
        self.add_divider()

        self.table_layout = Layout([100], fill_frame=True)
        self.add_layout(self.table_layout)
        self.table_layout.add_widget(self._list_view)
        self.table_layout.add_widget(Divider())

        self.add_shortcut_panel()
        self.fix()

    def _reload_list(self):
        self.nav_header.blur()
        self.table_layout.focus()
        self._list_view.options = self._model.list_branches()
        self._list_view.value = self._model.get_current_branch()

    def __checkout(self):
        self.save()
        try:
            self._model.checkout_branch(self.data["branches"])
        except GitCommandError as e:
            self._model.last_error = e
            raise NextScene("Error")
        self._model.current_id = self.data["branches"]
        self._reload_list()


class CommitView(View):
    def __init__(self, screen, model):
        super(CommitView, self).__init__(model,
                                         screen,
                                         screen.height * 9 // 10,
                                         screen.width * 9 // 10,
                                         on_load=self._reload_list,
                                         hover_focus=True,
                                         can_scroll=False,
                                         title="Commits")
        self._model = model

        self._list_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            ["10%", "60%", "15%", "15%"],
            model.list_commits(),
            titles=["Hash", "Message", "Author", "Date"],
            name="commits",
            add_scroll_bar=True,
            on_select=self.__view_diff)

        self.add_navigation_header()
        self.add_divider()

        self.table_layout = Layout([100], fill_frame=True)
        self.add_layout(self.table_layout)
        self.table_layout.add_widget(self._list_view)
        self.table_layout.add_widget(Divider())

        self.add_shortcut_panel()
        self.fix()

    def __view_diff(self):
        self.save()
        self._model.current_commit = self.data["commits"]
        self.__open_commit_details_scene()

    @staticmethod
    def __open_commit_details_scene():
        raise NextScene("Commit Options")

    def _reload_list(self):
        self._list_view.options = self._model.list_commits()
        self.nav_header.blur()
        self.table_layout.focus()


class CommitOptionsView(View):
    def __init__(self, screen, model):
        super(CommitOptionsView, self).__init__(model,
                                                screen,
                                                screen.height * 6 // 10,
                                                screen.width * 6 // 10,
                                                hover_focus=True,
                                                can_scroll=False,
                                                title="Commit Options",
                                                reduce_cpu=True)
        self._model = model

        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Button("View changes in commit..", self._view_changes), 0)
        layout.add_widget(Button("Checkout commit..", self._checkout_commit), 0)
        layout.add_widget(Button("Cancel", self._open_commits_view), 0)

        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(CommitOptionsView, self).reset()

    def _view_changes(self):
        raise NextScene("View Commit Details")

    def _checkout_commit(self):
        try:
            self._model.checkout_commit()
            # self._open_commits_view()
        except GitCommandError as e:
            print(e)
            self._model.last_error = e
            raise NextScene("Error")


class CommitFilesView(View):
    def __init__(self, screen, model):
        super(CommitFilesView, self).__init__(model,
                                              screen,
                                              screen.height * 9 // 10,
                                              screen.width * 9 // 10,
                                              on_load=self._reload_list,
                                              hover_focus=True,
                                              can_scroll=False,
                                              title="Diff Files")
        self._model = model

        # Create the form for displaying the list of branches.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.list_files_in_current_commit(),
            name="diff_files",
            add_scroll_bar=True,
            on_select=self.__view_diff)

        self.add_navigation_header()
        self.add_divider()

        self.table_layout = Layout([100], fill_frame=True)
        self.add_layout(self.table_layout)
        self.table_layout.add_widget(self._list_view)

        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Back", self._open_commits_view), 0)

        self.table_layout.add_widget(Divider())

        self.add_shortcut_panel()
        self.fix()

    def __view_diff(self):
        self.save()
        self._model.current_commit_file = self.data["diff_files"]
        self.__open_commit_file_diff_scene()

    @staticmethod
    def __open_commit_file_diff_scene():
        raise NextScene("View Commit Diff")

    def _reload_list(self):
        self._list_view.options = self._model.list_files_in_current_commit()
        self.nav_header.blur()
        self.table_layout.focus()


class CommitFileDiffView(View):
    def __init__(self, screen, model):
        super(CommitFileDiffView, self).__init__(model,
                                                 screen,
                                                 screen.height * 9 // 10,
                                                 screen.width * 9 // 10,
                                                 hover_focus=True,
                                                 can_scroll=False,
                                                 title="Commit Diff",
                                                 reduce_cpu=True)
        self._model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._header = TextBox(20, as_string=True)
        self._header.disabled = True
        self._header.custom_colour = "label"
        layout.add_widget(self._header)
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Back", self._open_commits_view), 0)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(CommitFileDiffView, self).reset()
        self._header.value = self._model.current_file_diff()


class WorkingCopyView(View):
    def __init__(self, screen, model):
        super(WorkingCopyView, self).__init__(model,
                                              screen,
                                              screen.height * 9 // 10,
                                              screen.width * 9 // 10,
                                              on_load=self._reload_list,
                                              hover_focus=True,
                                              can_scroll=False,
                                              title="Working copy")
        self._model = model
        screen.catch_interrupt = True

        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.changed_files_for_table(),
            name="working_copy",
            add_scroll_bar=True,
            on_select=self._add_to_index)

        self.add_navigation_header()
        self.add_divider()

        self.table_layout = Layout([100], fill_frame=True)
        self.add_layout(self.table_layout)
        self.table_layout.add_widget(self._list_view)
        self.table_layout.add_widget(Divider())

        self._commit_button = Button("Commit", self._commit)
        self._push_button = Button("Push", self._push)

        layout2 = Layout([8, 1, 1])
        self.add_layout(layout2)

        self.commit_message = Text("Commit message:", "commit_message")
        layout2.add_widget(self.commit_message, 0)
        layout2.add_widget(self._commit_button, 1)
        layout2.add_widget(self._push_button, 2)

        self.add_divider()

        self.add_shortcut_panel()
        self.fix()

    def _add_to_index(self):
        self.save()
        self._model.toggle_add_file_to_index(self.data["working_copy"])
        self._reload_list()

    def _commit(self):
        self._model.commit(self.commit_message.value)
        self.reset()

    def _push(self):
        self._model.push()
        self.reset()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(WorkingCopyView, self).reset()
        self._reload_list()

    def _reload_list(self):
        self._list_view.options = self._model.changed_files_for_table()
        self.nav_header.blur()
        self.table_layout.focus()


class ExceptionView(View):
    def __init__(self, screen, model):
        super(ExceptionView, self).__init__(model,
                                            screen,
                                            screen.height * 9 // 10,
                                            screen.width * 9 // 10,
                                            hover_focus=True,
                                            can_scroll=False,
                                            title="Error",
                                            reduce_cpu=True)
        self._model = model
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        self._header = TextBox(20, as_string=True)
        self._header.disabled = True
        self._header.custom_colour = "label"
        layout.add_widget(self._header)
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(ExceptionView, self).reset()
        self._header.value = "Error encountered: {0}".format(self._model.last_error)

    def _ok(self):
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")


class ShortcutsView(Frame):
    def __init__(self, screen):
        super(ShortcutsView, self).__init__(screen,
                                            screen.height * 6 // 10,
                                            screen.width * 6 // 10,
                                            hover_focus=True,
                                            can_scroll=False,
                                            title="Shortcuts",
                                            reduce_cpu=True)
        self.set_theme("tlj256")

        layout = Layout([100, 100], fill_frame=True)
        self.add_layout(layout)
        self._row0 = TextBox(20, as_string=True)
        self._row0.disabled = True
        self._row0.value = "F1 - See branch window\n" \
                           "Ctrl-A - See shortcuts window"
        layout.add_widget(self._row0, 0)
        self._row1 = TextBox(20, as_string=True)
        self._row1.disabled = True
        self._row1.value = "F2 - See commit list window\n" \
                           "F3 - See working copy and commit window"
        layout.add_widget(self._row1, 1)
        layout2 = Layout([1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Okay", self._ok), 1)
        self.fix()

    def reset(self):
        super(ShortcutsView, self).reset()

    def _ok(self):
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")
