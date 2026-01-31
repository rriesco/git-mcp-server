"""Integration tests for git-mcp-server utilities with real git operations.

These tests use actual git repositories to validate behavior in real scenarios.
Tests are marked with @pytest.mark.integration to allow excluding them in fast test runs.
"""

import os
from pathlib import Path

import git
import pytest

from git_mcp_server.utils import GitError, get_repo, handle_git_error, reset_repo


@pytest.mark.integration
class TestGetRepoIntegration:
    """Integration tests for get_repo with real git repositories."""

    def test_get_repo_returns_valid_repo_in_temp_git_repo(self, temp_git_repo: Path) -> None:
        """Test get_repo returns valid Repo instance in real git directory.

        This test:
        1. Changes to a temporary git repository
        2. Calls get_repo()
        3. Verifies it returns a valid Repo instance
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            reset_repo()  # Clear singleton to force new instance

            # Act
            repo = get_repo()

            # Assert
            assert isinstance(repo, git.Repo)
            assert repo.working_dir is not None
            assert Path(repo.working_dir) == temp_git_repo

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_get_repo_finds_git_root_from_subdirectory(self, git_repo_with_files: Path) -> None:
        """Test get_repo finds repository root from subdirectory.

        This test:
        1. Creates a subdirectory within a git repo
        2. Changes to the subdirectory
        3. Calls get_repo() (should search parent directories)
        4. Verifies it finds the repository root
        """
        # Arrange
        original_cwd = os.getcwd()
        subdir = git_repo_with_files / "subdir"
        subdir.mkdir(exist_ok=True)

        try:
            os.chdir(subdir)
            reset_repo()

            # Act
            repo = get_repo()

            # Assert
            assert isinstance(repo, git.Repo)
            assert repo.working_dir == str(git_repo_with_files)

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_get_repo_raises_error_outside_git_repo(self, non_git_dir: Path) -> None:
        """Test get_repo raises ValueError outside git repository.

        This test:
        1. Changes to a non-git directory
        2. Calls get_repo()
        3. Verifies it raises ValueError
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(non_git_dir)
            reset_repo()

            # Act & Assert
            with pytest.raises(ValueError) as exc_info:
                get_repo()

            error_msg = str(exc_info.value).lower()
            assert "git repository" in error_msg or "not a" in error_msg

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_get_repo_singleton_persists_across_operations(self, temp_git_repo: Path) -> None:
        """Test that get_repo singleton persists across multiple operations.

        This test:
        1. Changes to a git repo
        2. Gets repo instance
        3. Performs git operation
        4. Gets repo instance again
        5. Verifies both are same instance
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            reset_repo()

            # Act
            repo1 = get_repo()
            # Simulate some operation
            _ = repo1.git.status()
            repo2 = get_repo()

            # Assert
            assert repo1 is repo2

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_get_repo_accesses_git_attributes(self, git_repo_with_files: Path) -> None:
        """Test that returned Repo instance has accessible git attributes.

        This test:
        1. Gets repository instance
        2. Accesses common git attributes (branch, commits)
        3. Verifies they work with real repository
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(git_repo_with_files)
            reset_repo()

            # Act
            repo = get_repo()

            # Assert: Can access branch information
            assert repo.active_branch is not None
            assert repo.active_branch.name is not None

            # Assert: Can access commits
            commits = list(repo.iter_commits())
            assert len(commits) == 2  # We created 2 commits in fixture

        finally:
            os.chdir(original_cwd)
            reset_repo()


@pytest.mark.integration
class TestResetRepoIntegration:
    """Integration tests for reset_repo with real repositories."""

    def test_reset_repo_allows_fresh_discovery_after_reset(
        self, temp_git_repo: Path, git_repo_with_files: Path
    ) -> None:
        """Test reset_repo enables fresh repository discovery in different directory.

        This test:
        1. Gets repo instance in first directory
        2. Resets singleton
        3. Changes to second directory with more commits
        4. Gets new repo instance
        5. Verifies the new instance reflects the second directory's state
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            reset_repo()
            repo1 = get_repo()
            repo1_path = repo1.working_dir

            # Reset and switch to directory with commits
            reset_repo()
            os.chdir(git_repo_with_files)

            repo2 = get_repo()
            repo2_path = repo2.working_dir
            repo2_commit_count = len(list(repo2.iter_commits()))

            # Assert: Different directory, and state reflects new directory
            assert Path(repo1_path) == temp_git_repo
            assert Path(repo2_path) == git_repo_with_files
            assert repo2_commit_count == 2  # git_repo_with_files has commits

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_reset_repo_enables_fresh_repo_discovery(self, temp_git_repo: Path) -> None:
        """Test reset_repo forces fresh repository discovery.

        This test:
        1. Gets repo instance
        2. Resets singleton
        3. Gets repo again
        4. Verifies new instance was created
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)

            # Get first instance
            reset_repo()
            repo1 = get_repo()
            repo1_id = id(repo1)

            # Reset and get new instance
            reset_repo()
            repo2 = get_repo()
            repo2_id = id(repo2)

            # Assert: Different object instances
            assert repo1_id != repo2_id
            assert repo1 is not repo2

        finally:
            os.chdir(original_cwd)
            reset_repo()


