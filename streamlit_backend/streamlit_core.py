"""
    How to init core in streamlit
"""

# pylint: disable=C0301,C0103,C0303,C0411,W1203

import streamlit as st
from backend.core import Core
import logging

from backend.classes.main_params import MainParams

logger : logging.Logger = logging.getLogger(__name__)


def init_main_params() -> MainParams:
    """
        Init main params
    """
    if 'main_params' not in st.session_state:
        logger.info(f"Init new instance of MainParams")
        st.session_state.main_params = MainParams.Empty()
    return st.session_state.main_params


def init_core(main_params : MainParams) -> Core:
    """Init core"""

    # we should remove core from the session if code of Core was changed
    if 'backend_core_init' not in st.session_state or st.session_state.backend_core_init != str(Core.__init__.__code__):
        if 'backend_core' in st.session_state:
            _tmp = st.session_state.backend_core
            del _tmp
        st.session_state.clear()
        
        if main_params.gpt_key:
            logger.info(f"Init new instance of Core")
            core = Core(main_params.gpt_key)
            st.session_state.back_end_core = core
            st.session_state.backend_core_init = str(Core.__init__.__code__)

    return st.session_state.back_end_core

def draw_sidebar():
    """Draw sidebar"""
    
    if 'token_count' not in st.session_state:
        st.session_state.token_count = 0
    if 'token_cost' not in st.session_state:
        st.session_state.token_cost = 0
    
    with st.sidebar:
        st.markdown(f'Tokens used: {st.session_state.token_count}')
        st.markdown(f'Tokens cost: {st.session_state.token_cost:.2f}')
