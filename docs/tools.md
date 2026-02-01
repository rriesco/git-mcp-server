# Git MCP Server Tools

This document provides reference documentation for all MCP tools provided by the Git MCP server.

## Overview

The Git MCP server provides tools for local git operations:
- Committing changes with conventional commit format
- Creating and managing branches
- Pushing and pulling to/from remote repositories
- Syncing with main branch
- Checking repository status

**Status**: All tools fully implemented (v0.1.0+).

## Tool Categories

### 1. Commit Operations

**Status**: Implemented

Tools for committing changes to the repository:
- `commit`: Stage all changes and create commit with conventional format
- Support for commit types: feat, fix, docs, refactor, test, chore
- Automatic Claude Code attribution

**Replaces**:
- `github-manager/commit_changes.py`

---

### 2. Branch Management

**Status**: Implemented

Tools for managing git branches:
- `create_branch`: Create new feature branch from main
- `switch_branch`: Switch to existing branch
- `delete_branch`: Delete local branch
- Support for conventional branch naming (issue-N-description, feature-, fix-, etc.)

**Replaces**:
- `github-manager/create_feature_branch_from_main.py`

---

### 3. Remote Operations

**Status**: Implemented

Tools for pushing and pulling:
- `push`: Push current branch to remote
- `pull`: Pull latest changes from remote
- Automatic upstream tracking configuration
- Authentication via git credential helper

**Replaces**:
- `github-manager/push_branch.py`
- `github-manager/pull_branch.py`

---

### 4. Sync Operations

**Status**: Implemented

Tools for syncing with main branch:
- `sync_with_main`: Fetch and merge latest main branch changes
- Conflict detection and reporting
- Automatic merge commit creation

**Replaces**:
- `github-manager/sync_with_main.py`

---

### 5. Status Operations

**Status**: Implemented

Tools for checking repository status:
- `git_status`: Get current repository status
- Reports: current branch, uncommitted changes, untracked files, ahead/behind remote
- Structured status information for programmatic use

**Replaces**:
- Manual `git status` commands

---

## Tool Usage Examples

### Example: Commit Changes

```python
result = commit(
    type="feat",
    message="implement query helper functions",
    skip_preview=True
)
```

### Example: Create Branch

```python
result = create_branch(
    issue_number=42,
    description="add-feature-x"
)
```

### Example: Push to Remote

```python
result = push(
    set_upstream=True
)
```

### Example: Sync with Main

```python
result = sync_with_main()
```

### Example: Check Status

```python
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

### Version 0.1.0
- Initial release with all core tools implemented
- Git client singleton (`get_repo`, `reset_repo`)
- Structured error handling (`GitError`, `handle_git_error`)
- FastMCP server initialization
- Comprehensive test suite

### Version 0.1.1
- Renamed package to `rriesco-mcp-git` for PyPI publishing

### Version 0.1.2
- Fixed `uv sync --extra dev` for dev dependencies
- Fixed mypy type errors

### Version 0.1.3
- Version bump release

### Version 0.1.4
- Fix `__version__` to report correct version
- Update outdated documentation
- Remove broken links

---

## Additional Resources

- [Git MCP Server README](../README.md) - Setup and installation

---

**Last Updated**: January 2025
