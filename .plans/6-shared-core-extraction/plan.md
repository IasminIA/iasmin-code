# Shared-core extraction — build plan

Branch convention: plan PR is `docs/6-shared-core-extraction-plan`. Execution PR will branch off `origin/main` as `feat/6-shared-core-extraction`.

## Prerequisite decision (needed before step 0)
Package location + versioning mechanism — ask in body, not in code. Default recommendation: new repo `IasminIA/iasmin-core` with a versioned PyPI-style `pyproject.toml`, consumed via git dependency or editable install.

## Execution steps (post-approval)

0. Choose/confirm package home + versioning (pend Xavier). Default: new repo `IasminIA/iasmin-core`, versioned PyPI-style `pyproject.toml`, consumed via git dependency or editable install.
1. Create the package skeleton in the chosen home; init `pyproject.toml` (name e.g. `iasmin-core`), set name/version.
2. Copy leaf modules first (`alerts`, `context`, `skills`, `tier_router`) verbatim into the package; update their internal relative imports to package-relative. Add a shim in the monorepo `agent/` that re-exports from the package, so deploy-tree imports keep working untouched.
3. Copy `llm.py` then `tool_loop.py` (ordering: `alerts` → `llm` → `tool_loop`). Update the lazy `alerts` import + `tool_loop`'s `llm` import to package imports. Shim again.
4. Copy `mcp_client.py` (depends `alerts`). Shim.
5. Copy `loop.py` (depends `context`/`llm`/`mcp_client`/`skills`/`tier_router`). Update its lazy imports (`main.TASK_PROMPTS`, `context.find_skill`, `tier_router.classify_tier`) — resolve the `loop↔main` circularity by moving `TASK_PROMPTS` into the package or a shared location, then shim.
6. Deploy-tree consumption: install the package into the Pi venv; remove in-tree duplicates and point `agent/` at the package (or keep shims). Run full pytest on deploy tree — must be green.
7. CLI repo (`iasmin-code`) imports shared core as a declared dependency (add to `pyproject.toml` deps).
8. Tests + CI green on both repos.

## Acceptance (from issue #6)
- Shared library package created + versioned.
- Deploy tree consumes via package, not in-tree.
- Deploy tree tests pass at every commit.
- CLI can import shared core as a dependency.

## Verification commands
- Run pytest in the monorepo (deploy tree) — green.
- `python -c "import iasmin_core"` smoke test.
- Confirm code MCP server still imports (`agent.llm.LLMClient` + `agent.tool_loop.run_tool_loop`).

## Maintenance-cost caveat
A versioned shared component, pinned by version — carry the overhead of cutting/pinning releases when the core changes.
