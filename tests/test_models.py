# coding: utf-8
import unittest
from src.models import GitBranchModel, GitCommitModel, WorkingCopyModel
from tests.fixtures import *


class TestGitBranchModel(unittest.TestCase):
    def setUp(self):
        self.branch_model = GitBranchModel.__new__(GitBranchModel)
        self.branch_model.repo = MockRepository()

    def testGetActiveBranch(self):
        branch = self.branch_model.get_current_branch()
        assert branch.name == "sausage_branch"

    def testIsActiveBranch(self):
        assert not (self.branch_model.is_current_branch(MockNonTrackingHead()))
        assert not (self.branch_model.is_current_branch(None))
        assert self.branch_model.is_current_branch(self.branch_model.get_current_branch())

    def testCheckout(self):
        assert self.branch_model.is_current_branch(MockCurrentHead())
        self.branch_model.checkout_branch(MockNonTrackingHead())
        assert self.branch_model.is_current_branch(MockNonTrackingHead())

    def testListBranches(self):
        self.branch_model.branches = self.branch_model.repo.branches

        branch_1 = ['✔ sausage_branch -> sausage_branch', MockCurrentHead()]
        branch_2 = ['  bacon_branch -> bacon_branch', MockAlternateHead()]
        branch_3 = ['  not_tracking_branch', MockNonTrackingHead()]
        expected_list = [branch_1, branch_2, branch_3]

        branches = self.branch_model.list_branches()
        assert branches is not None
        assert branches == expected_list


class TestCommitModel(unittest.TestCase):
    def setUp(self):
        self.commit_model = GitCommitModel.__new__(GitCommitModel)
        self.commit_model.repository_miner = MockRepositoryMiner()
        self.commit_model.repo = MockRepository()
        self.commit_model.current_model = None

    def testListCommits(self):
        commits = self.commit_model.list_commits()
        assert commits is not None

        commit_info1 = [['hash1', 'msg1', 'name1', '03/03/1999, 00:00:00'], commits[3][1]]
        commit_info2 = [['hash2', 'msg2', 'name2', '03/03/1999, 00:00:00'], commits[2][1]]
        commit_info3 = [['hash3', 'msg3', 'name3', '03/03/1999, 00:00:00'], commits[1][1]]
        commit_info4 = [['hash4', 'msg4', 'name4', '03/03/1999, 00:00:00'], commits[0][1]]
        commit_with_info_list = [commit_info4, commit_info3, commit_info2, commit_info1]

        assert commits == commit_with_info_list

    def testListFilesInCurrentCommit(self):
        commit = MockRepositoryMinerCommit("hash1", "msg1", "name1", datetime(1999, 3, 3))
        self.commit_model.current_commit = commit
        files = self.commit_model.list_files_in_current_commit()

        assert files == [["test_path", commit.modifications[0]],
                         ["alt_test_path", commit.modifications[1]]]

    def testRetrievingCurrentDiff(self):
        self.commit_model.current_commit_file = MockRepositoryMinerCommitModification()
        modification = self.commit_model.current_file_diff()
        assert modification == "test_diff"

    def testCheckout(self):
        assert self.commit_model.repo.active_branch != 'hash1'
        commit = MockRepositoryMinerCommit("hash1", "msg1", "name1", datetime(1999, 3, 3))
        self.commit_model.current_commit = commit
        self.commit_model.checkout_commit()
        assert self.commit_model.repo.active_branch == 'hash1'


class TestWorkingCopyModel(unittest.TestCase):
    def setUp(self):
        self.working_copy_model = WorkingCopyModel.__new__(WorkingCopyModel)
        self.working_copy_model.repo = MockRepository()

    def testListChangedFiles(self):
        changed_files = self.working_copy_model.list_of_changed_unadded_files()

        assert changed_files is not None
        assert changed_files[0].b_path == "unadded_4"
        assert changed_files[1].b_path == "unadded_5"

    def testListUnaddedFiles(self):
        changed_files = self.working_copy_model.list_of_changed_files()

        assert changed_files is not None
        assert changed_files[0].b_path == "test_1"
        assert changed_files[1].b_path == "test_2"
        assert changed_files[2].b_path == "test_3"
        assert changed_files[3].b_path == "unadded_4"
        assert changed_files[4].b_path == "unadded_5"

    def testListOfChangedFilesInIndex(self):
        changed_index_files = self.working_copy_model.list_of_changed_files_in_index()

        assert changed_index_files is not None
        assert changed_index_files[0].b_path == "test_1"
        assert changed_index_files[1].b_path == "test_2"
        assert changed_index_files[2].b_path == "test_3"

    def testInfoForTable(self):
        test_info = self.working_copy_model.changed_files_for_table()

        assert test_info is not None
        changed_file1 = ['✔ test_1', 'test_1']
        changed_file2 = ['✔ test_2', 'test_2']
        changed_file3 = ['✔ test_3', 'test_3']
        changed_file4 = ['  unadded_4', 'unadded_4']
        changed_file5 = ['  unadded_5', 'unadded_5']
        changed_file6 = ['  untracked_file', 'untracked_file']
        changed_files = [changed_file1, changed_file2, changed_file3, changed_file4, changed_file5, changed_file6]

        assert changed_files == test_info

    def testTogglingAddFiles(self):
        added_file = "test_1"
        self.working_copy_model.toggle_add_file_to_index(added_file)
        assert added_file in self.working_copy_model.repo.git.reset_files
        assert added_file not in self.working_copy_model.repo.git.added_files

        unadded_file = "unadded_4"
        self.working_copy_model.toggle_add_file_to_index(unadded_file)
        assert unadded_file in self.working_copy_model.repo.git.added_files
        assert unadded_file not in self.working_copy_model.repo.git.reset_files

    def testCommit(self):
        self.working_copy_model.commit("Hello there")
        assert self.working_copy_model.repo.git.message == "-m Hello there"

    def testPush(self):
        self.working_copy_model.push()
        assert self.working_copy_model.repo.remote("origin").pushed
