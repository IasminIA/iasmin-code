# Shared-core extraction — execution context

Issue: #6 (sub-issue of #1, step 0 of the build plan)

## What we're doing
Extract the shared core from the monorepo (`IasminIA/iasmin`) into a versioned shared library package consumed by BOTH the deploy tree and the new CLI repo (`IasminIA/iasmin-code`).

## Modules in scope
`alerts`, `llm`, `tool_loop`, `mcp_client`, `context`, `skills`, `tier_router`, `loop`

## Verified dependency map (recon 2026-10-15, authoritative)

Leaf modules — NO agent-internal imports:
- `context.py`, `skills.py`, `tier_router.py`, `alerts.py`, `webauthn.py`

Hard top-level deps:
- `mcp_client.py` → `alerts.py`
- `tool_loop.py` → `llm.py` (only dep)

Lazy (function-local, circular-guarded) deps:
- `llm.py` → `alerts.py` (line 384)
- `loop.py` → `main.py` (TASK_PROMPTS, line 442), `context.py` (find_skill, line 493), `tier_router.py` (classify_tier, line 502)

Chain:
- `loop.py` → `context.py`, `llm.py`, `mcp_client.py`, `skills.py` (+ lazy tier_router/main)
- `channels.py` → `loop.py`, `tone_guard.py` (+ lazy cards/tier_router/context/mcp_client)
- `session_app.py` → `loop.py`, `webauthn.py`
- `main.py` → absolute lazy: dream_cycle, apartment_nudge, discogs_sync, loop, channels, github_webhook, session_app

## Key recon facts
- Code MCP server (`mcp-servers/code/server.py`) imports ONLY `agent.llm.LLMClient` + `agent.tool_loop.run_tool_loop`. It does NOT need `loop.py`. Clean extraction surface.
- `agent/__init__.py` is empty (0 bytes); all deps via relative (`.x`) or absolute (`agent.x`) imports.
- Circular edges already guarded lazy: `loop ↔ main` (TASK_PROMPTS), `llm → alerts`. Low risk.

## Dependency-safe extraction order
`alerts` → `llm` → `tool_loop`; `mcp_client` → `alerts`; `loop` → (context, llm, mcp_client, skills, tier_router, alerts).

## Key risk
Live `agent/` modules the deploy tree imports. The deploy tree must keep working at every commit — extraction is incremental, never breaking in-tree imports mid-migration (use shims that re-export from the package).

## Open decision (blocker)
WHERE does the shared library live + how is it versioned/consumed. Issue #6 does not specify. Options: (A) new repo `IasminIA/iasmin-core`, (B) subdirectory in iasmin-code, (C) private index / git dependency. Pending Xavier.
