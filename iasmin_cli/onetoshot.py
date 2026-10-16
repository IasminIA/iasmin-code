"""One-shot and entry-point handling for iasmin.

Issue #7 scaffold: the handler is a placeholder that echo-prints the prompt
back. The real brain arrives with the SSH transport (issue #10), at which
point the placeholder below is replaced by a call into the remote agent.
"""

from __future__ import annotations

import sys

from iasmin_cli import repl


async def handle_prompt(prompt: str) -> str:
    """Placeholder handler: echo the prompt back.

    Wired to the remote brain in issue #10. Kept trivial and separate so
    the transport can drop in without touching the REPL loop.
    """

    return prompt


async def run_one_shot(prompt: str) -> None:
    """Run a single prompt through the handler and print the result."""

    print(await handle_prompt(prompt))


def main() -> None:
    """Entry point: one-shot with argv[1], else fall back to the REPL."""

    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        import asyncio

        asyncio.run(run_one_shot(prompt))
    else:
        repl.run(handle_prompt)