"""
    Validation Result class
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

from dataclasses import dataclass

@dataclass
class ValidationResult:
    """
        Validation Result class
    """
    proposed_translation : str
    correct     : str 
    explanation : str
    used_tokens : int
    cost        : float
    