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
   - use `feat` for new features and `fix` for bug fixes; mark breaking changes with `!` or an uppercase `BREAKING CHANGE:` footer
   - never bypass the repository's `commit-msg` hook with `--no-verify`

7. Private Asset Boundary
   - `../assets/` is a human-maintained private store outside this repository
   - agents and automation must not access, enumerate, hash, copy, move, restore, publish, or build from `../assets/`
   - ignored PNG paths under `docs/background/02_crimson_troupe/04_collectibles/assets/collectibles/` are human-only local mounts and must never be force-added
   - agents may maintain asset filenames, relative-path metadata, provenance text, placeholders, and validators without accessing the private files
   - never record a machine-specific absolute private-asset path in tracked files
