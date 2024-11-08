"""
    Gap test page
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import logging

import streamlit as st
import pandas as pd
from redlines import Redlines

from backend.core import Core
from backend.classes.main_params import MainParams
from backend.classes.gap_test import GapTestList, GapTest

from utils import utils_streamlit
from utils.app_logger import init_streamlit_logger

logger : logging.Logger = logging.getLogger(__name__)

#---------------------------------------- Init logger

init_streamlit_logger()

#---------------------------------------- Session
if 'main_params' not in st.session_state:
    st.session_state.main_params = MainParams.Empty()
if 'token_count' not in st.session_state:
    st.session_state.token_count = 0
if 'back_end_core' not in st.session_state:
    st.session_state.back_end_core = None
    
if 'task_list' not in st.session_state:
    st.session_state.task_list = None

# ------------------------------------------ UI
how_it_work = """

Plese note - it's still POC. You can define your level and languages on Settings page.
You can also use special dictionary to learn specific words.
""".strip()

header_str = "Gpt Language Trainer"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str, help= how_it_work)

with st.sidebar:
    st.markdown(f'Tokens used: {st.session_state.token_count}')

utils_streamlit.streamlit_hack_remove_top_space()

# ------------------------------------------ Core

main_params : MainParams = st.session_state.main_params

core : Core = st.session_state.back_end_core
if not core:
    if main_params.gpt_key:
        core = Core(main_params.gpt_key)
        st.session_state.back_end_core = core

# ------------------------------------------ Main UI

if not main_params.gpt_key:
    st.error("Enter your Gpt key on Settings tab first")
    st.stop()

with st.container(border=True):
    settings_columns = st.columns(4)
    with settings_columns[0]:
        test_type = st.radio("Test type:", options=["Word", "Pronoun", "Unions"], index= 0, horizontal=True)
    with settings_columns[1]:
        level = st.radio("Your level:", options=["A1", "A2", "B1", "B2"], index= 2, horizontal=True)

run_button = st.button("Run")

task_list : list[GapTest] = st.session_state.task_list
if task_list:
    for test in task_list:
        st.markdown(f"**{test.test_task}**")
        for i, option in enumerate(test.options):
            st.markdown(f"{i+1}. {option}")
        st.markdown(f"Correct answer: {test.options[test.correct_index]}")
        st.markdown(f"Explanation: {test.explanation}")
        st.markdown("---")

if run_button:
    test_task_list : GapTestList = core.get_gap_test(
        level, 
        main_params.from_lang, 
        main_params.to_lang, 
        test_type
    )
    st.session_state.task_list = test_task_list.tests
    st.session_state.token_count += test_task_list.total_tokens
    st.rerun()
