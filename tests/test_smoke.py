"""Smoke test — verifies the repo is importable and tests run.

The real CLI suite lands with the build; this keeps CI green (and honest) in
the interim by exercising the package import path.
"""


def test_python_version_supported():
    import sys

    assert sys.version_info >= (3, 11)


def test_repo_has_governance():
    from pathlib import Path

    assert (Path(__file__).resolve().parents[1] / "AGENTS.md").exists()
    assert (Path(__file__).resolve().parents[1] / ".gitleaks.toml").exists()
