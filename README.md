![logo](res/logo_withtext.svg)

# PyQuick

PyQuick is a personal tool (although you might like it too!) to quickly create python
projects. It uses a set of very strict and opinionated python linting and formatting tools
to take the decision making and configuration out of your hands. 

# Installation

The easiest way to install PyQuick is via pip (to install it system-wide).

`python3 -m pip install git+https://github.com/novafacing/pyquick.git`

# Usage

PyQuick is very opinionated, so it doesn't have very many options. The help message can
be printed with `python3 -m pyquick -h`.

```txt
usage: pyquick [-h] [--dry-run] [--inject] [--non-interactive] [--dependency [DEP [DEP ...]]] [--upgrade] [--verbose] [path]

A tool for quickly creating python projects.

positional arguments:
  path                  Path to the directory to set up or quicken.

optional arguments:
  -h, --help            show this help message and exit
  --dry-run, -d         Print out everything that will be done without doing it.
  --inject, -i          Whether to try and inject pyquick into an existing project.
  --non-interactive, -n
                        Whether to run pyquick in interactive mode.
  --dependency [DEP [DEP ...]], -D [DEP [DEP ...]]
                        Add a dependency to the project.
  --upgrade, -u         Perform a self-update of pyquick.
  --verbose, -v         Print out more information, particularly from subcommands.
```

Most of the time, you will want to do: 
`python3 -m pyquick -D angr -D capstone -n ./projname`, or something like that.

# Gotchas

1. Make sure you're not in a `poetry shell` when running this program! You'll get weird json errors for no apparent reason.