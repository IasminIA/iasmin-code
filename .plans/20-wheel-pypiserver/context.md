# Context — CLI dep → iasmin-core wheel from pypiserver (issue #20)

## The problem
iasmin-code depends on iasmin-core via git+https://...@v0.1.0 + fine-grained PAT
(IASMIN_CORE_GH_PAT). Once iasmin-core publishes a wheel to the self-hosted pypiserver
(index host per issue #14), switch the CLI to iasmin-core==<version> from that index,
so it never reaches the private source repo.

## Locked decisions
1. Index = self-hosted pypiserver on the Pi behind Cloudflare Tunnel (NOT GitHub Packages
   — no PyPI registry there, retired API; verified 2026-10-16).
2. Read auth = read-only token for the pypiserver index (separate from the publish write
   token; least-privilege).
3. uv multi-index declares the private index.
4. Dep becomes iasmin-core==<version> (no git ref).

## Current dep (verified)
pyproject depends on iasmin-core via git+https + ${IASMIN_CORE_GH_PAT} interpolated in
ci.yml (uv cannot expand ${VAR} in pyproject URLs — logged lesson). ci.yml test job:
setup-uv + uv sync --extra dev + uv run pytest.

## Execution pins (verify live)
- Exact uv index/source syntax ([[tool.uv.index]] / [tool.uv.sources]) — check uv docs.
- Where the read token lives (Actions secret), e.g. PYPISERVER_READ_TOKEN.
- Whether IASMIN_CORE_GH_PAT (source-read) is retired after switch — flag to Xavier.
- uv.lock regeneration after dep switch.
