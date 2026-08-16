#!/bin/sh

set -eu

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"
git config --local core.hooksPath .githooks
printf '%s\n' '已启用 .githooks；后续 git commit 将校验 Conventional Commits 1.0.0。'
