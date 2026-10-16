"""Interactive REPL loop for iasmin.

This is the local shell only. It reads one prompt at a time and waits for
the handler to return before prompting again (staggered, one-at-a-time
interaction). The handler is injected as a callback so the remote-brain
transport (issue #10) can plug in without touching this module.
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import Awaitable, Callable

PROMPT = "iasmin> "
EXIT_TOKENS = {"/exit", "/quit", "exit", "quit"}


async def repl_loop(handle_line: Callable[[str], Awaitable[None]]) -> None:
    """Run the interactive loop until EOF, Ctrl-C, or an exit token.

    Args:
        handle_line: Awaitable callback invoked with each non-empty line.
            Its return value is printed to stdout; the loop waits for it
            before reading the next prompt.
    """

    while True:
        try:
            line = input(PROMPT)
        except EOFError:
            print()
            return
        except KeyboardInterrupt:
            print()
            continue

        line = line.strip()
        if not line:
            continue

        if line.lower() in EXIT_TOKENS:
            return

        try:
            result = await handle_line(line)
        except KeyboardInterrupt:
            print()
            continue

        if result is not None:
            print(result)


def run(handle_line: Callable[[str], Awaitable[None]]) -> None:
    """Synchronous wrapper that drives ``repl_loop`` on the event loop."""

    try:
        asyncio.run(repl_loop(handle_line))
    except KeyboardInterrupt:
        print(file=sys.stderr)
        sys.exit(0)