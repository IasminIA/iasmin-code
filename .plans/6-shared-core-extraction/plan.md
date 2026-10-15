# Shared-core extraction — build plan

Branch (execution PR): `feat/6-shared-core-extraction`

## Prerequisite decision
Resolved: new private repo `IasminIA/iasmin-core`, consumed via git+SSH dependency. Deploy tree: editable/local install.

## Execution steps
0. Confirm package home + versioning (answer the open decision).
1. Create package skeleton in chosen home (done: IasminIA/iasmin-core private repo, commit 525d418); init `pyproject.toml` (name e.g. `iasmin-core`), set version.
2. Add `iasmin_core/config.py` — the `paths` object; env-var/arg injection with deploy-tree defaults.
3. Copy leaf modules first (`alerts`, `context`, `skills`, `tier_router`) verbatim; replace `__file__`-relative anchors with `iasmin_core.config` imports. Update internal relative imports to package-relative. Add monorepo `agent/` shims re-exporting from the package so in-tree imports keep working untouched.
4. Copy `llm.py` then `tool_loop.py` (order: alerts → llm → tool_loop). Update lazy alerts + tool_loop's llm imports to package imports. Shim again.
5. Copy `mcp_client.py` (depends alerts). Shim.
6. Copy `loop.py` (depends context/llm/mcp_client/skills/tier_router). Resolve `loop ↔ main` circularity by moving TASK_PROMPTS into the package (or a shared location). Shim.
7. Deploy tree consumption: install package into Pi venv; point `agent/` at the package (or keep shims). Run full pytest on deploy tree — must stay green.
8. CLI repo (`iasmin-code`) declares shared core as a dependency (add to pyproject.toml).
9. Tests + CI green on both repos.

## Acceptance (issue #6)
- Shared library package created + versioned
- Deploy tree consumes via package, not in-tree imports
- Deploy tree tests pass at every commit
- CLI repo can import the shared core as a dependency

## Verification
- pytest green in monorepo
- `python -c "import iasmin_core"` smoke test
- code MCP server still imports (llm + tool_loop)

## Caveat
Maintenance cost of a versioned shared component, pinned by version — accepted explicitly.
