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
        dependencies = []
        for dependency_list in args.dependency:
            dependencies.extend(dependency_list)
        self.dry: bool = args.dry_run
        self.inject: bool = args.inject
        self.path: Path = args.path
        self.non_interactive: bool = args.non_interactive
        self.dependencies: List[str] = dependencies
        self.repo: Optional[Repo] = None
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
            + (
                (" " if self.dependencies else "")
                + " ".join(f"--dependency={dep}" for dep in self.dependencies)
            )
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
            with pyproject.open("w") as pf:
                self.config.write(pf)
                pf.write("\n")

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
            run("poetry install", shell=True, check=True, cwd=self.path)

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

    def initial_commit(self) -> None:
        """
        Initial commit.
        """
        self.logger.info("Initial commit.")
        if not self.dry:
            assert isinstance(self.repo, Repo)
            self.repo.git.add(all=True)
            self.repo.git.checkout("-b", "main")
            self.repo.index.commit("Initial commit")

    def run(self) -> None:
        """Perform actual setup of the project."""

        self.setup_repo()
        self.setup_poetry()
        self.init_poetry()
        self.setup_structure()
        self.setup_precommit()
        self.initial_commit()
