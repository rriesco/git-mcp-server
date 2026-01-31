# Git MCP Server Tools

This document provides reference documentation for all MCP tools provided by the Git MCP server.

## Overview

The Git MCP server provides tools for local git operations:
- Committing changes with conventional commit format
- Creating and managing branches
- Pushing and pulling to/from remote repositories
- Syncing with main branch
- Checking repository status

**Status**: Infrastructure complete (Task 4.9). Tools will be added in tasks 4.10-4.14.

## Tool Categories

### 1. Commit Operations (Task 4.10)

**Status**: Coming soon

Tools for committing changes to the repository:
- `commit`: Stage all changes and create commit with conventional format
- Support for commit types: feat, fix, docs, refactor, test, chore
- Automatic Claude Code attribution

**Replaces**:
- `github-manager/commit_changes.py`

---

### 2. Branch Management (Task 4.11)

**Status**: Coming soon

Tools for managing git branches:
- `create_branch`: Create new feature branch from main
- `switch_branch`: Switch to existing branch
- `delete_branch`: Delete local branch
- Support for conventional branch naming (issue-N-description, feature-, fix-, etc.)

**Replaces**:
- `github-manager/create_feature_branch_from_main.py`

---

### 3. Remote Operations (Task 4.12)

**Status**: Coming soon

Tools for pushing and pulling:
- `push`: Push current branch to remote
- `pull`: Pull latest changes from remote
- Automatic upstream tracking configuration
- Authentication via git credential helper

**Replaces**:
- `github-manager/push_branch.py`
- `github-manager/pull_branch.py`

---

### 4. Sync Operations (Task 4.13)

**Status**: Coming soon

Tools for syncing with main branch:
- `sync_with_main`: Fetch and merge latest main branch changes
- Conflict detection and reporting
- Automatic merge commit creation

**Replaces**:
- `github-manager/sync_with_main.py`

---

### 5. Status Operations (Task 4.14)

**Status**: Coming soon

Tools for checking repository status:
- `git_status`: Get current repository status
- Reports: current branch, uncommitted changes, untracked files, ahead/behind remote
- Structured status information for programmatic use

**Replaces**:
- Manual `git status` commands

---

## Tool Usage Examples

**Note**: Examples will be added as tools are implemented in tasks 4.10-4.14.

### Example: Commit Changes (Task 4.10)

```python
# Will be available after Task 4.10
result = commit(
    type="feat",
    message="implement query helper functions",
    skip_preview=True
)
```

### Example: Create Branch (Task 4.11)

```python
# Will be available after Task 4.11
result = create_branch(
    issue_number=42,
    description="add-feature-x"
)
```

### Example: Push to Remote (Task 4.12)

```python
# Will be available after Task 4.12
result = push(
    set_upstream=True
)
```

### Example: Sync with Main (Task 4.13)

```python
# Will be available after Task 4.13
result = sync_with_main()
```

### Example: Check Status (Task 4.14)

```python
# Will be available after Task 4.14
status = git_status()
print(status["branch"])
print(status["changes"])
```

---

## Error Handling

All tools use structured error handling via `GitError`:

```python
@dataclass(frozen=True)
class GitError:
    error_type: str      # Classification (e.g., "merge_conflict")
    message: str         # Human-readable error message
    suggestion: str      # Actionable suggestion for fixing
    command: str | None  # Optional command to run
```

### Common Error Types

| Error Type | Cause | Suggestion |
|------------|-------|------------|
| `not_a_repo` | Not in git repository | Navigate to a git repository |
| `auth_failed` | Git authentication failed | Check credentials or SSH key |
| `merge_conflict` | Merge conflict detected | Resolve conflicts and commit |
| `detached_head` | Detached HEAD state | Create or checkout a branch |
| `nothing_to_commit` | No changes to commit | Make changes before committing |
| `no_remote` | No remote configured | Add remote with `git remote add` |
| `git_command_failed` | Generic git error | Check error message and git status |
| `validation_error` | Invalid input | Verify input parameters |
| `unknown_error` | Unexpected error | Check error message, report if needed |

---

## Architecture

### Git Client Singleton

All tools share a singleton Git repository instance:

```python
from git_mcp_server.utils import get_repo

repo = get_repo()  # Returns singleton Repo instance
# All subsequent calls return same instance
```

Benefits:
- Single source of truth for repository state
- Performance (avoid re-initialization)
- Consistent state across all tools

### Type Safety

All tools use:
- Full type hints (mypy strict mode)
- Pydantic models for complex parameters
- Structured return types (dictionaries with known keys)

---

## Testing

All tools will include:
- **Unit tests**: Mock git operations, test logic
- **Integration tests**: Real git repositories, end-to-end validation
- **>90% coverage**: Comprehensive test coverage target

---

## Version History

### Version 0.1.0 (Task 4.9 - Infrastructure)
- Initial infrastructure setup
- Git client singleton (`get_repo`, `reset_repo`)
- Structured error handling (`GitError`, `handle_git_error`)
- FastMCP server initialization
- Comprehensive test suite (79 tests, 100% utils coverage)

### Future Versions

- **0.2.0** (Task 4.10): Commit operations
- **0.3.0** (Task 4.11): Branch management
- **0.4.0** (Task 4.12): Remote operations
- **0.5.0** (Task 4.13): Sync operations
- **1.0.0** (Task 4.14): Status operations - First stable release

---

## Additional Resources

- [Git MCP Server README](../README.md) - Setup and installation
- [GitHub MCP Server Tools](../../github-mcp-server/docs/mcp-tools.md) - GitHub API tools
- [MCP Migration Guide](../../docs/mcp-migration-guide.md) - Migration from scripts
- [Test Patterns](../../docs/test-patterns.md) - Testing guidelines

---

**Last Updated**: Task 4.9 Complete (Infrastructure) - January 2026
