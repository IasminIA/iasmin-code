# Contributing to iasmin-code

## Workflow
1. Branch off origin/main for any change:
   `git checkout -b feat/my-change origin/main`
2. Commit on the feature branch with Conventional Commits. Multiple commits fine.
3. Push and open a PR:
   `git push -u origin feat/my-change`
   `gh pr create`
4. Request @xavierosee as reviewer.
5. Merge only after approval and green CI.

## Never push directly to main
Hotfixes too. Branch `hotfix/<thing>` → PR. The audit trail and CI pass are worth it.

## Merge strategy
- Rebase-merge only. Never squash.

## Hooks
Install once per clone: `bash scripts/install-git-hooks.sh`. This sets
`core.hooksPath .githooks` (portable, repo-relative). Never bypass with
`--no-verify`.

## Runtime files
.gitignore covers generated artifacts. If git status shows runtime files as
untracked, extend .gitignore rather than committing them.
