# inference_engine.py
from knowledge_base import get_knowledge_base
from nlp_pipeline import process_review_into_sentences
from data_fetcher import process_manual_reviews


class InferenceEngine:
    def __init__(self):
        self.kb = get_knowledge_base()
        self.working_memory = {}

    def _reset_memory(self):
        self.working_memory = {"aspect_sentiments": {}, "explanation": []}

    def analyze_product_reviews(self, reviews_list: list):
        """Top-level function to analyze a list of product review texts."""
        processed_data = process_manual_reviews(reviews_list)

        # Handle cases where the processor returns an error dictionary
        if isinstance(processed_data, dict) and "error" in processed_data:
            return processed_data

        # Ensure 'reviews' key exists and is a list before proceeding
        if "reviews" not in processed_data or not isinstance(processed_data["reviews"], list):
            return {"error": "Processed data is not in the expected format (missing 'reviews' list)."}

        reviews_content = processed_data["reviews"]
        if not reviews_content:
            return {"error": "No reviews were found or returned from the data processor."}

        all_results = [self._analyze_single_review(text) for text in reviews_content]
        # Add the data_source to the final summary
        summary = self._summarize_all_reviews(all_results)
        summary["data_source"] = processed_data.get("status", "Manual Input") # Add data source
        return summary

    def _summarize_all_reviews(self, all_results: list):
        """Aggregates results from all individual review analyses."""
        if not all_results: # Handle case with no valid results to summarize
            return {
                "total_reviews_analyzed": 0,
                "overall_product_score": 0,
                "overall_recommendation": "Neutral",
                "review_breakdown": {"positive": 0, "negative": 0, "neutral": 0},
                "aspect_summary": {}
            }

        total_reviews = len(all_results)
        pos = sum(1 for r in all_results if r['Overall Sentiment']['label'] == 'Positive')
        neg = sum(1 for r in all_results if r['Overall Sentiment']['label'] == 'Negative')
        neu = total_reviews - pos - neg

        agg_aspects = {}
        for result in all_results:
            for aspect, details in result.get("Aspect Sentiments", {}).items():
                if aspect not in agg_aspects:
                    agg_aspects[aspect] = {'scores': [], 'pos_count': 0, 'neg_count': 0}
                agg_aspects[aspect]['scores'].append(details['score'])
                if details['label'] == 'Positive':
                    agg_aspects[aspect]['pos_count'] += 1
                elif details['label'] == 'Negative':
                    agg_aspects[aspect]['neg_count'] += 1

        final_summary = {}
        for aspect, data in agg_aspects.items():
            avg_score = sum(data['scores']) / len(data['scores'])
            final_summary[aspect] = {
                "average_score": round(avg_score, 2),
                "label": self._score_to_label(avg_score),
                "positive_mentions": data['pos_count'],
                "negative_mentions": data['neg_count'],
            }

        overall_score = (pos - neg) / total_reviews if total_reviews > 0 else 0

        return {
            "total_reviews_analyzed": total_reviews,
            "overall_product_score": round(overall_score, 2),
            "overall_recommendation": self._score_to_label(overall_score),
            "review_breakdown": {"positive": pos, "negative": neg, "neutral": neu},
            "aspect_summary": final_summary
        }

    def _analyze_single_review(self, review_text: str):
        """Analyzes one review text."""
        self._reset_memory()
        sentences = process_review_into_sentences(review_text)
        for sentence_tokens in sentences:
            self._analyze_sentence(sentence_tokens)
        return self._generate_final_sentiment()

    def _analyze_sentence(self, tokens: list):
        """Applies rules to a single tokenized sentence."""
        sentence_text = ' '.join(tokens)
        consumed = set()

        for phrase, details in self.kb["ngrams"].items():
            if phrase in sentence_text:
                score, aspect = details["score"], details["aspect"]
                if aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][aspect] = []
                self.working_memory["aspect_sentiments"][aspect].append(score)
                consumed.update(phrase.split())

        current_aspect = "Overall"
        for i, token in enumerate(tokens):
            if token in consumed: continue
            if token in self.kb["aspects"]: current_aspect = self.kb["aspects"][token]
            if token in self.kb["unigrams"]:
                score = self.kb["unigrams"][token]
                if i > 0 and tokens[i - 1] in self.kb["negations"]:
                    score *= -1

                # This 'if' block is where the indentation error was.
                # The line below it is now correctly indented.
                if current_aspect not in self.working_memory["aspect_sentiments"]:
                    self.working_memory["aspect_sentiments"][current_aspect] = []

                self.working_memory["aspect_sentiments"][current_aspect].append(score)
                current_aspect = "Overall"

    def _generate_final_sentiment(self):
        """Calculates sentiment for the current working memory."""
        final_aspects = {}
        total_score, count = 0, 0
        for aspect, scores in self.working_memory["aspect_sentiments"].items():
            if scores:
                avg = sum(scores) / len(scores)
                final_aspects[aspect] = {"score": round(avg, 2), "label": self._score_to_label(avg)}
                total_score += sum(scores)
                count += len(scores)
        overall = total_score / count if count > 0 else 0
        return {
            "Overall Sentiment": {"score": round(overall, 2), "label": self._score_to_label(overall)},
            "Aspect Sentiments": final_aspects
        }

    def _score_to_label(self, score: float) -> str:
        if score > 0.1: return "Positive"
        if score < -0.1: return "Negative"
        return "Neutral"
