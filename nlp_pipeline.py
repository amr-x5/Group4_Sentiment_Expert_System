import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer

def download_nltk_data():
    """Download required NLTK data if not already present."""
    try:
        nltk.data.find('tokenizers/punkt')
        print("NLTK 'punkt' tokenizer already available.")
    except LookupError:
        print("Downloading NLTK 'punkt' tokenizer...")
        nltk.download('punkt')
        print("Download complete.")
    
    try:
        nltk.data.find('tokenizers/punkt/english.pickle')
        print("NLTK 'punkt' English model already available.")
    except LookupError:
        print("Downloading NLTK 'punkt_tab' for updated models...")
        nltk.download('punkt_tab')
        print("Download complete.")

# Ensure NLTK data is available
download_nltk_data()

def process_review_into_sentences(text):
    """
    Cleans and preprocesses the raw review text, splitting it into sentences.
    Returns a list of sentences, where each sentence is a list of tokens.
    """
    try:
        # Use nltk.sent_tokenize, which internally uses the Punkt tokenizer
        sentences = sent_tokenize(text)
        
        processed_sentences = []
        for sentence in sentences:
            # For each sentence, convert to lowercase and tokenize into words
            tokens = word_tokenize(sentence.lower())
            processed_sentences.append(tokens)
        
        return processed_sentences
    
    except LookupError as e:
        print(f"NLTK resource error: {e}")
        print("Trying to download required resources...")
        nltk.download('punkt')
        nltk.download('punkt_tab')
        
        # Retry after download
        sentences = sent_tokenize(text)
        processed_sentences = []
        for sentence in sentences:
            tokens = word_tokenize(sentence.lower())
            processed_sentences.append(tokens)
        
        return processed_sentences