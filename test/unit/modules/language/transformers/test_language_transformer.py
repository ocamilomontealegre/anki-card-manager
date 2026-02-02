from typing import cast
from unittest.mock import MagicMock

import pytest

from modules.language.models.interfaces.card_response_interfaces.card_response_interface import (
    CardResponseBase,
    Forms,
)
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
def card_info_en():
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

@pytest.fixture
def card_info_fr():
    fake = cast(CardResponseBase, MagicMock(spec=CardResponseBase))
    fake.word = "confiance"
    fake.language = MagicMock(value="fr")
    fake.definition = "C'est un sentiment de sécurité ou de sûreté envers quelqu'un ou quelque chose, basé sur l'assurance en leurs capacités ou intentions."
    fake.category = MagicMock(value="noun")
    fake.usage = MagicMock(value="informal")
    fake.frequency_rank = "2543"
    fake.forms = Forms(
        singular_masculine="",
        singular_feminine="",
        plural_masculine="",
        plural_feminine="confiances",
    )
    fake.conjugations = []
    fake.sentence = "Elle a confiance en ses compétences pour réussir."
    fake.sentence_phonetics = "ɛl a kɔ̃fjɑ̃s ɑ̃ sɛ kɔ̃pɛtɑ̃s puʁ ʁesü"


def test_capitalize_text_array(transformer):
    assert transformer._capitalize_text_array([]) == ""
    assert transformer._capitalize_text_array(["dog"]) == "Dog"
    assert transformer._capitalize_text_array(["dog", "puppy"]) == "Dog, puppy"


@pytest.mark.parametrize(
    "text,word_forms,type_,expected",
    [
        # --- simple replacements ---
        ("The cat sleeps", ["cat"], "simple", "The {...} sleeps"),
        ("Cats are animals", ["cat", "cats"], "simple", "{...} are animals"),
        (
            "A dog, a cat, and another cat!",
            ["cat"],
            "simple",
            "A dog, a {...}, and another {...}!",
        ),
        ("No match here", ["cat"], "simple", "No match here"),
        (
            "Il lavoro su questo progetto è davvero impegnativo",
            ["impegnativo"],
            "simple",
            "Il lavoro su questo progetto è davvero {...}",
        ),
        (
            "Malgré l'accident, il est rentré chez lui sain et sauf",
            ["Sain et sauf", ""],
            "compound",
            "Malgré l'accident, il est rentré chez lui [sain et sauf]",
        ),
        (
            "Malgré l'accident, il est rentré chez lui sain et sauf",
            ["sain et sauf"],
            "simple",
            "Malgré l'accident, il est rentré chez lui {...}",
        ),
        # --- compound replacements ---
        ("The cat sleeps", ["cat"], "compound", "The [cat] sleeps"),
        ("Cats are animals", ["cat", "cats"], "compound", "[Cats] are animals"),
        (
            "A dog, a cat, and another cat!",
            ["cat"],
            "compound",
            "A dog, a [cat], and another [cat]!",
        ),
        # --- edge cases ---
        ("", ["cat"], "simple", ""),  # empty text
        ("The catalog", ["cat"], "simple", "The catalog"),  # substring shouldn't match
        (
            "Cat!",
            ["cat"],
            "compound",
            "[Cat]!",
        ),  # capitalization should still match exactly (case sensitive)
        # --- punctuation around words ---
        ("The cat.", ["cat"], "simple", "The {...}."),
        ("The (cat) sleeps", ["cat"], "compound", "The ([cat]) sleeps"),
        ("A cat—really!", ["cat"], "simple", "A {...}—really!"),
        # --- quotes ---
        ('"cat" is here', ["cat"], "compound", '"[cat]" is here'),
        ("'cat'", ["cat"], "simple", "'{...}'"),
    ],
)
def test_escape_word(transformer, text, word_forms, type_, expected):
    result = transformer._escape_word(text, word_forms=word_forms, type=type_)
    assert result == expected
