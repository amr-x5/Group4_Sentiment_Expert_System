import gradio as gr
import json
from inference_engine import InferenceEngine

# Instantiate your expert system's inference engine
engine = InferenceEngine()

def analyze_sentiment(review_text):
    """
    This function takes raw review text, passes it to the expert system,
    and formats the JSON output for display.
    """
    if not review_text.strip():
        return "Please enter a review text.", "No explanation available."

    # Get the analysis results from the inference engine
    results = engine.analyze_review(review_text)

    # Separate the main analysis from the explanation
    explanation_list = results.pop("Explanation", [])
    explanation_str = "\n".join(f"- {item}" for item in explanation_list)

    # Format the main results as a pretty-printed JSON string
    formatted_results = json.dumps(results, indent=2)

    return formatted_results, explanation_str

# --- Gradio Interface Definition ---

# Define the input and output components for the web UI
input_textbox = gr.Textbox(
    lines=5,
    label="Product Review Text",
    placeholder="Enter a Shopee product review here..."
)

output_json = gr.JSON(label="Sentiment Analysis Results")
output_explanation = gr.Markdown(label="🔎 Explanation (How the system decided)")


# Create the Gradio interface
# Use the 'theme' parameter for better styling
# Use the 'title' and 'description' for better presentation
# Provide examples to guide the user
iface = gr.Interface(
    fn=analyze_sentiment,
    inputs=input_textbox,
    outputs=[output_json, output_explanation],
    title="Shopee Review Sentiment Analysis ES",
    description=(
        "An expert system by **Group 4: The Star Syndicate** (WID2001). "
        "Enter a product review to see an aspect-based sentiment analysis. "
        "This system demonstrates explainable AI by showing the rules it used."
    ),
    examples=[
        ["The fabric quality is excellent, but the shipping was very slow."],
        ["This is a highcopy not authentic as advertised. But it's still well made."],
        ["I dont like this product it is a cheap copy"],
    ],
    allow_flagging="never",
    theme=gr.themes.Soft()
)

# Launch the web application
if __name__ == "__main__":
    iface.launch()
