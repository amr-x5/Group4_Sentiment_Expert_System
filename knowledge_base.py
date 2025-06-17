import json
import os

def load_json_kb(filename):
    """Loads a JSON knowledge file."""
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading {filename}: {e}")
        return {}

def get_knowledge_base():
    """Loads and compiles the entire knowledge base from external files."""
    return {
        "ngrams": load_json_kb('ngrams.json'),
        "unigrams": load_json_kb('unigrams.json'),
        "aspects": load_json_kb('aspects.json'),
        "negations": {'not': -1, "don't": -1, "dont": -1, "isn't": -1, "tak": -1, "bukan": -1}
    }
