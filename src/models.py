# coding: utf-8
import os
from git import Repo
from pydriller import RepositoryMining


class GitModel(object):
    """
    Parent class for all Git models.
    """
    def __init__(self):
        # Current branch when editing.
        self.current_id = None
        self.last_error = None

        self.dir_path = os.getcwd()
        self.repo = Repo(self.dir_path)
        self.branches = self.repo.branches
        assert not self.repo.bare


class GitBranchModel(GitModel):
    """
    Model for listing and manipulating Git branches.
    """
    def list_branches(self):
        """
        Lists branches for Branches table. Prepends the current branch with a tick.
        :return: A list of branch_name, branch tuples.
        """
        branches = []
        for branch in self.branches:
            branch_name = branch.name
            if self.is_current_branch(branch):
                branch_name = "✔ " + branch_name
            else:
                branch_name = "  " + branch_name
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


class GitCommitModel(GitModel):
    def __init__(self):
        super(GitCommitModel, self).__init__()
        self.repository_miner = RepositoryMining(self.dir_path)
        self.current_commit = None
        self.current_commit_file = None

    """
    A model for listing and manipulating git commits.
    """
    def list_commits(self):
        """
        Lists commits for the current branch for the commits table.
        :return: An array of arrays with commit information inside.
        """
        _commits_with_info = []
        for commit in reversed(list(self.repository_miner.traverse_commits())):
            _commit_info = [commit.hash[:12], commit.msg, commit.author.name,
                            commit.author_date.strftime("%d/%m/%Y, %H:%M:%S")]
            _commit_info_with_hash_as_key = [_commit_info, commit]
            _commits_with_info.append(_commit_info_with_hash_as_key)
        return _commits_with_info

    def list_files_in_current_commit(self):
        _file_map = []
        if self.current_commit is not None:
            for diff in self.current_commit.modifications:
                _file_map.append([diff.new_path, diff])
        return _file_map

    def current_file_diff(self):
        _diff = ""
        if self.current_commit_file is not None:
            _diff = self.current_commit_file.diff
        return _diff


class WorkingCopyModel(GitModel):
    """
    A model for viewing working copy file changes.
    """
    def list_of_changed_files(self):
        return self.repo.head.commit.diff(None)

    def list_of_changed_unadded_files(self):
        return self.repo.index.diff(None)

    def list_of_changed_files_in_index(self):
        return self.repo.index.diff('HEAD')

    def changed_files_for_table(self):
        """
        Lists changed files in the working copy. Prepends files added to the index with a tick.
        :return: A list of formatted_file_path, file_path tuples representing changed working copy files.
        """
        changed_files = []
        for file in self.list_of_changed_files_in_index():
            _file_name_with_diff = ["✔ " + file.b_path, file.b_path]
            changed_files.append(_file_name_with_diff)
        for file in self.list_of_changed_unadded_files():
            _file_name_with_diff = ["  " + file.b_path, file.b_path]
            changed_files.append(_file_name_with_diff)
        for file in self.repo.untracked_files:
            _file_name_with_diff = ["  " + file, file]
            changed_files.append(_file_name_with_diff)
        return changed_files

    def toggle_add_file_to_index(self, path):
        added = [item.a_path for item in self.list_of_changed_files_in_index()]
        if path in added:
            self.repo.git.reset("--", path)
        else:
            self.repo.git.add(path)

    def commit(self, commit_message):
        self.repo.git.commit('-m {}'.format(commit_message))

    def push(self):
        origin = self.repo.remote(name='origin')
        origin.push()
