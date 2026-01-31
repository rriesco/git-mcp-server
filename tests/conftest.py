"""Shared fixtures for git-mcp-server tests."""

import shutil
import tempfile
from collections.abc import Generator
from pathlib import Path
from unittest.mock import Mock

import git
import pytest

from git_mcp_server.utils import reset_repo


@pytest.fixture(autouse=True)
def reset_repo_singleton() -> Generator[None, None, None]:
    """Reset the repo singleton before and after each test."""
    reset_repo()
    yield
    reset_repo()


@pytest.fixture
def mock_repo() -> Mock:
    """Create a mock GitPython Repo instance.

    Returns:
        Mock: Configured mock Repo with common git attributes
    """
    repo = Mock(spec=git.Repo)
    repo.working_dir = "/path/to/repo"
    repo.active_branch.name = "main"
    repo.is_dirty.return_value = False
    repo.untracked_files = []
    repo.head.commit.hexsha = "abc123def456"

    return repo


@pytest.fixture
def temp_git_repo() -> Generator[Path, None, None]:
    """Create a temporary git repository for integration tests.

    This fixture:
    1. Creates a temporary directory
    2. Initializes it as a git repository
    3. Configures git user (required for commits)
    4. Yields the path for use in tests
    5. Cleans up after test completes

    Yields:
        Path: Path to the temporary git repository

    Example:
        >>> def test_something(temp_git_repo):
        ...     repo = git.Repo(temp_git_repo)
        ...     assert repo.git_dir.endswith('.git')
    """
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    try:
        # Initialize git repo
        repo = git.Repo.init(temp_path)

        # Configure git user (required for commits)
        with repo.config_writer() as config:
            config.set_value("user", "name", "Test User")
            config.set_value("user", "email", "test@example.com")

        yield temp_path

    finally:
        # Clean up
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def non_git_dir() -> Generator[Path, None, None]:
    """Create a temporary directory that is NOT a git repository.

    This fixture is used for testing error cases where the code
    operates outside of a git repository.

    Yields:
        Path: Path to the temporary non-git directory

    Example:
        >>> def test_error_outside_repo(non_git_dir):
        ...     os.chdir(non_git_dir)
        ...     with pytest.raises(ValueError):
        ...         get_repo()
    """
    temp_dir = tempfile.mkdtemp()
    temp_path = Path(temp_dir)

    try:
        yield temp_path
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def git_repo_with_files(temp_git_repo: Path) -> Generator[Path, None, None]:
    """Create a temporary git repository with some initial commits.

    This fixture extends temp_git_repo by:
    1. Creating initial test files
    2. Creating initial commits
    3. Setting up branches for testing

    Yields:
        Path: Path to the repository with files

    Example:
        >>> def test_with_commits(git_repo_with_files):
        ...     repo = git.Repo(git_repo_with_files)
        ...     assert len(list(repo.iter_commits())) > 0
    """
    # Create initial file
    test_file = temp_git_repo / "test.txt"
    test_file.write_text("initial content")

    repo = git.Repo(temp_git_repo)
    repo.index.add([str(test_file)])
    repo.index.commit("Initial commit")

    # Create another file and commit
    test_file2 = temp_git_repo / "test2.txt"
    test_file2.write_text("more content")
    repo.index.add([str(test_file2)])
    repo.index.commit("Second commit")

    yield temp_git_repo
