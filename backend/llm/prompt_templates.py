generation_prompt_template = """/
Your role is a teacher. I learn {lang_learn}. 
Make me a random sentence in {lang_my} for translation into {lang_learn}.
Rules:
{rules}
{special_dict}

Use this {random} value for seed randomization and generate different sentences.

Provide answer in JSON format:
{{
    "random_word" : "random word in {lang_my}",
    "generated_sentence" : "Sentence in {lang_my} with random word. All words MUST BE in {lang_my} language",
}}
"""

translate_prompt_template = """/
Your role is a teacher. Your task is to translate the sentence from {lang_my} into {lang_learn} and give me dictionary.
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
                "infinitive": "noun from original sentence in infinitive and singular form (in {lang_my})", 
                "translation" : "translation into {lang_learn} of infinitive and singular form with article if article is needed"
            }}
        ],
        "adjectives":[
            {{
                "word": "adjective from original sentence",
                "infinitive": "adjective from original sentence in infinitive and singular form (in {lang_my}). base form, not comparative", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ],
        "verbs":[
            {{
                "word": "verb from original sentence",
                "infinitive": "verb from original sentence in infinitive and singular form (in {lang_my})", 
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
                "infinitive": "word from original sentence in infinitive and singular form (in {lang_my})", 
                "translation" : "translation into {lang_learn} of infinitive and singular form"
            }}
        ]
    }}
}}
"""

check_prompt_template = """/
Your role is a teacher.
I have proposed translation of original sentence from {lang_my} into {lang_learn}.
Please correct me if my translation is wrong and if there are errors please explain me my mistakes.

Don't try to make up an errors.
Don't change my transplation too much.
Do not tell me what I did correctly.
Do not check original sentence, only check my translation!
Take into account that user can use synonyms and different word forms.
If all is correct, just write "Correct!" (in {lang_my}).


Think about it step by step.

All explanations should be provided in {lang_my}.

Original sentence in {lang_my}:
<original_sentence>
{original_sentence}
</original_sentence>

Translation of this sentence in {lang_learn}:
<proposed_translation>
{proposed_translation}
</proposed_translation>

Provide answer in JSON format:
{{
    "correct_translation" : "correctly translated original sentence in {lang_learn}",
    "mistakes":[
        "detailed explanation of all my translation mistakes (in {lang_my}) with references to the grammar rules"
    ]
}}

"""

detailed_help_prompt_template = """/
Your role is a teacher. I want to translate text from {lang_my} to {lang_learn} used rules for {type_input}. 
Please provide me rules that I should use to translate concrete this text. 
Describe rules in {lang_my}. 

<input_sentence>
{input_sentence}
</input_sentence>

Provide answer in markdown format:
```markdown
```
"""

task01_prompt_template = """
Please create me sprachbausteine TELC for level "{level}" in {lang_learn} language.
There are gap in the text and need to choose the correct {test_type} for the gap from the list of 3 options in {lang_learn} language.
You must generate 5 different tests. Be creative and use different words in the tests.

The test should be about a selection of correct {test_type}.
The test should be complex enough for "{level}" language level.
The test must have only one gap in the sentence!
All answers MUST be in {lang_learn} language, except explanations and translation!
All options must be different!
Only one option is correct!

Provide answer in JSON format:
{{
    "tests":[
        "test_number" : {random},
        "test_index" : 1..5,
        "test_task": "text of test in {lang_learn} language",
        "options": [
            3 different options in {lang_learn} language, only one is correct
        ],
        "correct": "index of correct answer",
        "translation": "sentense translation in {lang_my}",
        "explanation": "detailed explanation of answer in {lang_my} and why another options are wrong. do not say that they are wrong, explain why they are wrong"
    ]
}}
"""
