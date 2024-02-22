"""Run instructions scripts to generate merged instructions and stats files."""
import json
import os
import random
import subprocess
import sys
from datetime import datetime

from utils.functions import create_directory

SCRIPTS_DIR = 'instructions_scripts'
SAMPLES_DIR = 'instructions_samples'
INSTR_AND_STATS_DIR = 'instructions_merged_and_stats'
base_dir = os.path.dirname(os.path.abspath(__file__))

# Path to the merged instructions file and generated stats files
merged_instructions_path = os.path.join(base_dir, INSTR_AND_STATS_DIR)

# Path to the scripts directory
scripts_dir_path = os.path.join(base_dir, SCRIPTS_DIR)

# Directory for instructions json files generated by instructions scripts
output_dir = os.path.join(base_dir, "output")

# Directory for downloaded external datasets and used by instructions scripts
data_dir = os.path.join(base_dir, "data")
# Directory for downloaded internal datasets from Speakelash and used by instructions scripts. It will be removed when
# new feature will be implemented in the Speakleash package.
data_speakleash_dir = os.path.join(base_dir, "data_speakleash")

# Create directory for merged instructions and stats files
create_directory(merged_instructions_path, output_dir, data_dir, data_speakleash_dir)

version = "0_0_8"

generate = True
exclude_tests = True

scipts_to_run = []
scipts_to_run.append({"script_name" : "allegro_klej_dyk_questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "legal-questions.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_LEGAL_QA", "test" : True})
scipts_to_run.append({"script_name" : "polish-summaries-corpus.py", "author" : "Ic & MariaF", "category": "NLP_SUMMARIZATION"})
scipts_to_run.append({"script_name" : "ipipan_polqa_questions.py", "author" : "Ic & MariaF", "category":
    "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "poquad_text_extraction.py", "author" : "Ic & MariaF", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "speakleash-categorization.py", "author" : "Amarok & Sekon", "category": "NLP_CLASSIFICATION"}) ##
scipts_to_run.append({"script_name" : "speakleash_forums_questions.py", "author" : "Ic & MariaF", "category":
    "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "wiki-lemmat-words.py", "author" : "Sekon", "category": "NLP_LEMMATIZATION"})
scipts_to_run.append({"script_name" : "allegro-summarization.py", "author" : "Sekon", "category": "NLP_SUMMARIZATION"})
scipts_to_run.append({"script_name" : "speakleash-create-sentence.py", "author" : "Sekon", "category": "NLP_SENTENCE_CREATION"})
scipts_to_run.append({"script_name" : "create_password.py", "author" : "Sekon", "category": "BUSINESS_TOOLS"})
scipts_to_run.append({"script_name" : "speakleash-simple-math-operations.py", "author" : "ChrisO", "category": "KNOWLEDGE_MATH"})
scipts_to_run.append({"script_name" : "amazon-massive-pl.py", "author" : "pawkis", "category": "NLP_INTENT_DETECTION"})
scipts_to_run.append({"script_name" : "plwiki_random_word_list.py", "author" : "Sekon", "category": "NLP_WORD_LIST"})
scipts_to_run.append({"script_name" : "plwiki_random_word_pos.py", "author" : "Sekon", "category": "NLP_WORD_POS"})
scipts_to_run.append({"script_name" : "quotes.py", "author" : "Sekon", "category": "NLP_QUOTES"})
scipts_to_run.append({"script_name" : "vulgar_words.py", "author" : "Sekon", "category": "NLP_VULGAR_DETECTION"})
scipts_to_run.append({"script_name" : "sentiment_detection.py", "author" : "Sekon", "category":
"NLP_SENTIMENT_DETECTION"})

scipts_to_run.append({"script_name" : "BAN-PL_hatespeech_detection.py", "author" : "Maria", "category": "NLP_HATESPEECH_DETECTION"}) ##
scipts_to_run.append({"script_name" : "exams_questions.py", "author" : "Jan.Maria", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "human_annotators_common_errors.py", "author" : "Ic", "category": "NLP_CORRECTION"})
scipts_to_run.append({"script_name" : "ipipan_polqa_questions.py", "author" : "Ic", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "emplocity_owca_questions.py", "author" : "Jan.Maria", "category": "KNOWLEDGE_QA"})
scipts_to_run.append({"script_name" : "polish-news-summarization.py", "author" : "Jan.Maria", "category": "NLP_SUMMARIZATION"})
scipts_to_run.append({"script_name" : "almost_like_an_alpaca.py", "author" : "Sekon", "category": "ALMOST_LIKE_AN_ALPACA"})


if generate:
    for script in scipts_to_run:
        result = subprocess.run([sys.executable, os.path.join(scripts_dir_path, script["script_name"])],
                                capture_output=True,
                                text=True)


def get_author(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script["author"]


def get_category(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script["category"]


def get_test(script_name):
    for script in scipts_to_run:
        if script["script_name"] == script_name:
            return script.get("test", False)


print("Merging files...")

files = os.listdir(output_dir)
all = []
counter = 1

authors_stats = {}
source_stats = {}
category_stats = {}

for file in files:
    file_path = os.path.join(output_dir, file)
    with open(file_path, "rb") as f:
        data = json.load(f)

    file_counter = 1

    for item in data:

        print("Merging file: " + file.upper().replace(".JSON", "") + " (" + str(file_counter) + ")")
        new_item = {}
        new_item['instruct'] = item.get('instruct', item.get('instruction', ''))
        new_item['input'] = item.get('input', '')
        new_item['output'] = item['output']

        if not new_item.get('output', ''):
            continue

        if new_item['output'].strip() == '':
            continue

        category = item.get('category', get_category(item['script_name']))
        test = get_test(item['script_name'])

        if test and exclude_tests:
            continue

        print("Category: " + category)

        new_item['category'] = category

        script_name = item.get('script_name', '')
        source_name = item.get('source_name', '')
        source_url = item.get('source_url', '')
        source_description = item.get('source_description', '')
        author = get_author(script_name)

        new_item['source_name'] = source_name

        if author not in authors_stats:
            authors_stats[author] = 1
        else:
            authors_stats[author] += 1

        if category not in category_stats:
            category_stats[category] = 1
        else:
            category_stats[category] += 1

        if source_name not in source_stats:
            source_stats[source_name] = {}
            source_stats[source_name]["count"] = 1
            source_stats[source_name]["url"] = source_url
            source_stats[source_name]["description"] = source_description
        else:
            source_stats[source_name]["count"] += 1

        all.append(new_item)
        counter += 1
        file_counter += 1

    print(file.upper().replace(".JSON", "") + ";" + str(file_counter))

random.shuffle(all)

current_date = datetime.now()
formatted_date = current_date.strftime("%Y_%m_%d")

# Save instructions
instr_file_name = "speakleash_pl_instructions_" + formatted_date + "_v" + version + ".jsonl"
instr_file_path = os.path.join(merged_instructions_path, instr_file_name)
with open(instr_file_path, "w", encoding="utf-8") as plik:
    for item in all:
        plik.write(json.dumps(item, ensure_ascii=False) + "\n")

# Save stats files
stats_files = ["authors_stats_", "source_stats_", "category_stats_"]
stats_to_save = [authors_stats, source_stats, category_stats]
for file, data in zip(stats_files, stats_to_save):
    file_name = file + formatted_date + "_v" + version + ".jsonl"
    file_path = os.path.join(merged_instructions_path, file_name)
    with open(file_path, "w", encoding="utf-8") as plik:
        plik.write(json.dumps(data, ensure_ascii=False))

print("Done!")
print("Total instructions: " + str(counter))
