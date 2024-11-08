"""
    GapTest class
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

from dataclasses import dataclass

@dataclass
class GapTest:
    """
        GapTest class
    """
    test_task     : str
    options       : list[str]
    correct_index : int
    explanation   : str

@dataclass
class GapTestList:
    """
        GapTestList class
    """
    tests : list[GapTest]
    total_tokens : int
    cost         : float
    