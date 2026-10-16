"""iasmin — terminal CLI agent.

A Claude-Code-faithful local runner with a remote brain on the Pi
(reached later via SSH tunnel, issue #10). This package is the thin
client shell: REPL + one-shot modes and the local interaction loop. The
reasoning/memory/MCP servers stay on the Pi; tools, executor, transport,
sessions, and commands are separate issues (#8-#12) and wire in later.
"""

__version__ = "0.1.0"

__all__ = ["__version__"]