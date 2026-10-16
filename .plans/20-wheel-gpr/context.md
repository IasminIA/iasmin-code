# Context — CLI dep → iasmin-core wheel from GPR (issue #20)

## The problem
iasmin-code depends on iasmin-core via git+https://...@v0.1.0 + fine-grained PAT
(IASMIN_CORE_GH_PAT, repo-scoped read on iasmin-core only). Once iasmin-core publishes
a wheel to GPR (issue #14), switch the CLI to depend on iasmin-core==<version> from the
GPR index so the build pulls a compiled wheel and never reaches the private source repo.

## Locked decisions
1. GPR per-repository read index: https://pypi.github.com/IasminIA/index/
2. Read auth = read-scoped GPR token (packages:read on iasmin-core's GPR package). New
   secret in iasmin-code CI (replaces the IASMIN_CORE_GH_PAT source-read use once dep switches).
3. uv multi-index / tool.uv.sources declares the private index.
4. Dep line becomes iasmin-core==<version> (no git ref).

## Current dep (verified)
pyproject.toml dependency: iasmin-core via git+https + ${IASMIN_CORE_GH_PAT}
interpolated in ci.yml (uv doesn't expand ${VAR} in pyproject URLs — lesson already logged).
ci.yml test job: setup-uv + uv sync --extra dev + uv run pytest.

## Points to pin in plan.md
- Exact uv index syntax ([[tool.uv.index]] with name/url/explicit, [tool.uv.sources]
  iasmin-core = { index = "gpr" } or similar). Do not trust memory — check uv docs during
  execution.
- Where the read token lives (Actions secret) and whether it replaces or joins
  IASMIN_CORE_GH_PAT.
- Whether the existing IASMIN_CORE_GH_PAT can be re-scoped to packages:read instead of
  adding a new secret (prefer reuse if scope allows — but it was created read-only on
  contents only; a PAT's scope is fixed at creation, so a NEW PAT or re-scoped one is needed).
- uv.lock regeneration after dep switch.