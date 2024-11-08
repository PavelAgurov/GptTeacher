""""
    Core module for the backend
"""

# pylint: disable=C0301,C0103,C0303,C0304,C0305,C0411,E1121

import os
import json
import logging
import random

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_community.callbacks.manager import get_openai_callback
from langchain.globals import set_llm_cache
from langchain_community.cache import SQLiteCache

import backend.llm.prompt_templates as prompt_templates

from backend.classes.proposed_sentense import ProposedSentence
from backend.classes.validation_result import ValidationResult
from backend.classes.gap_test import GapTestList, GapTest

from utils import utils_app

logger : logging.Logger = logging.getLogger(__name__)

class Core:
    """"
        Core class for the backend
    """

    SENTENCE_SUFFIX_LIST = ['.', '!', '?']

    def __init__(self, gpt_key_input : str):
        # Init cache
        os.makedirs(".langchain-cache", exist_ok=True)
        set_llm_cache(
            SQLiteCache(
                database_path=os.path.join(".langchain-cache", ".langchain.db")
            )
        )
        
        self.gpt_key_input = gpt_key_input
        
        self.llm_fixed = ChatOpenAI(
                openai_api_key= gpt_key_input,
                model_name  = "gpt-4o-mini",
                temperature = 0,
                max_tokens  = 1000
        )

        self.llm_generation = ChatOpenAI(
                openai_api_key= self.gpt_key_input,
                model_name  = "gpt-4o-mini",
                temperature = 1,
                max_tokens  = 1000
        )


    def get_next_sentence(self, 
            level_input       : str, 
            type_input        : str,
            to_lang_value     : str,
            from_lang_value   : str,
            special_dict      : str,
            special_topic     : str,
            add_detailed_help : bool
        ) -> ProposedSentence:
        """"
            Get the next sentence
        """
        total_tokens = 0
        
        special_dict_str = []
        if special_dict:
            special_dict_str.append(f"The sentence MUST contain words from the list: <must_used_words>{special_dict}</must_used_words>")
        if special_topic:
            special_dict_str.append(f" The sentence MUST be about the topic '{special_topic}'")
        special_dict_str = "\n".join(special_dict_str)
        
        generation_prompt  = PromptTemplate.from_template(prompt_templates.generation_prompt_template)
        generation_chain  = generation_prompt | self.llm_generation | StrOutputParser()
        with get_openai_callback() as cb:
            generated_sentence_result = generation_chain.invoke({
                    "level_and_type" : prompt_templates.get_level_and_type_for_prompt(level_input, type_input), 
                    "lang_learn"     : to_lang_value,
                    "lang_my"        : from_lang_value,
                    "random"         : str(random.randint(0, 1000)),
                    "special_dict"   : special_dict_str
                })
            total_tokens = cb.total_tokens
        logger.info(f"{generated_sentence_result=}")
        generated_sentence_json = json.loads(utils_app.get_fixed_json(generated_sentence_result))
        generated_sentence = generated_sentence_json['generated_sentence']

        translation_prompt = PromptTemplate.from_template(prompt_templates.translate_prompt_template)
        translation_chain  = translation_prompt | self.llm_fixed | StrOutputParser()
        with get_openai_callback() as cb:
            translated_sentence_result = translation_chain.invoke({
                    "input_sentence": generated_sentence,
                    "lang_learn"    : to_lang_value,
                    "lang_my"       : from_lang_value
                })
            total_tokens += cb.total_tokens
        translation_sentence_json = json.loads(utils_app.get_fixed_json(translated_sentence_result))
        logger.info(f"{translation_sentence_json=}")
        translation_sentence = translation_sentence_json['translation']
        
        translation_words = translation_sentence_json['words']
        proposed_words_list = list[list[str]]()
        for w in translation_words['nouns']:
            if 'infinitive' in w and 'translation' in w:
                proposed_words_list.append([w['infinitive'], w["translation"]])
        for w in translation_words['adjectives']:
            if 'infinitive' in w and 'translation' in w:
                proposed_words_list.append([w['infinitive'], w["translation"]])
        for w in translation_words['verbs']:
            if 'infinitive' in w and 'translation' in w:
                proposed_words_list.append([w['infinitive'], w["translation"]])
        for w in translation_words['other']:
            if 'infinitive' in w and 'translation' in w:
                proposed_words_list.append([w['infinitive'], w["translation"]])
        
        proposed_words_list = [x for x in proposed_words_list if len(x[0]) > 1]
        
        detailed_help_str = ""
        if add_detailed_help:
            detailed_help_prompt = PromptTemplate.from_template(prompt_templates.detailed_help_prompt_template)
            detailed_help_chain  = detailed_help_prompt | self.llm_fixed | StrOutputParser()
            with get_openai_callback() as cb:
                detailed_help_str = detailed_help_chain.invoke({
                        "input_sentence": generated_sentence,
                        "lang_learn"    : to_lang_value,
                        "lang_my"       : from_lang_value
                    })
                total_tokens += cb.total_tokens
            detailed_help_str = utils_app.get_fixed_markdown(detailed_help_str)
            logger.info(f"{detailed_help_str=}")
        
        return ProposedSentence(generated_sentence, translation_sentence, proposed_words_list, detailed_help_str, total_tokens)

    def validate_sentence(self, 
                          proposed_sentence : str, 
                          translation       : str, 
                          to_lang_value     : str, 
                          from_lang_value   : str,
                          used_words        : list[str]
            ) -> ValidationResult:
        """"
            Validate the sentence
                proposed_sentence - the sentence to validate
                translation - the translation of the sentence from the user
        """
        logger.info(f"validate_sentence: proposed_sentence: {proposed_sentence}, translation: {translation}, to_lang_value: {to_lang_value}, from_lang_value: {from_lang_value}")
        
        validation_prompt = PromptTemplate.from_template(prompt_templates.check_prompt_template)
        validation_chain  = validation_prompt | self.llm_fixed | StrOutputParser()
        
        with get_openai_callback() as cb:
            validation_result = validation_chain.invoke({
                    "input_sentence": proposed_sentence,
                    "translation"   : translation,
                    "lang_learn"    : to_lang_value,
                    "lang_my"       : from_lang_value,
                    "used_words"    : used_words
            })
        
        logger.info(f"validate_sentence: {validation_result=}")
                       
        result_json = json.loads(utils_app.get_fixed_json(validation_result))
        
        correct : str = result_json["correct"].strip()
        correct = utils_app.remove_double_spaces(correct)
        
        explanation = result_json["mistakes"]

        return ValidationResult(correct, explanation, cb.total_tokens)                

    def fix_suffixes(self, proposed_sentence_str : str,  correct_str: str):
        """"
            Fix the suffixes
        """
        correct_suffix = correct_str[-1]
        user_suffix    = proposed_sentence_str[-1]
        if correct_suffix in Core.SENTENCE_SUFFIX_LIST:
            if correct_suffix != user_suffix:
                if user_suffix in Core.SENTENCE_SUFFIX_LIST:
                    proposed_sentence_str = proposed_sentence_str[:-1]
                proposed_sentence_str = proposed_sentence_str + correct_suffix
        return proposed_sentence_str, correct_str

    def get_gap_test(self, level : str, from_lang_value : str, to_lang_value : str, test_type : str) -> GapTestList:
        """
            Get the gap test
        """
        task_prompt = PromptTemplate.from_template(prompt_templates.task01_prompt_template)
        task_chain  = task_prompt | self.llm_fixed | StrOutputParser()
        
        total_tokens = 0
        with get_openai_callback() as cb:
            result = task_chain.invoke({
                    "lang_my"     : from_lang_value,
                    "lang_learn"  : to_lang_value,
                    "level"       : level,
                    "test_type"   : test_type,
                    "random"      : str(random.randint(0, 1000))
            })
            total_tokens = cb.total_tokens
            
        result = utils_app.get_fixed_json(result)
        result = result.replace("\n", "")
        logger.info(f"get_gap_test: {result=}")
        result_json = json.loads(result)
        
        tests = []
        for test in result_json["tests"]:
            test_task = test["test_task"]
            options   = test["options"]
            correct   = int(test["correct"])
            explanation = test["explanation"]
            tests.append(GapTest(test_task, options, correct, explanation))
        
        return GapTestList(tests, total_tokens)
        