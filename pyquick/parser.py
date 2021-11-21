"""Parser for pyquick."""

from argparse import ArgumentParser, Namespace
from pathlib import Path


class Parser:
    """
    Parses pyquick's command-line arguments.
    """

    def __init__(self) -> None:
        """
        Initialize the parser.
        """
        self.parser = ArgumentParser(description="pyquick")
        self.add_optional()
        self.add_positional()

    def add_optional(self) -> None:
        """
        Add positional arguments.
        """
        self.parser.add_argument(
            "--dry-run",
            "-d",
            action="store_true",
            default=False,
            required=False,
            help="Print out everything that will be done without doing it.",
        )

        self.parser.add_argument(
            "--inject",
            "-i",
            action="store_true",
            default=False,
            required=False,
            help="Whether to try and inject pyquick into an existing project.",
        )

        self.parser.add_argument(
            "--non-interactive",
            "-n",
            action="store_false",
            default=True,
            required=False,
            help="Whether to run pyquick in interactive mode.",
        )

    def add_positional(self) -> None:
        """
        Add optional arguments.
        """
        self.parser.add_argument(
            "path",
            type=Path,
            help="Path to the directory to set up or quicken.",
        )

    def parse(self) -> Namespace:
        """
        Perform parsing of command line arguments.
        """
        return self.parser.parse_args()
