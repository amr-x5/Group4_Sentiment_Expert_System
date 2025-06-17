# data_fetcher.py

def process_manual_reviews(reviews_list: list):
    """
    Processes a list of manually input review strings.
    Returns a dictionary in the format expected by the InferenceEngine.
    """
    if not isinstance(reviews_list, list):
        return {"error": "Input must be a list of review strings."}

    if not reviews_list:
        return {"error": "No reviews provided for analysis."}

    # Filter out any empty strings or strings with only whitespace
    processed_reviews = [review.strip() for review in reviews_list if review.strip()]

    if not processed_reviews:
        return {"error": "All provided reviews were empty or whitespace."}

    return {"status": "Manual Input", "reviews": processed_reviews}
