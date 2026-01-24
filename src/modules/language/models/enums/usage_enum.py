from enum import Enum


class Usage(Enum):
    """
    Indicates the context or style in which a word is typically used.
    
    FORMAL    -> suitable for formal writing or speech
    INFORMAL  -> casual or conversational
    SLANG     -> very informal or playful language
    ARCHAIC   -> old-fashioned, rarely used today
    FIGURATIVE -> metaphorical, not literal
    """
    FORMAL = "formal"
    INFORMAL = "informal"
    SLANG = "slang"
    ARCHAIC = "archaic"
    FIGURATIVE = "figurative"
