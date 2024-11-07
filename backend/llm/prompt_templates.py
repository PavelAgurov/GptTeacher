generation_template = """/
Hello! I learn {lang_learn}.
Make me a random sentence in {lang_my} for translation into {lang_learn} and translate all the words in it, 
but not the sentence itself. All nouns must have an article (for example "der Ort", "das Essen").
Use this {random} value for seed randomization and generate different sentences.
###
{level_and_type}
###
{use_words}
Provide answer in JSON format:
{{
    "proposed_sentence" : "proposed sentence in {lang_my}",
    "words":{{
        "nouns":[
            {{
                "word": "noun from {lang_my} sentence",
                "infinitive": "noun from {lang_my} sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form with article if article is needed"
            }}
        ],
        "adjectives":[
            {{
                "word": "adjective from {lang_my} sentence",
                "infinitive": "adjective from {lang_my} sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "verbs":[
            {{
                "word": "verb from {lang_my} sentence",
                "infinitive": "verb from {lang_my} sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "prepositions":[
            {{
                "word": "preposition from {lang_my} sentence",
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "other":[
            {{
                "word": "word from {lang_my} sentence",
                "infinitive": "word from {lang_my} sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ]
    }}

}}
"""

check_prompt_template = """/
Hi, I want to check my {lang_learn}.
I have translation sentence (separated by XML tags) from {lang_my} into {lang_learn} (separated by XML tags).
Please correct me if my translation is wrong and if there are errors please explain me step by step all my mistakes.
Do not check original sentence, only check my translation.
Don't try to make up an errors, only provide me information about my mistakes in this sentence.
Don't change my transplation too much, only provide me information about my mistakes in this sentence.
All explanations should be provided in {lang_my}.

Take into account that user can use synonyms and different word forms.
<used_words>
{used_words}
</used_words>

Provide answer in JSON format:
{{
    "correct" : "correct sentence in {lang_learn}",
    "errors_explanations":[
        "detailed explanation of all my mistakes",
        "the same explanation translated into {lang_my}"
    ]
}}
Be sure that result is valid JSON.

<input_sentence>
{input_sentence}
</input_sentence>

<translation>
{translation}
</translation>
"""


def get_level_and_type_for_prompt(level, atype):
    if level == "Simple":
        return f"Sentence should be very simple - noun, verb and adjective and be {atype}."
    elif level == "Medium":
        return f"Sentence should have medium complexity and have maximum 10 words and be {atype}."
    elif level == "Advanced":
        return f"Sentence should be complex and have minumum 20 words and subordinate clause and be {atype}."
