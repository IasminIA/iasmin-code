# iasmin-code — agent routing

Terminal CLI agent repo. This is the CLAUDE.md for agents working in this
repo.

## Skill routing
When a request matches an available skill, invoke it as the FIRST action:
- Product ideas / "is this worth building" → office-hours
- Bugs / errors / "why is this broken" → investigate
- Ship / deploy / push / create PR → ship
- Code review / check my diff → review
- Architecture review → plan-eng-review
- Save progress / checkpoint → checkpoint
- Code quality / health check → health

## Workflow
- Branch off origin/main: `git nb <slug>` (or `git checkout -b feat/<slug> origin/main`).
- Never commit or push to main — enforced by hooks.
- PR → request @xavierosee → CI green → approval → Iasmin merges.
- See AGENTS.md for full governance.
