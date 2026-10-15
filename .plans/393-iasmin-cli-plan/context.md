# Iasmin CLI — execution context

Design doc: `06_Resources/Design-Docs/iasmin-cli.md` (APPROVED 2026-10-15)
Issue: #393

## What we're building
A terminal CLI `iasmin`, Claude-Code-faithful: runs locally on whatever machine Xavier invokes it from, local file edit + shell execution, remote brain (reasoning/memory/13 MCP servers) on the Pi over SSH tunnel + MCP-over-HTTP. REPL + session mgmt, `--yolo` full non-sudo access with a persistent deny-list, `/model` + `/effort` commands, staggered one-at-a-time interaction.

## Verified current state (from spec Phase 1 recon, 2026-10-15)
- `AgentLoop(user, thread_name=DEFAULT_THREAD)` (agent/loop.py:143) — shared drive unit, thread-aware; `chat()` at line 268; session files at `agent/sessions/<user>.json` or `<user>/<slug>.json` (`_save_session` lines 213-246, `_session_path` lines 181-186).
- No channel abstraction; `_handle_message(user, text)` (agent/channels.py:157) is the dispatch layer.
- `agent/session_app.py` `_loops: dict[(user, thread_name), AgentLoop]` + `_get_loop` (lines 31/34) — the thread cache pattern. Shared thread store REUSED (decision Q2).
- Local shell execution already exists: `run_tool_loop()` (agent/tool_loop.py:118), `_bash` (line 262) `subprocess.run(shell=True, cwd, timeout=120)`, Read/Write/Edit with read-before-edit (session_reads, line 367). Code MCP (mcp-servers/code/server.py) is a thin FastMCP wrapper (port 8111).
- Tier routing callable: `classify_tier(text)` (agent/tier_router.py:42); /model pinning (channels.py:171-203); `LLMClient.model_for/known_tiers/known_models` (agent/llm.py:223-248).
- 13 MCP servers on 127.0.0.1:8100-8113 (8112 vacant). Uvicorn on 127.0.0.1:18789.
- Python 3.11.2 / .venv, Starlette 1.x, pytest. CLI style = Python argparse+asyncio (agent/main.py).

## Locked decisions
- Q1 transport: SSH tunnel + MCP-over-HTTP (client → Pi)
- Q2 sessions: reuse Session App thread store
- Q3 local-shell: arbitrary shell behind ask/auto/yolo gate + deny-list
- Language: Python (reuse AgentLoop/run_tool_loop; matches stack)
- Auth: none for local terminal (local-trust)
- Sovereignty: no US company in critical path

## Scope decision (2026-10-15): separate repo
The CLI becomes its own repo, `IasminIA/iasmin-cli` (public, committed 2026-10-15, currently empty). The shared core — `tool_loop`, `loop`, `llm`, `context`, `skills`, `mcp_client`, `tier_router`, optionally `alerts` — is extracted into a versioned shared library consumed by BOTH the deploy tree (IasminIA/iasmin) and the new CLI repo. MCP servers stay in-tree on the Pi (the CLI is only an MCP-over-HTTP client); new entry point `bin/iasmin`.

Justification:
- Clean dependency direction: the web tree imports down into the agent modules; the CLI never imports the web tree.
- Independent release cadence on two machines (Mac M4 arm64 / Fedora T2 x86).
- Unblocks #363 VSCode bridge later.

## Key architectural insight
The local-runner piece is the genuinely new part and the foundation the VSCode bridge (#363) reuses. run_tool_loop's tool impls (bash/read/write/edit) are the reusable seam — NOT the code MCP's remote path.
