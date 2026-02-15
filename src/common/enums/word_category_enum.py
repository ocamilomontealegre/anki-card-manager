from enum import Enum


class WordCategory(str, Enum):
    NOUN = "noun"
    VERB = "verb"
    ADJECTIVE = "adjective"
    ADVERB = "adverb"
    PRONOUN = "pronoun"
    PROPOSITION = "proposition"
    CONJUNCTION = "conjunction"
    INTERJECTION = "interjection"
    IDIOM = "idiom"
