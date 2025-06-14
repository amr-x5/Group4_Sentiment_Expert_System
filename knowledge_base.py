def get_knowledge_base():
    """
    Returns the knowledge base for the sentiment analysis expert system.
    V3: Aspect-aware n-grams and expanded domain-specific vocabulary.
    """

    # N-gram sentiment lexicon with associated aspects
    ngram_lexicon = {
        # Quality Phrases
        "well made": {"score": 0.8, "aspect": "Quality"},
        "good quality": {"score": 0.8, "aspect": "Quality"},
        "high quality": {"score": 0.9, "aspect": "Quality"},
        "poorly made": {"score": -0.8, "aspect": "Quality"},
        "low quality": {"score": -0.8, "aspect": "Quality"},
        "very good": {"score": 1.05, "aspect": "Overall"},

        # Authenticity Phrases
        "cheap copy": {"score": -0.9, "aspect": "Authenticity"},
        "not authentic": {"score": -1.0, "aspect": "Authenticity"},
        "not original": {"score": -1.0, "aspect": "Authenticity"},

        # General Phrases
        "tidak suka": {"score": -0.9, "aspect": "Overall"},
        "don't like": {"score": -0.9, "aspect": "Overall"},
        "dont like": {"score": -0.9, "aspect": "Overall"},
        "not good": {"score": -0.8, "aspect": "Overall"},
    }

    # Unigram (single word) sentiment lexicon
    unigram_lexicon = {
        # Positive
        'good': 0.7, 'great': 0.9, 'excellent': 1.0, 'love': 0.9, 'like': 0.5,
        'authentic': 0.9, 'original': 0.9, 'genuine': 0.9,

        # Negative
        'bad': -0.7, 'poor': -0.8, 'terrible': -1.0, 'hate': -0.9, 'slow': -0.6,
        'fake': -0.9, 'scam': -1.0, 'disappointed': -0.8,
        'copy': -0.7, 'highcopy': -0.6, 'cheap': -0.5,
    }

    # Aspect Dictionary now includes authenticity terms
    aspect_dictionary = {
        'quality': 'Quality', 'kualiti': 'Quality', 'made': 'Quality',
        'shipping': 'Shipping', 'delivery': 'Shipping',
        'seller': 'Seller Service', 'servis': 'Seller Service',
        'authenticity': 'Authenticity', 'originality': 'Authenticity',
    }

    # Modifiers
    intensifiers = {'very': 1.5, 'really': 1.4, 'extremely': 1.6}
    diminishers = {'slightly': 0.7, 'a bit': 0.6}
    negation_words = {'not': -1, "don't": -1, "dont": -1, "isn't": -1}

    kb = {
        "ngrams": ngram_lexicon,
        "unigrams": unigram_lexicon,
        "aspects": aspect_dictionary,
        "intensifiers": intensifiers,
        "negations": negation_words
    }

    return kb