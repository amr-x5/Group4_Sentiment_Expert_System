import json
import os


def load_json_kb(filename):
    """
    A helper function to load a JSON file from the knowledge_base directory.
    """
    # Get the directory where this script is located
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Knowledge base file not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file_path}. Check for syntax errors.")
        return {}


def get_knowledge_base():
    """
    Loads the expert system's knowledge from external JSON files.
    This makes the system scalable and easier to maintain.
    """
    # Load all knowledge components from their respective files
    ngrams_kb = load_json_kb('ngrams.json')
    unigrams_kb = load_json_kb('unigrams.json')
    aspects_kb = load_json_kb('aspects.json')

    # Define any knowledge that is better kept in code (e.g., static lists)
    negation_words = {'not': -1, "don't": -1, "dont": -1, "isn't": -1, "tak": -1, "bukan": -1}

    # Compile the final knowledge base dictionary
    kb = {
        "ngrams": ngrams_kb,
        "unigrams": unigrams_kb,
        "aspects": aspects_kb,
        "negations": negation_words
    }

    return kb

