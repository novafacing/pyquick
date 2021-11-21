"""Default data for pyquick."""

from textwrap import dedent

PYPROJECT = {
    "tool.poetry.dev-dependencies": {
        "black": '"^21.11b"',
        "pylint": '"^2.11.1"',
        "isort": '"^5.10.1"',
        "pytest": '"^6.2.5"',
        "mypy": '"^0.910"',
        "pytest-cov": '"^3.0.0"',
        "poetry": '"^1.1.11"',
        "pre-commit": '"^2.15.0"',
    },
    "build-system": {
        "requires": '["poetry-core>=1.0.0"]',
        "build-backend": '"poetry.core.masonry.api"',
    },
    "tool.pylint.messages_control": {
        "max-line-length": "88",
        "disable": '["attribute-defined-outside-init", "logging-fstring-interpolation"]',  # pylint: disable=line-too-long
    },
    "tool.pylint.basic": {
        "argument-naming-style": '"snake_case"',
        "attr-naming-style": '"snake_case"',
        "class-attribute-naming-style": '"snake_case"',
        "class-naming-style": '"PascalCase"',
        "const-naming-style": '"UPPER_CASE"',
        "function-naming-style": '"snake_case"',
        "method-naming-style": '"snake_case"',
        "module-naming-style": '"snake_case"',
        "variable-naming-style": '"any"',
    },
    "tool.pylint.format": {
        "expected-line-ending-format": '"LF"',
        "max-module-lines": "600",
        "logging-format-style": '"new"',
        "max-args": "6",
        "max-attributes": "12",
        "max-bool-expr": "4",
        "max-locals": "16",
        "max-parents": "7",
        "max-public-methods": "16",
        "max-statements": "64",
        "min-public-methods": "1",
    },
    "tool.pylint.exceptions": {"overgeneral-exceptions": '"Exception"'},
    "tool.black": {"line-length": "88", "target-version": '["py36","py37","py38"]'},
    "tool.mypy": {
        "follow_imports": '"normal"',
        "disallow_any_unimported": "true",
        "disallow_untyped_calls": "true",
        "disallow_untyped_defs": "true",
        "disallow_untyped_decorators": "true",
        "no_implicit_optional": "true",
        "strict_optional": "true",
        "warn_redundant_casts": "true",
        "warn_unused_ignores": "true",
        "warn_return_any": "true",
        "warn_unreachable": "true",
        "strict_equality": "true",
    },
    "tool.isort": {
        "profile": '"black"',
        "multi_line_output": "3",
        "use_parentheses": "true",
    },
}

GITIGNORE = dedent(
    """
    *.d
    *.slo
    *.lo
    *.o
    *.obj
    *.gch
    *.pch
    *.dylib
    *.dll
    *.mod
    *.smod
    *.lai
    *.la
    *.exe
    *.out
    *.app
    __pycache__/
    *.py[cod]
    *$py.class
    .Python
    build/
    develop-eggs/
    dist/
    downloads/
    eggs/
    .eggs/
    lib/
    lib64/
    parts/
    sdist/
    var/
    wheels/
    share/python-wheels/
    *.egg-info/
    .installed.cfg
    *.egg
    MANIFEST
    *.manifest
    *.spec
    pip-log.txt
    pip-delete-this-directory.txt
    htmlcov/
    .tox/
    .nox/
    .coverage
    .coverage.*
    .cache
    nosetests.xml
    coverage.xml
    *.cover
    *.py,cover
    .hypothesis/
    .pytest_cache/
    cover/
    *.mo
    *.pot
    *.log
    local_settings.py
    db.sqlite3
    db.sqlite3-journal
    instance/
    .webassets-cache
    .scrapy
    docs/_build/
    .pybuilder/
    target/
    .ipynb_checkpoints
    profile_default/
    ipython_config.py
    # pipenv
    __pypackages__/
    celerybeat-schedule
    celerybeat.pid
    *.sage.py
    .env
    .venv
    env/
    venv/
    ENV/
    env.bak/
    venv.bak/
    .spyderproject
    .spyproject
    .ropeproject
    /site
    .mypy_cache/
    .dmypy.json
    dmypy.json
    .pyre/
    .pytype/
    cython_debug/
    """
)

PRE_COMMIT = {
    "repos": [
        {
            "repo": "https://github.com/pre-commit/pre-commit-hooks",
            "rev": "v2.3.0",
            "hooks": [
                {"id": "end-of-file-fixer"},
                {"id": "trailing-whitespace"},
                {"id": "debug-statements"},
            ],
        },
        {
            "repo": "meta",
            "hooks": [{"id": "check-hooks-apply"}, {"id": "check-useless-excludes"}],
        },
        {
            "repo": "https://github.com/psf/black",
            "rev": "21.11b1",
            "hooks": [{"id": "black"}],
        },
        {
            "repo": "https://github.com/pre-commit/mirrors-mypy",
            "rev": "v0.910",
            "hooks": [{"id": "mypy"}],
        },
        {
            "repo": "https://github.com/pycqa/isort",
            "rev": "5.10.1",
            "hooks": [{"id": "isort", "name": "isort (python)"}],
        },
        {
            "repo": "local",
            "hooks": [
                {
                    "id": "tests",
                    "pass_filenames": False,
                    "name": "pytest",
                    "entry": "pytest",
                    "language": "system",
                    "types": ["python3"],
                    "args": ["."],
                },
                {
                    "id": "pylint",
                    "pass_filenames": False,
                    "name": "pylint",
                    "entry": "pylint",
                    "language": "system",
                    "types": ["python3"],
                    "args": ["."],
                },
            ],
        },
    ]
}
