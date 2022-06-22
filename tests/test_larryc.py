# Import built-in libraries.
import os
import sys
from typing import List, Dict

# Import third-party libraries.
import pytest


# Add support layer for accessing the primary package.
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.path.pardir)
    )
)

# Import the App class from the package.
from larryc import App

# Make an App instance and use it in further testing.
app = App()


# Let the testing begin!
@pytest.mark.asyncio
class TestLarryc:
    async def test_response(self) -> None:
        assert await app.call('archeology')

    async def test_synonyms(self) -> None:
        test_synonyms: Dict[str, List[str] | None] = {
            'archeology': [],
            'entry': [
                "access",
                "enter",
                "entrance",
                "article",
                "lemma",
                "lexeme",
                "entrance",
                "ingang",
                "way in",
                "access",
                "admission",
                "record",
                "element"
            ],
            'dilemma': [
                "bind",
                "fix",
                "pickle",
                "problem",
                "quandary"
            ],
            'arbitrary': []
        }

        for key, value in test_synonyms.items():
            await app.call(key)
            synonyms = app.filter_meanings('synonyms')

            assert value == synonyms

    async def test_antonyms(self) -> None:
        test_antonyms: Dict[str, List[str] | None] = {
            'archeology': [],
            'entry': [
                "departure",
                "exit",
                "leaving",
                "exit",
                "way out"
            ],
            'dilemma': [],
            'arbitrary': []
        }

        for key, value in test_antonyms.items():
            await app.call(key)
            antonyms = app.filter_meanings('antonyms')

            assert value == antonyms