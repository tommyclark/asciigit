from asciimatics.widgets import Frame, ListBox, Layout, Divider, Text, \
    Button, TextBox, Widget, MultiColumnListBox
from asciimatics.exceptions import NextScene, StopApplication
from git import GitCommandError

class BranchListView(Frame):
    def __init__(self, screen, model):
        super(BranchListView, self).__init__(screen,
                                             screen.height * 9 // 10,
                                             screen.width * 9 // 10,
                                             on_load=self._reload_list,
                                             hover_focus=True,
                                             can_scroll=False,
                                             title="Branches")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            model.list_branches(),
            name="branches",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self.__checkout)
        self.__checkout_button = Button("Checkout", self.__checkout)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self.__checkout_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self.__checkout_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self):
        self._list_view.options = self._model.list_branches()
        self._list_view.value = self._model.get_current_branch()

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Branch")

    def __checkout(self):
        self.save()
        try:
            self._model.checkout_branch(self.data["branches"])
        except GitCommandError as e:
            self._model.last_error = e
            raise NextScene("Error")
        self._model.current_id = self.data["branches"]
        self._reload_list()

    def _delete(self):
        self.save()
        self._model.delete_contact(self.data["branches"])
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")

class CommitView(Frame):
    def __init__(self, screen, model):
        super(CommitView, self).__init__(screen,
                                         screen.height * 9 // 10,
                                         screen.width * 9 // 10,
                                         on_load=self._reload_list,
                                         hover_focus=True,
                                         can_scroll=False,
                                         title="Commits")
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        self._list_view = MultiColumnListBox(
            Widget.FILL_FRAME,
            ["10%", "60%", "15%", "15%"],
            model.list_commits(),
            titles=["Hash", "Message", "Author", "Date"],
            name="commits",
            add_scroll_bar=True,
            on_change=self._on_pick,
            on_select=self.__checkout)
        self.__checkout_button = Button("Checkout", self.__checkout)
        self._delete_button = Button("Delete", self._delete)
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view)
        layout.add_widget(Divider())
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Add", self._add), 0)
        layout2.add_widget(self.__checkout_button, 1)
        layout2.add_widget(self._delete_button, 2)
        layout2.add_widget(Button("Quit", self._quit), 3)
        self.fix()
        self._on_pick()

    def _on_pick(self):
        self.__checkout_button.disabled = self._list_view.value is None
        self._delete_button.disabled = self._list_view.value is None

    def _reload_list(self):
        self._list_view.options = self._model.list_commits()
        # self._list_view.value = self._model.get_current_branch()

    def _add(self):
        self._model.current_id = None
        raise NextScene("Edit Branch")

    def __checkout(self):
        self.save()
        # try:
        #     self._model.checkout_branch(self.data["branches"])
        # except GitCommandError as e:
        #     self._model.last_error = e
        #     raise NextScene("Error")
        # self._model.current_id = self.data["branches"]
        self._reload_list()

    def _delete(self):
        self.save()
        self._reload_list()

    @staticmethod
    def _quit():
        raise StopApplication("User pressed quit")


class BranchView(Frame):
    def __init__(self, screen, model):
        super(BranchView, self).__init__(screen,
                                         screen.height * 9 // 10,
                                         screen.width * 9 // 10,
                                         hover_focus=True,
                                         can_scroll=False,
                                         title="Branch Details",
                                         reduce_cpu=True)
        # Save off the model that accesses the contacts database.
        self._model = model

        # Create the form for displaying the list of contacts.
        layout = Layout([100], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(Text("Name:", "name"))
        layout.add_widget(Text("Address:", "address"))
        layout.add_widget(Text("Phone number:", "phone"))
        layout.add_widget(Text("Email address:", "email"))
        layout.add_widget(TextBox(
            Widget.FILL_FRAME, "Notes:", "notes", as_string=True, line_wrap=True))
        layout2 = Layout([1, 1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("OK", self._ok), 0)
        layout2.add_widget(Button("Cancel", self._cancel), 3)
        self.fix()

    def reset(self):
        # Do standard reset to clear out form, then populate with new data.
        super(BranchView, self).reset()
        self.data = self._model.get_current_contact()

    def _ok(self):
        self.save()
        self._model.update_current_contact(self.data)
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")

class ExceptionView(Frame):
    def __init__(self, screen, model):
        super(ExceptionView, self).__init__(screen,
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
        print("testing")

    def _ok(self):
        raise NextScene("Main")

    @staticmethod
    def _cancel():
        raise NextScene("Main")
