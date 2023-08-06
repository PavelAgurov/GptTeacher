how_it_work = """\
Enter your translation of proposed text, click Ctrl+Enter and wait for Gpt3.5-turbo validation and advice.
Plese note - it's still POC.<br/>
You can define your level and languages on Settings page.
"""
header_str = "Gpt Language Trainer"

SENTENCE_SUFFIX_LIST = ['.', '!', '?']

enter_key_info_message = '<p style="color:white; background-color:red">Enter your Gpt key on Settings tab</p>'

correct_answer_message = '<p style="color:green;">Correct!</p>'

gpt_key_usage_warning  = "Enter your Gpt key and press Enter. Your key is only used in your browser. If you refresh the page - enter the key again."

url_params_info_string = """\
URL parameters:
- from - "I speak" value
- to   - "I learn" value

Example: /from=Russian&To=German
"""