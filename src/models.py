import os
from git import Repo
from pydriller import RepositoryMining


class GitBranchModel(object):
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


class GitCommitModel(object):
    def __init__(self):
        # Current branch when editing.
        self.current_id = None
        self.last_error = None

        self.dir_path = os.getcwd()
        self.repo = Repo(self.dir_path)
        assert not self.repo.bare

    def list_commits(self):
        _commits_with_info = []
        for commit in RepositoryMining(self.dir_path).traverse_commits():
            _commit_info = [commit.hash, commit.msg, commit.author.name, commit.author_date.strftime("%d/%m/%Y, %H:%M:%S")]
            _commit_info_with_hash_as_key = [_commit_info, commit.hash]
            _commits_with_info.append(_commit_info_with_hash_as_key)
        return _commits_with_info
