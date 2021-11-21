from tempfile import TemporaryDirectory
from pyquick.quick import Quick
from pathlib import Path
from argparse import Namespace


def test_pyquick() -> None:
    """
    Test pyquick.
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


if __name__ == "__main__":
    test_pyquick()
