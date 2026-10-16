# Plan — switch CLI dependency to iasmin-core wheel from pypiserver

Backing: #20. Branch: feat/20-wheel-pypiserver.

1. Verify iasmin-core wheel is on the pypiserver index (from #14 manual release) first.
2. Add read-only pypiserver index token as Actions secret, e.g. PYPISERVER_READ_TOKEN.
   Least-privilege; write auth never shipped to a consumer.
3. Declare pypiserver index in pyproject via [[tool.uv.index]] (+ [tool.uv.sources] if
   needed), pointing at the VERIFIED pypiserver install URL. Check uv docs at execution.
4. Change dependency: remove git+ URL, add iasmin-core==<version> from that index.
5. Regenerate uv.lock. Ensure ci.yml passes the read token to uv so the test job resolves
   the private index in CI.
6. Commit + push feat/20-wheel-pypiserver, open PR (reviewer xavierosee). CI green — test
   job must install the wheel from pypiserver, not git.
7. Flag to Xavier whether IASMIN_CORE_GH_PAT (source-read) should be kept or removed.

## Acceptance criteria
- [ ] pyproject no longer references a git+ URL for iasmin-core.
- [ ] uv.lock resolves iasmin-core from the pypiserver index.
- [ ] CI test job installs the wheel from the index with the read token and passes.
- [ ] No source-repo read needed by iasmin-code.
