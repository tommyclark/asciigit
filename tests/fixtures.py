from datetime import datetime

from git import Repo, Head, Diff, Commit, IndexFile
from pydriller import RepositoryMining
from pydriller.domain.developer import Developer


class MockDiff(Diff):
    def __init__(self, path):
        self.b_path_attr = path
        self.a_path_attr = path

    def __eq__(self, other):
        return self.b_path == other.b_path and\
               self.a_path == other.a_path

    @property
    def b_path(self):
        return self.b_path_attr

    @property
    def a_path(self):
        return self.a_path_attr

    @property
    def a_mode(self): return None
    @property
    def a_blob(self): return None
    @property
    def a_rawpath(self): return None
    @property
    def b_mode(self): return None
    @property
    def b_blob(self): return None
    @property
    def b_rawpath(self): return None
    @property
    def new_file(self): return None
    @property
    def deleted_file(self): return None
    @property
    def raw_rename_from(self): return None
    @property
    def raw_rename_to(self): return None
    @property
    def diff(self): return None
    @property
    def change_type(self): return None
    @property
    def score(self): return None


class MockCommit(Commit):
    def __init__(self):
        pass

    def diff(self, other=None, paths=None, create_patch=False, **kwargs):
        if other is None:
            diff1 = MockDiff("test_1")
            diff2 = MockDiff("test_2")
            diff3 = MockDiff("test_3")
            diff4 = MockDiff("unadded_4")
            diff5 = MockDiff("unadded_5")
            return [diff1, diff2, diff3, diff4, diff5]
        elif other is 'HEAD':
            diff1 = MockDiff("test_1")
            diff2 = MockDiff("test_2")
            diff3 = MockDiff("test_3")
            return [diff1, diff2, diff3]


class MockCurrentHead(Head):
    def __init__(self):
        pass

    @property
    def name(self):
        return "sausage_branch"

    @property
    def path(self):
        return "origin sausage"

    def tracking_branch(self):
        return self

    @property
    def commit(self):
        return MockCommit()


class MockAlternateHead(Head):
    def __init__(self):
        pass

    @property
    def name(self):
        return "bacon_branch"

    @property
    def path(self):
        return "origin bacon"

    def tracking_branch(self):
        return self


class MockNonTrackingHead(Head):
    def __init__(self):
        pass

    @property
    def name(self):
        return "not_tracking_branch"

    @property
    def path(self):
        return "origin tracking"

    def tracking_branch(self):
        return None


class MockGit(object):
    repository = None
    added_files = []
    reset_files = []
    message = ""

    def __init__(self, repo):
        self.repository = repo

    def checkout(self, head):
        self.repository.active_branch = head

    def add(self, path):
        self.added_files.append(path)

    def reset(self, arg, path):
        self.reset_files.append(path)

    def commit(self, message):
        self.message = message


class MockIndex(IndexFile):
    def __init__(self):
        pass

    @staticmethod
    def diff(other=None, paths=None, create_patch=False, **kwargs):
        if other is None:
            diff4 = MockDiff("unadded_4")
            diff5 = MockDiff("unadded_5")
            return [diff4, diff5]
        elif other is 'HEAD':
            diff1 = MockDiff("test_1")
            diff2 = MockDiff("test_2")
            diff3 = MockDiff("test_3")
            return [diff1, diff2, diff3]


class MockRemote:
    def __init__(self):
        self.pushed = False

    def push(self, refspec=None, progress=None, **kwargs):
        self.pushed = True


class MockRepository(Repo):
    heads = [MockCurrentHead(), MockAlternateHead(), MockNonTrackingHead()]
    active_branch = heads[0]
    head = heads[0]
    index = MockIndex
    git = None
    # alias for heads
    branches = heads
    untracked_files = ["untracked_file"]

    def __init__(self):
        self.git = MockGit(self)
        self.mock_remote = MockRemote()

    def remote(self, name='origin'):
        return self.mock_remote


class MockRepositoryMiner(RepositoryMining):
    def __init__(self):
        pass

    def traverse_commits(self):
        date = datetime(1999, 3, 3)
        commit1 = MockRepositoryMinerCommit("hash1", "msg1", "name1", date)
        commit2 = MockRepositoryMinerCommit("hash2", "msg2", "name2", date)
        commit3 = MockRepositoryMinerCommit("hash3", "msg3", "name3", date)
        commit4 = MockRepositoryMinerCommit("hash4", "msg4", "name4", date)
        return [commit1, commit2, commit3, commit4]


class MockRepositoryMinerCommit:
    def __init__(self, hash, msg, name, date):
        self.hash = hash
        self.msg = msg
        self.author = Developer(name, "")
        self.author.name = name
        self.author_date = date
        self.modifications = [MockRepositoryMinerCommitModification(), MockRepositoryMinerCommitAltModification()]


class MockRepositoryMinerCommitModification:
    def __init__(self):
        self.new_path = "test_path"
        self.diff = "test_diff"


class MockRepositoryMinerCommitAltModification:
    def __init__(self):
        self.new_path = "alt_test_path"
