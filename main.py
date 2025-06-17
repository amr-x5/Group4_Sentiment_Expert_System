# main.py
from inference_engine import InferenceEngine
import json


def cli_app():
    """
    A command-line interface to test the product review analysis expert system
    using manually entered reviews.
    """
    engine = InferenceEngine()

    print("*" * 50)
    print("Welcome to the Product Review Analysis ES")
    print("*" * 50)
    # Removed .env and API key check as it's no longer needed for scraper

    print("-" * 50)
    print("Please enter product reviews one by one.")
    print("Type 'done' on a new line when you have finished entering all reviews.")
    print("Or type 'exit' to quit the application.")
    print("-" * 50)

    while True:
        reviews_list = []
        print("\nEnter reviews for the product (type 'done' when finished, or 'exit' to quit):")
        while True:
            review_input = input("> ")
            if review_input.lower() == 'done':
                if not reviews_list:
                    print("No reviews entered. Please enter at least one review or type 'exit'.")
                    continue # Go back to asking for reviews for current product
                break # Proceed to analysis
            elif review_input.lower() == 'exit':
                return # Exit the cli_app function
            if review_input.strip(): # Add non-empty reviews
                reviews_list.append(review_input)
        
        if not reviews_list: # Should not happen if 'done' logic is correct, but as a safeguard
            print("No reviews were provided. Starting over or type 'exit'.")
            continue

        results = engine.analyze_product_reviews(reviews_list)

        print("\n--- Product Analysis Summary ---")
        if "error" in results:
            print(f"ERROR: {results['error']}")
        else:
            print(json.dumps(results, indent=2))
        print("--------------------------------\n")


if __name__ == "__main__":
    cli_app()
