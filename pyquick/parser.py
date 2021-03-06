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
        self.parser = ArgumentParser(
            prog="pyquick", description="A tool for quickly creating python projects."
        )
        self.add_optional()

    def add_optional(self) -> None:
        """
        Add positional arguments.
        """
        self.parser.add_argument(
            "--dry-run",
            "-D",
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
            action="store_true",
            default=False,
            required=False,
            help="Whether to run pyquick in interactive mode.",
        )

        self.parser.add_argument(
            "--dependency",
            "-d",
            metavar="DEP",
            action="append",
            nargs="*",
            default=[],
            required=False,
            help="Add a dependency to the project.",
        )

        self.parser.add_argument(
            "--upgrade",
            "-u",
            action="store_true",
            default=False,
            required=False,
            help="Perform a self-update of pyquick.",
        )

        self.parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            default=False,
            required=False,
            help="Print out more information, particularly from subcommands.",
        )
        self.parser.add_argument(
            "--path",
            "-p",
            type=Path,
            required=False,
            default=None,
            help="Path to the directory to set up or quicken.",
        )

    def parse(self) -> Namespace:
        """
        Perform parsing of command line arguments.
        """
        return self.parser.parse_args()
