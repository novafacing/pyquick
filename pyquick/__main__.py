"""Entrypoint for pyquick when used from CLI as a module."""

from pyquick.parser import Parser
from pyquick.quick import Quick

if __name__ == "__main__":
    Quick(Parser().parse()).run()
