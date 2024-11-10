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
    translation   : str
    explanation   : str
    
    def randomize(self):
        """
            Randomize options
        """
        import random
        correct_answer = self.options[self.correct_index]
        random.shuffle(self.options)
        self.correct_index = self.options.index(correct_answer)

@dataclass
class GapTestList:
    """
        GapTestList class
    """
    tests         : list[GapTest]
    random_value  : str
    total_tokens  : int
    cost          : float
    