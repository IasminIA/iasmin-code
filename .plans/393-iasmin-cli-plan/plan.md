# Iasmin CLI — build plan

Branch convention: plan PR is `docs/iasmin-cli-plan`. Execution PRs will branch off origin/main as `<type>/<slug>`.

## Execution steps (post-approval)

0. Shared-core extraction: create the shared library package from `agent/tool_loop.py` + `agent/loop.py` + `llm`/`context`/`skills`/`mcp_client`/`tier_router` (+ `alerts` optional), publish/version it, and have the deploy tree consume it via the package rather than in-tree imports. Note maintenance cost explicitly: a versioned shared component, pinned by version.
1. Scaffold: inside the NEW repo `IasminIA/iasmin-cli`, new Python package `cli/` (or `iasmin_cli/`) + `bin/iasmin` entry, argparse + asyncio (match agent/main.py style), with the shared core imported as a dependency.
2. Local executor: extract/reuse the shared-core tool_loop tool impls (bash/read/write/edit + read-before-edit) as a local runner module. THIS is the reusable seam for #363 — structure as standalone module with a documented interface.
3. Permission gate: three modes (ask/auto/yolo) + deny-list (rm -rf, git push -f, sudo) that persists in all modes incl. yolo.
4. Transport: auto ssh -L tunnel from client to Pi; MCP-over-HTTP (streamable-http) client to the 13 servers.
5. Session wiring: point AgentLoop/loop cache at the existing thread-aware store (via the shared library); /resume + named sessions.
6. /model + /effort commands: classify_tier + /model pinning logic; effort = thinking budget within tier.
7. REPL + one-shot: interactive loop + `iasmin "prompt"` single-shot; staggered one-at-a-time interaction.
8. Tests + CI green.

## Acceptance
Per issue #393 acceptance criteria 1-10.

## Verification commands
- `iasmin` opens REPL; `iasmin "prompt"` one-shots
- local repo read/write + local shell run on Xavier's machine
- `--yolo` full non-sudo; rm -rf / git push -f / sudo denied
- /model + /effort take effect next turn
- sessions persist + re-enterable, shared store
- 13 MCP servers work through tunnel
