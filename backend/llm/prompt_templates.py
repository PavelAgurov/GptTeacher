generation_template = """/
Hello! I learn {lang_learn}. 
Make me a random sentence in {lang_my} for translation into {lang_learn}. 
{level_and_type}
Use this {random} value for seed randomization and generate different sentences.

{special_dict}

Provide answer in JSON format:
{{
    "random_word" : "random word in {lang_my}",
    "generated_sentence" : "sentence in {lang_my} with random word",
}}
"""

translate_template = """/
Hello! Your task is to translate the sentence from {lang_my} into {lang_learn} and give me dictionary.
Dictionary should contain all words from the sentence with their translations in infinitive form.
All nouns must have an article (for example "der Ort", "das Essen").

<input_sentence>
{input_sentence}
</input_sentence>

Provide answer in JSON format:
{{
    "translation" : "translated sentence in {lang_my}",
    "words":{{
        "nouns":[
            {{
                "word": "noun from original sentence",
                "infinitive": "noun from original sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form with article if article is needed"
            }}
        ],
        "adjectives":[
            {{
                "word": "adjective from original sentence",
                "infinitive": "adjective from original sentence in infinitive and singular form. base form, not comparative", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "verbs":[
            {{
                "word": "verb from original sentence",
                "infinitive": "verb from original sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "prepositions":[
            {{
                "word": "preposition from original sentence",
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "other":[
            {{
                "word": "word from original sentence",
                "infinitive": "word from original sentence in infinitive and singular form", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ]
    }}
}}
"""

check_prompt_template = """/
I have translation sentence from {lang_my} into {lang_learn}.
Please correct me if my translation is wrong and if there are errors please explain me step by step all my mistakes.

Do not check original sentence, only check my translation.
Don't try to make up an errors.
Don't change my transplation too much.
Do not tell me what I did correctly.
Do not check input sentence, only check my translation.
All explanations should be provided in {lang_my}.

If all is correct, just write "Correct!" (in {lang_my}).

Take into account that user can use synonyms and different word forms.
<used_words>
{used_words}
</used_words>

<input_sentence>
{input_sentence}
</input_sentence>

<translation>
{translation}
</translation>

Provide answer in JSON format:
{{
    "correct" : "correct translated sentence in {lang_learn}",
    "mistakes":[
        "detailed explanation of all translation mistakes (in {lang_my}) with references to the grammar rules"
    ]
}}

"""


def get_level_and_type_for_prompt(level, atype):
    if level == "Simple":
        return f"Sentence should be very simple - noun, verb and adjective and be {atype}."
    elif level == "Medium":
        return f"Sentence should have medium complexity and have maximum 10 words and be {atype}."
    elif level == "Advanced":
        return f"Sentence should be complex and have minumum 20 words and subordinate clause and be {atype}."
