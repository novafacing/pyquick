"""Initialize repository and python projects."""

from logging import getLogger
from argparse import Namespace
from typing import Optional, cast, List
from pathlib import Path
from configparser import ConfigParser
from pyquick.defaults import PYPROJECT, GITIGNORE, PRE_COMMIT
from multiprocessing import Process
from os import chdir
from platform import python_version

# I've been defeated sadly #TODO: Figure out clikit/cleo
from subprocess import run


from git import Repo
from git.exc import InvalidGitRepositoryError
from git.objects.util import Actor
from clikit.io.console_io import ConsoleIO
from poetry.poetry import Poetry
from poetry.factory import Factory
from poetry.installation.installer import Installer
from poetry.utils.env import EnvManager
from poetry.console.commands.init import InitCommand
from poetry.core.packages.project_package import ProjectPackage
from pre_commit.main import main as pre_commit_main
from yaml import dump


class Quick:
    """Initializer for repository and python projects."""

    def __init__(self, args: Namespace) -> None:
        """
        Initialize the...initializer.

        :param args: Arguments from CLI.
        """
        self.sanity_check_args(args)
        self.logger = getLogger(__name__)

    def sanity_check_args(self, args: Namespace) -> None:
        """
        Sanity check arguments.

        :param args: Arguments from CLI.
        """
        self.dry: bool = args.dry_run
        self.inject: bool = args.inject
        self.path: Path = args.path
        self.non_interactive: bool = args.non_interactive
        self.dependencies: List[str] = args.dependency
        self.repo: Optional[Repo] = None
        self.poetry = Optional[Poetry]
        self.cio = Optional[ConsoleIO]
        self.installer = Optional[Installer]
        self.config = Optional[ConfigParser]

    def setup_repo(self) -> None:
        """Check for an existing repo and create one if not found."""

        if not self.path.exists():
            self.logger.info(f"Path {str(self.path)} does not exist. Creating it.")
            if not self.dry:
                self.path.mkdir(parents=True, exist_ok=False)

        if not self.dry:
            try:
                self.repo = Repo(self.path)
                if self.repo.is_dirty() and self.inject:
                    self.logger.error(
                        "Repo is dirty and inject is set to True. "
                        "Please commit your changes.\n"
                        "Aborting."
                    )
                self.repo.git.checkout("-b", "main")
            except InvalidGitRepositoryError:
                self.logger.info(
                    f"No git repo found at {str(self.path)}. Creating one."
                )
                if not self.dry:
                    self.repo = Repo.init(self.path)

    def init_pyproject(self) -> None:
        """
        Initialize pyproject.toml.

        Warning! Only run as mp Process, this does chdir.
        """
        self.logger.info("Initializing pyproject.toml on command line.")
        actor = Actor.author()
        run(
            (
                "poetry init "
                "--author "
                f"'{actor.name} <{actor.email}>' "
                "--name "
                f"'{self.path.name}' "
                "--python "
                f"'{python_version()}'"
            )
            + (" ".join(f"--dependency={dep}" for dep in self.dependencies))
            + (" -n" if self.non_interactive else ""),
            shell=True,
            check=True,
            cwd=self.path,
        )

    def write_pyproject(self) -> None:
        """
        Write pyproject.toml to the repo.
        """

        self.logger.info("No pyproject.toml found. Creating one.")

        if not self.dry:
            self.config = ConfigParser()
            pyproject = self.path / "pyproject.toml"

            self.init_pyproject()

            self.config.read(pyproject)

            assert (
                "tool.poetry" in self.config
            ), "Failed to read newly created pyproject.toml"

            self.config.read_dict(PYPROJECT)
            self.config.write(pyproject.open("w"))

    def update_pyproject(self) -> None:
        """
        Update an existing pyproject.toml
        """
        # TODO: When this is actually useful...
        raise NotImplementedError("Update of pyproject.toml not implemented.")

    def setup_poetry(self) -> None:
        """
        Setup poetry.
        """
        pyproject = self.path / "pyproject.toml"
        if not pyproject.exists():
            self.write_pyproject()
        else:
            self.update_pyproject()

    def init_poetry(self) -> None:
        """
        Initialize poetry.
        """

        self.logger.info("Initializing poetry.")
        if not self.dry:
            try:
                self.poetry = Factory().create_poetry(self.path)
            except RuntimeError as e:
                self.logger.error(
                    "Poetry could not be initialized. Probably there is no pyproject.toml. "
                    "Are you running with --dry-run?"
                )
                with (self.path / "pyproject.toml") as pyproject:
                    self.logger.error(pyproject.read_text())
                raise e

            cast(ConfigParser, self.config)
            cast(Poetry, self.poetry)

            def strip_quote(s: str) -> str:
                """Strip quotes from string."""
                return s.strip('"').strip("'")

            env_manager = EnvManager(poetry=self.poetry)
            env = env_manager.create_venv(ConsoleIO())
            io = ConsoleIO()
            io.is_decorated = lambda: True
            io.output.is_decorated = lambda: True
            installer = Installer(
                io=io,
                env=env,
                package=ProjectPackage(
                    strip_quote(self.config.get("tool.poetry", "name")),
                    strip_quote(self.config.get("tool.poetry", "version")),
                    strip_quote(self.config.get("tool.poetry", "version")),
                ),
                locker=self.poetry.locker,
                pool=self.poetry.pool,
                config=self.poetry.config,
            )

            installer.run()

    def setup_gitignore(self) -> None:
        """
        Setup .gitignore.
        """
        self.logger.info("Creating .gitignore")
        if not self.dry:
            if not (self.path / ".gitignore").exists():
                with (self.path / ".gitignore").open("w") as gitignore:
                    gitignore.write(GITIGNORE)
            else:
                self.logger.warning(".gitignore exists. Skipping.")

    def setup_structure(self) -> None:
        """
        Sets up a directory structure.
        """
        self.logger.info("Setting up directory structure.")
        if not self.inject and not self.dry:
            (self.path / "README.md").touch()

            self.setup_gitignore()

            package = self.path / self.path.name
            package.mkdir(parents=True, exist_ok=False)
            (package / "__init__.py").touch()
            (package / "__main__.py").touch()

    def install_precommit(self) -> None:
        """
        Install pre-commit.

        Warning! Only run as mp Process, this does chdir.
        """
        self.logger.info("Installing pre-commit.")
        if not self.dry:
            chdir(self.path)
            pre_commit_main(["install"])

    def setup_precommit(self) -> None:
        """
        Setup pre-commit.
        """
        self.logger.info("Setting up pre-commit.")
        if not self.dry:
            pre_commit_yml = self.path / ".pre-commit-config.yaml"
            if not pre_commit_yml.exists():
                with pre_commit_yml.open("w") as pre_commit:
                    dump(PRE_COMMIT, pre_commit, default_flow_style=False)
            else:
                self.logger.warning(".pre-commit-config.yaml exists. Skipping.")
            installer = Process(target=self.install_precommit)
            installer.start()
            installer.join()

    def run(self) -> None:
        """Perform actual setup of the project."""

        self.setup_repo()
        self.setup_poetry()
        self.init_poetry()
        self.setup_structure()
        self.setup_precommit()
