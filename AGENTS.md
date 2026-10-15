# AGENTS.md — iasmin-code governance

Operating conventions for this repo. Source of truth: the shared
code-vault conventions (~/repos/GarnetSeal/code-vault/conventions/). This
file distills what applies to this repo.

## Branch naming
- NEVER commit or push directly to `main`. Enforced by git hooks.
- Branches: `<type>/<kebab-case-slug>` — feat/, fix/, chore/, docs/, refactor/.
- One concern per branch; short-lived, single-purpose.

## Commits — Conventional Commits
- `type(scope): lowercase subject, no trailing period`
- Max header 100 chars; body lines wrap at 72.
- Allowed types: feat, fix, chore, docs, style, refactor, test, ci, perf, revert.

## Pull requests
- Every PR answers a GitHub issue: `Closes #N` or `Ref #N`. Open the issue first if none exists.
- Request **@xavierosee** as reviewer on every PR. No merge without his approval.
- Diff under 400 lines of meaningful change. Split larger work.
- PR title follows Conventional Commits. Keep the description current.
- CI must be green before merge. A PR is not done until CI passes.
- When approved, Iasmin merges and deploys.

## Self-review before pushing
1. Run the full local test suite.
2. Run lint/typecheck.
3. `git diff <base>` — read your own diff. Would another engineer understand it in 6 months?

## Plan files
- Non-trivial handoffs: `.plans/<issue#>-<slug>/` with `context.md` (findings/why) and `plan.md` (numbered steps + verify commands + acceptance criteria).
- Commit the plan folder WITH the execution PR that fulfils it.
- See code-vault convention plan-files-in-repo.

## Deferred work
- Deferred work becomes a GitHub issue — the durable record of WHY. Never a floating TODO.

## Hooks
- Portable hooks live in `.githooks/` (repo-relative, option A). Install: `bash scripts/install-git-hooks.sh`. Never bypass with `--no-verify`.
