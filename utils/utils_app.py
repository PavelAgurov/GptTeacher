"""
    This file contains utility functions that are used in the project.
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import re
import base64

def remove_double_spaces(input):
    return re.sub(' +', ' ', input)


def get_fixed_json(text : str) -> str:
    """
        Extract JSON from text
    """
    if '```json' in text:
        open_bracket = text.find('```json')
        close_bracket = text.rfind('```')
        if open_bracket != -1 and close_bracket != -1:
            return text[open_bracket+7:close_bracket].strip()
    return text

def string_to_base64(input : str) -> str:
    """
        Convert string to base64
    """
    return base64.b64encode(input.encode('utf-8')).decode('utf-8')

def string_from_base64(input : str) -> str:
    """
        Convert string from base64
    """
    return base64.b64decode(input).decode('utf-8')

