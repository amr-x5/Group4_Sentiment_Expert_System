import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

# Ensure NLTK sentence tokenizer data is available
try:
    nltk.data.find('tokenizers/punkt')
except nltk.downloader.DownloadError:
    print("Downloading NLTK 'punkt' model...")
    nltk.download('punkt', quiet=True)


def process_review_into_sentences(text):
    """
    Cleans and preprocesses the raw review text, splitting it into sentences.
    Returns a list of sentences, where each sentence is a list of tokens.
    """
    # Split the review into sentences
    sentences = sent_tokenize(text)

    processed_sentences = []
    for sentence in sentences:
        # For each sentence, convert to lowercase and tokenize into words
        tokens = word_tokenize(sentence.lower())
        processed_sentences.append(tokens)

    return processed_sentences