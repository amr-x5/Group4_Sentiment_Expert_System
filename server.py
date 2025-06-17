# server.py
from flask import Flask, request, jsonify, render_template
from inference_engine import InferenceEngine

# Initialize the Flask application
# The 'template_folder' argument tells Flask where to find your app.html
app = Flask(__name__, template_folder='templates')

# Create a single instance of our expert system's engine
engine = InferenceEngine()


@app.route('/')
def home():
    """Serves the main user interface (app.html)."""
    return render_template('app.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    """
    This is the API endpoint the browser will call. It receives a list of reviews,
    runs the analysis, and returns the results.
    """
    data = request.get_json()
    reviews_text = data.get('reviews') # Expecting a single string with reviews separated by newlines

    if not reviews_text:
        return jsonify({"error": "Reviews are missing from the request."}), 400

    # Split the input string into a list of reviews
    reviews_list = [review.strip() for review in reviews_text.splitlines() if review.strip()]

    if not reviews_list:
        return jsonify({"error": "No valid reviews provided in the text."}), 400

    # This calls your expert system's backend logic
    results = engine.analyze_product_reviews(reviews_list)

    # Return the analysis results back to the browser as JSON
    return jsonify(results)


# This allows us to run the server by typing "python server.py"
if __name__ == '__main__':
    print("Starting the Product Analyzer web server...")
    print("Open your browser and navigate to http://127.0.0.1:5000")
    app.run(port=5000, debug=False)
