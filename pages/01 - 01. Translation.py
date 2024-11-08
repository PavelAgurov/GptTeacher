"""
    Sentense translation page
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
if 'token_cost' not in st.session_state:
    st.session_state.token_cost = 0
if 'back_end_core' not in st.session_state:
    st.session_state.back_end_core = None

if 'proposed_sentence' not in st.session_state:
    st.session_state.proposed_sentence = None
if 'translation' not in st.session_state:
    st.session_state.translation = ""
if 'validation_result' not in st.session_state:
    st.session_state.validation_result = None
if 'special_dict' not in st.session_state:
    st.session_state.special_dict = None
if 'special_topic' not in st.session_state:
    st.session_state.special_topic = None

# ------------------------------------------ UI
how_it_work = """
Client Next to get sentense for translation.
Enter your translation, click Validate and wait for validation and advice from LLM.

Plese note - it's still POC. You can define your level and languages on Settings page.
You can also use special dictionary to learn specific words.
""".strip()

header_str = "Gpt Language Trainer"
st.set_page_config(page_title= header_str, layout="wide")
st.title(header_str, help= how_it_work)

with st.sidebar:
    st.markdown(f'Tokens used: {st.session_state.token_count}')
    st.markdown(f'Tokens cost: {st.session_state.token_cost:.2f}')

utils_streamlit.streamlit_hack_remove_top_space()

# ------------------------------------------ Core

main_params : MainParams = st.session_state.main_params

core : Core = st.session_state.back_end_core
if not core:
    if main_params.gpt_key:
        core = Core(main_params.gpt_key)
        st.session_state.back_end_core = core

# ------------------------------------------ Params

TYPE_INPUT_LIST = ["Statement", "Questions", "Imperative"]
TYPE_COND_LIST  = ["Normal", "Conditional", "Subordinate clause"]
DICT_TYPE_LIST  = ["Random",  "Topic", "Special dictionary"]
EXTRA_LIST = ["Help words", "Detailed help"]

# ------------------------------------------ Main UI

if not main_params.gpt_key:
    st.error("Enter your Gpt key on Settings tab first")
    st.stop()

with st.container(border=True):
    settings_columns = st.columns(4)
    with settings_columns[0]:
        type_input = st.radio("type:", options= TYPE_INPUT_LIST, index= 0, label_visibility="collapsed")
    with settings_columns[1]:
        type_cond = st.radio("type:", options= TYPE_COND_LIST, index= 0, label_visibility="collapsed")
    with settings_columns[2]:
        dict_type = st.radio("Dictionary type:", options= DICT_TYPE_LIST, index= 0, label_visibility="collapsed")
    with settings_columns[3]:
        help_words_enabled = st.checkbox(EXTRA_LIST[0], value= True)
        detailed_help_enabled = st.checkbox(EXTRA_LIST[1], value= False)

if help_words_enabled or detailed_help_enabled:
    main_columns = st.columns([2, 1])
else:
    main_columns = st.columns(1)

proposed_sentence : ProposedSentence = st.session_state.proposed_sentence

with main_columns[0]:
    total_height = 260
    
    special_topic = None
    if dict_type == DICT_TYPE_LIST[1]:
        with st.container(border=True):
            special_topic = st.text_input("I want to learn topic:", value= st.session_state.special_topic)
        total_height += 115

    special_dict = None
    if dict_type == DICT_TYPE_LIST[2]:
        with st.container(border=True):
            special_dict = st.text_area("I want to learn words (comma or lines separated):", height=100, value= st.session_state.special_dict)
        total_height += 170
    
    with st.container(border=True):
        proposed_sentence_value = ""
        if proposed_sentence:
            proposed_sentence_value = proposed_sentence.proposed_sentence
        st.text_area("Sentense to translate: ", value= proposed_sentence_value, disabled=True, placeholder="Click Next to get new sentence", height=80)

    with st.container(border=True):
        translation = st.text_area("Your translation: ", value= st.session_state.translation, height=100)

if len(main_columns) == 2:
    with main_columns[1]:
        extra_tabs = []
        if help_words_enabled:
            extra_tabs.append(EXTRA_LIST[0])
        if detailed_help_enabled:
            extra_tabs.append(EXTRA_LIST[1])
        st_extra_tabs = st.tabs(extra_tabs)
        
        if help_words_enabled:
            with st_extra_tabs[extra_tabs.index(EXTRA_LIST[0])]:
                if proposed_sentence and proposed_sentence.proposed_words_list:
                    df = pd.DataFrame(proposed_sentence.proposed_words_list, columns=["Word", "Translation"])
                    st.dataframe(df, use_container_width=True, hide_index=True, height= total_height)
                else:
                    st.text_area("Help words:", value= "No words to show yet", label_visibility="collapsed", disabled=True, height= total_height)
                    
        if detailed_help_enabled: 
            with st_extra_tabs[extra_tabs.index(EXTRA_LIST[1])]:
                if proposed_sentence and proposed_sentence.detailed_help:
                    with st.container(border=True, height= total_height):
                        st.markdown(proposed_sentence.detailed_help, unsafe_allow_html=True)
                else:
                    st.text_area("Detailed help:", value= "No detailed help to show yet", label_visibility="collapsed", disabled=True, height= total_height)

validate_button_enabled = proposed_sentence and proposed_sentence.proposed_sentence
validate_button = st.button(label= "Validate", use_container_width=True, disabled= not validate_button_enabled)

validation_result : ValidationResult = st.session_state.validation_result
if validation_result and validation_result.proposed_translation == translation:
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
    if dict_type == DICT_TYPE_LIST[1] and not special_topic:
        st.error("Enter your special topic first")
        st.stop()
    
    if dict_type == DICT_TYPE_LIST[2] and not special_dict:
        st.error("Enter your special dictionary first")
        st.stop()
    
    st.session_state.validation_result = None
    st.session_state.translation = ""
    st.session_state.special_dict = special_dict
    st.session_state.special_topic = special_topic
    
    proposed_sentence = core.get_next_sentence(
        main_params.level,
        f"{type_input} {type_cond}",
        main_params.to_lang,
        main_params.from_lang,
        special_dict,
        special_topic,
        detailed_help_enabled
    )
    st.session_state.proposed_sentence = proposed_sentence
    st.session_state.token_count += proposed_sentence.used_tokens
    st.session_state.token_cost += proposed_sentence.cost
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
    st.session_state.token_cost += validation_result.cost
    st.rerun()
   




