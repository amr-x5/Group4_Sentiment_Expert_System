from inference_engine import InferenceEngine
import json


def main():
    """
    A simple command-line interface for the Expert System.
    """

    engine = InferenceEngine()

    print("*" * 50)
    print("Welcome to the Shopee Review Sentiment Analysis ES")
    print(f"Aligning with SDG 12: Responsible Consumption ")
    print("*" * 50)

    while True:
        review = input("\nPlease enter a product review text (or type 'exit' to quit):\n> ")
        if review.lower() == 'exit':
            break

        # The engine performs the analysis
        results = engine.analyze_review(review)

        # The UI displays the results
        print("\n--- Sentiment Analysis Results ---")
        print(json.dumps(results, indent=2))
        print("--------------------------------\n")


if __name__ == "__main__":
    main()