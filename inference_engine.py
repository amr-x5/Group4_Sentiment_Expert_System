# inference_engine.py
from knowledge_base import get_knowledge_base
from nlp_pipeline import process_review_into_sentences


class InferenceEngine:
    def __init__(self):
        """
        Initializes the Inference Engine by loading the entire knowledge base.
        """
        self.kb = get_knowledge_base()
        self.working_memory = {}

    def _reset_memory(self):
        """
        Clears the working memory for a new analysis.
        """
        self.working_memory = {
            "aspect_sentiments": {},
            "explanation": []
        }

    def analyze_review(self, review_text):
        """
        Orchestrates the analysis of a given product review.
        """
        self._reset_memory()

        # 1. Process review into a list of tokenized sentences using the NLP pipeline.
        sentences = process_review_into_sentences(review_text)

        # 2. Analyze each sentence individually to identify sentiments and aspects.
        for sentence_tokens in sentences:
            self._analyze_sentence(sentence_tokens)

        # 3. Aggregate the results from all sentences to form a final conclusion.
        final_result = self._generate_final_sentiment()
        return final_result

    def _analyze_sentence(self, tokens):
        """
        Applies rules to a single sentence (list of tokens).
        This follows a forward-chaining, data-driven approach.
        """
        sentence_text = ' '.join(tokens)
        consumed_tokens = set()

        # Rule 1 (High Priority): Check for multi-word n-gram phrases first.
        # This is a more specific rule, so it's fired before general unigram rules.
        for phrase, details in self.kb["ngrams"].items():
            if phrase in sentence_text:
                score = details["score"]
                aspect = details["aspect"]

                # Add facts to working memory
                if aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][aspect] = []
                self.working_memory["aspect_sentiments"][aspect].append(score)
                self.working_memory["explanation"].append(
                    f"Found phrase '{phrase}' -> aspect '{aspect}' with score {score}")

                # Mark tokens as used to prevent re-analysis
                for word in phrase.split():
                    consumed_tokens.add(word)

        # Rule 2 (Lower Priority): Process remaining single words (unigrams).
        current_aspect = "Overall"
        for i, token in enumerate(tokens):
            if token in consumed_tokens:
                continue

            # Sub-rule 2a: Identify aspect context for the current part of the sentence.
            if token in self.kb["aspects"]:
                current_aspect = self.kb["aspects"][token]

            # Sub-rule 2b: Identify a sentiment-bearing word.
            if token in self.kb["unigrams"]:
                base_score = self.kb["unigrams"][token]

                # Contextual sub-rule: Check for negation words immediately preceding.
                if i > 0 and tokens[i - 1] in self.kb["negations"]:
                    base_score *= -1
                    self.working_memory["explanation"].append(f"Found negation modifying '{token}'")

                # Add facts to working memory under the current aspect context.
                if current_aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][current_aspect] = []
                self.working_memory["aspect_sentiments"][current_aspect].append(base_score)
                self.working_memory["explanation"].append(
                    f"Found word '{token}' -> aspect '{current_aspect}' with score {round(base_score, 2)}")

                # Reset aspect to avoid sentiment bleed-over in the same sentence
                current_aspect = "Overall"

    def _generate_final_sentiment(self):
        """
        Aggregates all facts from the working memory to produce the final analysis.
        """
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
        """Converts a numerical score to a sentiment label."""
        if score > 0.1: return "Positive"
        if score < -0.1: return "Negative"
        return "Neutral"
