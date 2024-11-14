"""
    Main
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import logging

import streamlit as st
from utils.app_logger import init_streamlit_logger

from backend.classes.main_params import MainParams, LEVEL_INPUT_OPTIONS
from streamlit_backend import streamlit_core

logger : logging.Logger = logging.getLogger(__name__)

#---------------------------------------- Init logger

init_streamlit_logger()

#---------------------------------------- Session

main_params : MainParams = streamlit_core.init_main_params()

# ------------------------------------------ UI
header_str = "Settings"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str)

st.info("""
Enter your Gpt key, set the parameters and press Save. 

**Your key is only used in your browser.**

URL parameters:
- from - "I speak" value
- to   - "I learn" value

Example: /from=Russian&To=German
        
""")

main_params : MainParams = st.session_state.main_params

gpt_key_input = main_params.gpt_key
main_params.gpt_key = st.text_input("Your Gpt key:", value = gpt_key_input, type='password')

from_lang_value = main_params.from_lang
from_lang_value = st.text_input("I speak:", value= from_lang_value)
main_params.from_lang = from_lang_value

to_lang_value = main_params.to_lang
to_lang_value = st.text_input("I learn:", value= to_lang_value)
main_params.to_lang = to_lang_value

level_input = main_params.level
level_input_index = LEVEL_INPUT_OPTIONS.index(level_input)
level_input = st.selectbox("Level:", key="slevel", options= LEVEL_INPUT_OPTIONS, index= level_input_index)
main_params.level = level_input

if st.button("Save"):
    st.session_state.main_params = main_params
    main_params.save()


