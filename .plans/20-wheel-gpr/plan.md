# Plan — switch CLI dependency to iasmin-core wheel from GPR

Backing issue: #20. Branch: feat/20-wheel-gpr.

1. Verify iasmin-core wheel exists on GPR (from #14 manual release exercise) before switching.
2. Add read-scoped GPR token as Actions secret (packages:read on IasminIA's GPR iasmin-core
   package). Name it e.g. GPR_READ_TOKEN. Verify scope exactly; a PAT's scope is fixed at
   creation — if IASMIN_CORE_GH_PAT cannot be extended, create a new one.
3. Declare the GPR index in pyproject via [[tool.uv.index]] (+ [tool.uv.sources]); point at
   https://pypi.github.com/IasminIA/index/ with explicit=true for the private package.
   Verify exact syntax against uv docs at execution time (do not trust memory).
4. Change dependency: remove the git+https URL, add iasmin-core==<version> sourced from the
   GPR index.
5. Regenerate uv.lock with the new index. Ensure ci.yml provides the read token to uv
   (env / .netrc / uv config), and that uv resolves the private index in CI.
6. Commit + push feat/20-wheel-gpr, open PR (reviewer xavierosee). Watch CI green — the
   test job must resolve iasmin-core from GPR, not git.
7. The old IASMIN_CORE_GH_PAT (source-read) becomes unused for iasmin-core once switched;
   decide whether to keep or remove (flag to Xavier).

## Acceptance criteria
- [ ] pyproject no longer references a git+ URL for iasmin-core.
- [ ] uv.lock resolves iasmin-core from the GPR index.
- [ ] CI test job installs the wheel from GPR with the read token and passes.
- [ ] No source-repo read needed by iasmin-code (token usage confirmed).