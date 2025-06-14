from knowledge_base import get_knowledge_base
from nlp_pipeline import process_review_into_sentences


class InferenceEngine:
    def __init__(self):
        self.kb = get_knowledge_base()
        self.working_memory = {}

    def _reset_memory(self):
        self.working_memory = {
            "aspect_sentiments": {},  # e.g., {'Quality': [0.8, -0.5]}
            "explanation": []
        }

    def analyze_review(self, review_text):
        self._reset_memory()

        # 1. Process review into a list of tokenized sentences
        sentences = process_review_into_sentences(review_text)

        # 2. Analyze each sentence individually
        for sentence_tokens in sentences:
            self._analyze_sentence(sentence_tokens)

        # 3. Aggregate the results from all sentences
        final_result = self._generate_final_sentiment()
        return final_result

    def _analyze_sentence(self, tokens):
        """
        Applies rules to a single sentence (list of tokens).
        """
        sentence_text = ' '.join(tokens)

        # Rule 1: Check for aspect-aware n-gram phrases
        consumed_tokens = []  # Keep track of words used in phrases
        for phrase, details in self.kb["ngrams"].items():
            if phrase in sentence_text:
                score = details["score"]
                aspect = details["aspect"]
                if aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][aspect] = []
                self.working_memory["aspect_sentiments"][aspect].append(score)
                self.working_memory["explanation"].append(
                    f"Found phrase '{phrase}' -> aspect '{aspect}' with score {score}")
                consumed_tokens.extend(phrase.split())

        # Rule 2: Process remaining single words
        current_aspect = "Overall"
        for i, token in enumerate(tokens):
            if token in consumed_tokens:
                continue  # Skip words that were part of an n-gram

            # Sub-rule: Find aspect keyword in sentence
            if token in self.kb["aspects"]:
                current_aspect = self.kb["aspects"][token]

            # Sub-rule: Find sentiment unigram
            if token in self.kb["unigrams"]:
                base_score = self.kb["unigrams"][token]

                # Check for negation
                if i > 0 and tokens[i - 1] in self.kb["negations"]:
                    base_score *= -1
                    self.working_memory["explanation"].append(f"Found negation for '{token}'")

                if current_aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][current_aspect] = []
                self.working_memory["aspect_sentiments"][current_aspect].append(base_score)
                self.working_memory["explanation"].append(
                    f"Found word '{token}' -> aspect '{current_aspect}' with score {round(base_score, 2)}")

    def _generate_final_sentiment(self):
        final_aspects = {}
        total_score = 0
        score_count = 0

        for aspect, scores in self.working_memory["aspect_sentiments"].items():
            if scores:
                avg_score = sum(scores) / len(scores)
                final_aspects[aspect] = {"score": round(avg_score, 2), "label": self._score_to_label(avg_score)}
                total_score += sum(scores)
                score_count += len(scores)

        overall_score = total_score / score_count if score_count > 0 else 0

        return {
            "Overall Sentiment": {"score": round(overall_score, 2), "label": self._score_to_label(overall_score)},
            "Aspect Sentiments": final_aspects,
            "Explanation": self.working_memory["explanation"]
        }

    def _score_to_label(self, score):
        if score > 0.1: return "Positive"
        if score < -0.1: return "Negative"
        return "Neutral"