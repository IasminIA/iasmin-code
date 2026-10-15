# Shared-core extraction — context

Issue: #6
Recon verified 2026-10-15 (authoritative dependency map — do not re-verify).

## Why
Extract a shared core from the monorepo `IasminIA/iasmin` into a versioned shared library, consumed by both the deploy tree (the live Pi agent) and the new CLI repo (`iasmin-code`). Today the CLI would otherwise need to duplicate (or reach into) `agent/` internals to reuse `loop`, `tool_loop`, `llm`, `context`, `skills`, `mcp_client`, `tier_router`, and `alerts`. A single versioned component keeps one source of truth and a clean dependency direction: shared core ← deploy tree; shared core ← CLI.

## Modules in scope
`alerts`, `llm`, `tool_loop`, `mcp_client`, `context`, `skills`, `tier_router`, `loop` (the full list from issue #6).

## Recon findings (authoritative dependency map, verified 2026-10-15)

- **Leaf modules with NO agent-internal deps**: `context.py`, `skills.py`, `tier_router.py`, `alerts.py`, `webauthn.py`.
- `mcp_client.py` → `alerts.py` (top-level hard dep).
- `llm.py` → `alerts.py` (lazy only, line 384, guarded to avoid circular).
- `tool_loop.py` → `llm.py` only.
- `loop.py` → `context.py`, `llm.py`, `mcp_client.py`, `skills.py` + lazy: `main.py` (`TASK_PROMPTS`, line 442), `context.py` (`find_skill`, line 493), `tier_router.py` (`classify_tier`, line 502).
- `channels.py` → `loop.py`, `tone_guard.py` + lazy `cards`/`tier_router`/`context`/`mcp_client`.
- `session_app.py` → `loop.py`, `webauthn.py`.
- `main.py` → absolute lazy: `dream_cycle`, `apartment_nudge`, `discogs_sync`, `loop`, `channels`, `github_webhook`, `session_app`.
- Code MCP server (`mcp-servers/code/server.py`) imports ONLY `agent.llm.LLMClient` + `agent.tool_loop.run_tool_loop` — clean extraction surface; does NOT need `loop.py`.
- `agent/__init__.py` is empty (0 bytes). All deps via relative (`.x`) or absolute (`agent.x`) imports.
- Circular edges already guarded lazy: `loop↔main` (`TASK_PROMPTS`), `llm→alerts`. Both function-local, low risk.

## Key risk
The deploy tree must keep working at every commit. Extraction must be incremental — never break in-tree imports mid-migration.

## Dependency-safe ordering
`alerts` → `llm` → `tool_loop`; `mcp_client` → `alerts`; `loop` → (`context`, `llm`, `mcp_client`, `skills`, `tier_router`, `alerts`).

## Open question (blocker for execution)
WHERE does the shared library live and how is it versioned/consumed?

Options:
- (A) new repo `IasminIA/iasmin-core`
- (B) subdirectory/packages inside `iasmin-code`
- (C) private PyPI / git dependency

Recording this as a pending question for Xavier, since issue #6 does not specify it.
