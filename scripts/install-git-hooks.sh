#!/bin/bash
# Point repo config at the portable versioned hooks (option A: repo-relative).
# Works on any clone (the monorepo used an absolute Pi deploy-tree path; this
# repo may be cloned elsewhere, e.g. on the Mac).
set -e
git config core.hooksPath .githooks
echo "core.hooksPath -> .githooks"
git config core.hooksPath

# Branch-from-origin/main helper
git config alias.nb '!f() { git fetch -q origin && git switch -c "$1" origin/main; }; f'
echo "alias.nb -> git nb <name> (branch from origin/main)"

# Delete local branches merged into origin/main
git config alias.cleanup-merged '!git fetch -q origin && git branch --merged origin/main | grep -v "^\\*" | grep -v "^  main$" | xargs -r git branch -d'
echo "alias.cleanup-merged -> deletes local branches merged into origin/main"
