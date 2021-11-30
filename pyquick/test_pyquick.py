"""Test cases for pyquick."""

from argparse import Namespace
from pathlib import Path
from tempfile import TemporaryDirectory

from ptpython import embed

from pyquick.quick import Quick


def test_pyquick() -> None:
    """
    Test pyquick. Manual test unfortunately.
    """
    with TemporaryDirectory() as tmpdir:
        q = Quick(
            Namespace(
                dry_run=False,
                inject=False,
                path=Path(tmpdir),
                non_interactive=False,
            )
        )
        q.run()
        print(f"Env is at {tmpdir}")
        good = False
        embed(globals(), locals())
        assert good, "Please set `good=True` if everything looks OK."


if __name__ == "__main__":
    test_pyquick()
