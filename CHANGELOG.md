# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2025-01-31

### Fixed

- Fix CI/CD workflow: correct mypy path from `src/github_mcp_server` to `src/git_mcp_server`
- Remove outdated `github-manager/` script references from documentation

## [0.1.4] - 2025-01-31

### Fixed

- Fix `__version__` in package to report correct version
- Update outdated documentation in docs/tools.md (remove "Coming soon" references)
- Remove broken links to non-existent documentation files
- Add missing CHANGELOG entries for v0.1.1, v0.1.2, v0.1.3

## [0.1.3] - 2025-01-31

### Changed

- Version bump release

## [0.1.2] - 2025-01-31

### Fixed

- Use `uv sync --extra dev` to install dev dependencies correctly
- Fix mypy type errors

## [0.1.1] - 2025-01-31

### Changed

- Renamed package to `rriesco-mcp-git` for PyPI publishing

## [0.1.0] - 2025-01-31

### Added

- Initial release as standalone package
- **Branch Operations**: `git_create_branch` with naming conventions
- **Commit Operations**: `git_commit` with conventional commit format
- **Remote Operations**: `git_push`, `git_pull` with token authentication
- **Status Operations**: `git_status` for branch and file change info
- **Sync Operations**: `git_sync_with_main` with merge/rebase strategies
- Singleton repository pattern for consistent state
- Structured error handling with actionable suggestions
- Comprehensive test suite with unit and integration tests
- Full documentation and usage examples
