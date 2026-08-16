# AGENTS.md

Preface: All development should be conducted in Simplified Chinese.

1. Think Before Coding
   - ambiguity, assumptions, alternatives, tradeoffs

2. Simplicity and Reachability
   - minimum implementation
   - no speculative abstractions/configuration
   - no speculative feature flags/compat/migrations/wrappers
   - handle unusual cases when reachable through supported use

3. Surgical Changes
   - smallest diff
   - no unrelated cleanup

4. Goal-Driven Verification
   - explicit success criteria
   - verify material criteria
   - checks must detect a specific failure and affect the next action
   - don't repeat settled checks

5. Project Threat Model / Anti-Overdefense
   - cooperating operator unless specified otherwise
   - no unnecessary security machinery
   - hashes/fingerprints only with material benefit
   - exercise judgment instead of procedural theater
   - report real problems, including rare-but-reachable ones
   - don't manufacture findings
   - higher-priority/user/project requirements override this section

6. Commit Convention
   - before creating a commit, read and follow `CONTRIBUTING.md`
   - every new commit message must conform to Conventional Commits 1.0.0: `<type>[optional scope][optional !]: <description>`
   - for a standard GitHub two-parent merge commit, the PR title in the generated message body is the Conventional Commits header; no other merge-message exception applies
   - use `feat` for new features and `fix` for bug fixes; mark breaking changes with `!` or an uppercase `BREAKING CHANGE:` footer
   - never bypass the repository's `commit-msg` hook with `--no-verify`

7. Third-Party Asset Boundary
   - this repository does not maintain third-party originals, private image filenames, relative paths, or local mount points
   - agents and automation must not access, enumerate, hash, copy, move, restore, publish, or build from out-of-repository private backups
   - agents may maintain public source URLs, provenance text, project-owned assets, and assets with the necessary permissions
   - never add third-party originals to issues, pull requests, fixtures, builds, or releases

8. Repository Verification
   - install development dependencies from `requirements-dev.txt`
   - before handoff, run `python3 scripts/validate_docs.py` and `python3 -m unittest discover -s tests -p 'test_*.py'`
   - the tracked collectibles catalog is text-only; never restore third-party image indexes or embeds
