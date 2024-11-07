"""
    Proposed Sentence class
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

from dataclasses import dataclass

@dataclass
class ProposedSentence:
    """
        Proposed Sentence class
    """
    proposed_sentence   : str
    proposed_words_list : list[list[str]]
    used_tokens         : int
    