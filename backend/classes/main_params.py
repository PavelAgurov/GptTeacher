"""
    Main params
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import streamlit as st
import os
from dataclasses import dataclass

from utils import utils_app


LEVEL_INPUT_OPTIONS = ["Simple", "Medium", "Advanced"]

@dataclass
class MainParams:
    """
        Main params
    """
    gpt_key   : str
    level     : str
    from_lang : str
    to_lang   : str
    
    @staticmethod
    def Default() -> 'MainParams':
        """
            Default
        """
        gpt_key = st.query_params.get("key")
        if gpt_key:
            gpt_key = utils_app.string_from_base64(gpt_key)
        else:
            gpt_key = os.environ.get("OPENAI_API_KEY")
            
        level_input = st.query_params.get("level")
        if not level_input:
            level_input = LEVEL_INPUT_OPTIONS[1]

        from_lang = st.query_params.get("from")
        if not from_lang:
            from_lang = "Russian"
        
        to_lang = st.query_params.get("to")
        if not to_lang:
            to_lang = "German"
        
        return MainParams(
            gpt_key,
            level_input,
            from_lang,
            to_lang
        )
    
    
    def save(self):
        """
            Save
        """
        st.query_params["key"] = utils_app.string_to_base64(self.gpt_key)
        st.query_params["level"] = self.level
        st.query_params["from"] = self.from_lang
        st.query_params["to"] = self.to_lang
