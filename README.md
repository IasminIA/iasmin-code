# iasmin-code

Terminal CLI agent `iasmin` — a Claude-Code-faithful local runner with the
brain on the Pi. Runs on whatever machine Xavier invokes it from (local file
edit + shell autonomy), while reasoning, memory, and MCP servers stay on the
Pi over an SSH tunnel.

Currently in early build — the plan is open as a plan PR; the shared core
(AgentLoop, run_tool_loop) is being extracted from `IasminIA/iasmin` into a
versioned package this repo consumes.

## Status
- Plan: PR #2 (docs(plan))
- Build: shared-core extraction + CLI scaffold (not started)
- Governance: see AGENTS.md

## Layout (target)
- `iasmin_cli/` — the CLI package (REPL, --yolo, /model, /effort)
- `bin/iasmin` — entry point
- `.githooks/` — portable git hooks
- `scripts/git-hooks/` — chained enforcement hooks
