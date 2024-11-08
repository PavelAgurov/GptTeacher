"""
    Main
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import logging

import streamlit as st
import pandas as pd
from redlines import Redlines

from backend.core import Core
from backend.classes.proposed_sentense import ProposedSentence
from backend.classes.validation_result import ValidationResult
from backend.classes.main_params import MainParams

from utils import utils_streamlit, utils_app
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
if 'proposed_sentence' not in st.session_state:
    st.session_state.proposed_sentence = None
if 'translation' not in st.session_state:
    st.session_state.translation = ""
if 'validation_result' not in st.session_state:
    st.session_state.validation_result = None

# ------------------------------------------ UI
header_str = "Gpt Language Trainer"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str)

how_it_work = """
Enter your translation of proposed text, click Ctrl+Enter and wait for validation and advice from LLM.
Plese note - it's still POC.
<br/>
You can define your level and languages on Settings page.
<br/>
You can find helful words on the right side.
""".strip()
st.markdown(how_it_work, unsafe_allow_html=True)


with st.sidebar:
    st.markdown(f'Tokens used: {st.session_state.token_count}')
    used_words_container = st.expander(label="I want to learn words (separate words by comma)")
    #used_words_input = used_words_container.text_area(label="", label_visibility="hidden")

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
    settings_columns = st.columns(2)
    with settings_columns[0]:
        type_input = st.radio("Sentence type:", options=["Statement", "Questions", "Imperative"], index= 0, horizontal=True, label_visibility="collapsed")
    with settings_columns[1]:
        help_words_enabled = st.checkbox("Show help words", value= True)

if help_words_enabled:
    main_columns = st.columns([2, 1])
else:
    main_columns = st.columns(1)

with main_columns[0]:
    proposed_sentence : ProposedSentence = st.session_state.proposed_sentence

    proposed_sentence_value = ""
    if proposed_sentence:
        proposed_sentence_value = proposed_sentence.proposed_sentence
    st.text_input("Sentense to translate: ", value= proposed_sentence_value, disabled=True, placeholder="Click Next to get new sentence")

    with st.container(border=True):
        translation = st.text_area("Your translation: ", value= st.session_state.translation, height=100)

if help_words_enabled:
    with main_columns[1]:
        with st.expander(label="Help words", expanded=True):
            if proposed_sentence and proposed_sentence.proposed_words_list:
                df = pd.DataFrame(proposed_sentence.proposed_words_list, columns=["Word", "Translation"])
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.text_area("Help words: ", value= "No words to show yet", label_visibility="collapsed", disabled=True)

validate_button_enabled = proposed_sentence and proposed_sentence.proposed_sentence
validate_button = st.button(label= "Validate", use_container_width=True, disabled= not validate_button_enabled)

validation_result : ValidationResult = st.session_state.validation_result
if validation_result:
    correct_str = utils_app.remove_double_spaces(validation_result.correct).strip()
    translation_str = utils_app.remove_double_spaces(translation).strip()
    
    # sync end of sentence - ? or . or !
    translation_str, correct_str  = core.fix_suffixes(translation_str, correct_str)

    diff = Redlines(translation_str, correct_str)
    st.markdown(diff.output_markdown, unsafe_allow_html=True)
    
    explanation = validation_result.explanation
    if explanation:
        if isinstance(explanation, list):
            explanation = "\n".join(explanation)
        st.markdown(explanation, unsafe_allow_html=True)
    else:
        st.markdown('<p style="color:green;">Correct!</p>', unsafe_allow_html=True)

next_button = st.button(label= "Next" , use_container_width=True)
    
if next_button:
    st.session_state.validation_result = None
    st.session_state.translation = ""
    
    proposed_sentence = core.get_next_sentence(
        main_params.level,
        type_input,
        main_params.to_lang,
        main_params.from_lang
    )
    st.session_state.proposed_sentence = proposed_sentence
    st.session_state.token_count += proposed_sentence.used_tokens
    st.rerun()
    
if validate_button:
    proposed_sentence : ProposedSentence = st.session_state.proposed_sentence
    st.session_state.translation = translation
    if not proposed_sentence or not proposed_sentence.proposed_sentence:
        st.error("Click Next to get new sentence before validation")
        st.stop()
    if not translation:
        st.error("Enter your translation before validation")
        st.stop()
    validation_result = core.validate_sentence(
        proposed_sentence.proposed_sentence,
        translation,
        main_params.to_lang,
        main_params.from_lang,
        proposed_sentence.proposed_words_list
    )
    st.session_state.validation_result = validation_result
    st.session_state.token_count += validation_result.used_tokens
    st.rerun()
   




