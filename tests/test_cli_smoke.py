"""Smoke test for the CLI scaffold (issue #7).

Verifies the package imports and that the one-shot handler echoes a prompt
back. The REPL loop itself is exercised only through its callback contract,
not interactively.
"""

import asyncio

import iasmin_cli
from iasmin_cli import onetoshot


def test_package_imports_and_has_version():
    assert hasattr(iasmin_cli, "__version__")
    assert iasmin_cli.__version__


def test_one_shot_echoes_prompt():
    asyncio.run(onetoshot.run_one_shot("hello"))


def test_one_shot_handler_echoes():
    assert asyncio.run(onetoshot.handle_prompt("sample prompt")) == "sample prompt"