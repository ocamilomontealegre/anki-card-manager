from pathlib import Path

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.modules.language.transformers.language_transformer import LanguageTransformer

@pytest.fixture
def mock_env(monkeypatch):
    """Patch EnvVariables.get() to return a fake env object."""
    fake_env = MagicMock()
    fake_env.anki.media = "/fake/media"
    monkeypatch.setattr(
        "src.modules.language.transformers.language_transformer.EnvVariables.get",
        lambda: fake_env,
    )
    return fake_env


@pytest.fixture
def mock_logger():
    """Mock logger with debug/error methods."""
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_scraper():
    """Mock scraper service."""
    mock = MagicMock()
    return mock


@pytest.fixture
def transformer(mock_scraper, mock_logger, mock_env):
    """Create the transformer instance."""
    return LanguageTransformer(scraper_service=mock_scraper, logger=mock_logger)


@pytest.fixture
def card_info():
    """Fake CardResponse-like object."""
    fake = MagicMock()
    fake.word = "cat"
    fake.language = MagicMock(value="en")
    fake.category = MagicMock(value="noun")
    fake.definition = "a small domesticated feline"
    fake.sentence = "The cat sleeps."
    fake.sentence_phonetics = "ðə kæt sliːps"
    fake.singular = ["cat"]
    fake.plural = ["cats"]
    fake.synonyms = ["kitty"]
    return fake


# def test_capitalize_text_array(transformer):
#     assert transformer._capitalize_text_array([]) == ""
#     assert transformer._capitalize_text_array(["dog"]) == "Dog"
#     assert transformer._capitalize_text_array(["dog", "puppy"]) == "Dog, puppy"

@pytest.mark.parametrize(
    "text,word_forms,type_,expected",
    [
        # --- simple replacements ---
        ("The cat sleeps", ["cat"], "simple", "The {...} sleeps"),
        ("Cats are animals", ["cat", "cats"], "simple", "{...} are animals"),
        ("A dog, a cat, and another cat!", ["cat"], "simple", "A dog, a {...}, and another {...}!"),
        ("No match here", ["cat"], "simple", "No match here"),

        # --- compound replacements ---
        ("The cat sleeps", ["cat"], "compound", "The [cat] sleeps"),
        ("Cats are animals", ["cat", "cats"], "compound", "[Cats] are animals"),
        ("A dog, a cat, and another cat!", ["cat"], "compound", "A dog, a [cat], and another [cat]!"),

        # --- edge cases ---
        ("", ["cat"], "simple", ""),  # empty text
        ("The catalog", ["cat"], "simple", "The catalog"),  # substring shouldn't match
        ("Cat!", ["cat"], "compound", "[Cat]!"),  # capitalization should still match exactly (case sensitive)
    ],
)
def test_scape_word(transformer, text, word_forms, type_, expected):
    result = transformer._scape_word(text, word_forms=word_forms, type=type_)
    assert result == expected