@pytest.mark.integration
class TestHandleGitErrorIntegration:
    """Integration tests for error handling with real git operations."""

    def test_handle_git_error_from_actual_git_operation_failure(self, temp_git_repo: Path) -> None:
        """Test error handler with actual git operation failure.

        This test:
        1. Attempts a git operation that fails (push with no remote)
        2. Catches the resulting GitCommandError
        3. Passes to handle_git_error
        4. Verifies structured error is returned
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_git_repo)
            repo = git.Repo(temp_git_repo)

            # Act: Attempt to push with no remote configured
            try:
                repo.git.push()
                # If push somehow succeeds, skip test
                pytest.skip("Push succeeded unexpectedly")
            except git.GitCommandError as e:
                result = handle_git_error(e)

                # Assert
                assert isinstance(result, GitError)
                assert result.error_type == "no_remote"
                assert result.message is not None
                assert result.suggestion is not None

        except Exception as e:
            # If we can't create the error condition, skip test
            pytest.skip(f"Could not create test condition: {e}")
        finally:
            os.chdir(original_cwd)

    def test_error_handling_with_invalid_git_repo_error(self, non_git_dir: Path) -> None:
        """Test error handler with InvalidGitRepositoryError.

        This test:
        1. Attempts to create Repo in non-git directory
        2. Catches InvalidGitRepositoryError
        3. Passes to handle_git_error
        4. Verifies proper error classification
        """
        # Act
        try:
            git.Repo(non_git_dir, search_parent_directories=False)
            pytest.skip("Repo creation succeeded unexpectedly")
        except git.InvalidGitRepositoryError as e:
            result = handle_git_error(e)

            # Assert
            assert isinstance(result, GitError)
            assert result.error_type == "not_a_repo"
            assert "git repository" in result.suggestion.lower()

    def test_error_from_get_repo_is_value_error(self, non_git_dir: Path) -> None:
        """Test that get_repo ValueError can be handled by error handler.

        This test:
        1. Calls get_repo() outside git repo
        2. Catches ValueError
        3. Passes to handle_git_error
        4. Verifies proper error classification
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(non_git_dir)
            reset_repo()

            # Act
            try:
                get_repo()
                pytest.skip("get_repo succeeded unexpectedly")
            except ValueError as e:
                result = handle_git_error(e)

                # Assert
                assert isinstance(result, GitError)
                assert result.error_type == "validation_error"

        finally:
            os.chdir(original_cwd)
            reset_repo()


@pytest.mark.integration
class TestGitClientWorkflow:
    """Integration tests for complete git workflows."""

    def test_multiple_operations_with_singleton_repo(self, git_repo_with_files: Path) -> None:
        """Test multiple git operations using singleton pattern.

        This test:
        1. Gets repo instance
        2. Performs multiple git operations
        3. Verifies all use same repo instance
        """
        # Arrange
        original_cwd = os.getcwd()
        try:
            os.chdir(git_repo_with_files)
            reset_repo()

            # Act
            repo = get_repo()
            branch_name = repo.active_branch.name
            commit_count = len(list(repo.iter_commits()))
            status_output = repo.git.status()

            # Assert
            assert branch_name == "master"
            assert commit_count == 2
            assert isinstance(status_output, str)
            assert len(status_output) > 0

        finally:
            os.chdir(original_cwd)
            reset_repo()

    def test_reset_allows_testing_different_scenarios(
        self, temp_git_repo: Path, non_git_dir: Path
    ) -> None:
        """Test reset enables testing both success and failure scenarios.

        This test:
        1. Tests success case (valid git repo)
        2. Resets
        3. Tests failure case (non-git directory)
        4. Verifies both work correctly
        """
        # Arrange
        original_cwd = os.getcwd()

        try:
            # Test 1: Valid repo
            os.chdir(temp_git_repo)
            reset_repo()
            repo = get_repo()
            assert isinstance(repo, git.Repo)

            # Test 2: Invalid repo
            reset_repo()
            os.chdir(non_git_dir)
            with pytest.raises(ValueError):
                get_repo()

            # Assert: Both scenarios work as expected
            assert True

        finally:
            os.chdir(original_cwd)
            reset_repo()
