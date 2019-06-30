import os
from git import Repo

class GitModel(object):
    def __init__(self):
        # Current branch when editing.
        self.current_id = None
        self.last_error = None

        dir_path = os.getcwd()
        self.repo = Repo(dir_path)
        self.branches = self.repo.branches
        assert not self.repo.bare

    def list_branches(self):
        branches = []
        for branch in self.branches:
            branch_name = branch.name
            if self.is_current_branch(branch):
                branch_name = "✓ " + branch_name
            else :
                branch_name = " " + branch_name
            if branch.tracking_branch() is not None:
                branch_name = branch_name + " -> " + branch.tracking_branch().name
            branch_with_name = [branch_name, branch]
            branches.append(branch_with_name)
        return branches

    def is_current_branch(self, branch):
        return branch == self.get_current_branch()

    def get_current_branch(self):
        return self.repo.active_branch

    def get_current_contact(self):
        if self.current_id is None:
            return {"name": "", "address": "", "phone": "", "email": "", "notes": ""}
        else:
            return self.get_contact(self.current_id)

    def checkout_branch(self, branch_name):
        # self.repo.git.stash()
        self.repo.git.checkout(branch_name)
        # self.repo.git.stash('pop')
