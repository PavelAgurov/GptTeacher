"""
    Gap test page
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import logging
from redlines import Redlines

import streamlit as st

from backend.core import Core
from backend.classes.main_params import MainParams
from streamlit_backend import streamlit_core
from backend.classes.gap_test import GapTestList, GapTest

from utils import utils_streamlit
from utils.app_logger import init_streamlit_logger

logger : logging.Logger = logging.getLogger(__name__)

#---------------------------------------- Init logger

init_streamlit_logger()

# ------------------------------------------ Core

main_params : MainParams = streamlit_core.init_main_params()
core : Core = streamlit_core.init_core(main_params)

#---------------------------------------- Session
if 'task_list' not in st.session_state:
    st.session_state.task_list = None
if 'show_answers' not in st.session_state:
    st.session_state.show_answers = False

# ------------------------------------------ UI
how_it_work = """

Plese note - it's still POC. You can define your level and languages on Settings page.
You can also use special dictionary to learn specific words.
""".strip()

header_str = "Gpt Language Trainer"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str, help= how_it_work)

utils_streamlit.streamlit_hack_remove_top_space()

streamlit_core.draw_sidebar()

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

main_columns = st.columns(2)

with main_columns[0]:
    next_button = st.button("Generate next test")
    with st.container(border=True, height=550):
        task_list : GapTestList = st.session_state.task_list
        if task_list:
            proposed_answer_list = []
            for test_index, test in enumerate(task_list.tests):
                st.markdown(f"{test_index+1}. **{test.test_task}**")
                proposed_answer = st.radio("Select option:", 
                    options=test.options, 
                    horizontal=True, 
                    label_visibility="collapsed", 
                    index= None,
                    key= test.test_task + task_list.random_value
                )
                proposed_answer_list.append(proposed_answer)
            st.markdown(f"Test #{task_list.random_value}")

with main_columns[1]:
    check_column = st.columns(2)
    
    with check_column[0]:
        check_button = st.button("Check answers")

    with check_column[1]:
        correct_answers = 0
        if st.session_state.show_answers:
            for i, test in enumerate(task_list.tests):
                if proposed_answer_list[i]:
                    correct_answer = test.options[test.correct_index]
                    if correct_answer == proposed_answer_list[i]:
                        correct_answers += 1
            st.markdown(f"Correct answers: {correct_answers}/{len(task_list.tests)}")
            
    with st.container(border=True, height=550):
        if st.session_state.show_answers:
            for i, test in enumerate(task_list.tests):
                if proposed_answer_list[i]:
                    correct_answer = test.options[test.correct_index]
                    diff = Redlines(proposed_answer_list[i], correct_answer)
                    st.markdown(f"**Anwer**: {diff.output_markdown}", unsafe_allow_html=True)
                st.markdown(f"*{test.translation}*  {test.explanation}")
        else:
            st.markdown("Press 'Check answers' to see the results")
            
if next_button:
    test_task_list : GapTestList = core.get_gap_test(
        level, 
        main_params.from_lang, 
        main_params.to_lang, 
        test_type
    )
    st.session_state.task_list = test_task_list
    st.session_state.token_count += test_task_list.total_tokens
    st.session_state.show_answers = False
    st.rerun()

if check_button:
    st.session_state.show_answers = True
    st.rerun()