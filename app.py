# app.py
import gradio as gr
from inference_engine import InferenceEngine

# --- Instantiate the Expert System's Core ---
engine = InferenceEngine()


def analyze_product_reviews_gradio(reviews_text: str):
    """
    Main function for Gradio. Takes a string of reviews, runs the analysis, and formats the output.
    """
    if not reviews_text.strip():
        return "Please enter product reviews.", None, None, None

    # Split the input string into a list of reviews, assuming one review per line
    reviews_list = [review.strip() for review in reviews_text.splitlines() if review.strip()]

    if not reviews_list:
        return "No valid reviews entered. Please provide at least one review.", None, None, None

    summary = engine.analyze_product_reviews(reviews_list)

    # --- Error Handling ---
    if "error" in summary:
        error_message = f"❌ **Error:** {summary['error']}"
        return error_message, None, None, None

    # --- Formatting the Output for the Dashboard ---
    status = summary.get("data_source", "Manual Input") # Default to Manual Input
    status_emoji = "🧪" # Using beaker emoji for manual/simulated
    status_output = f"**{status_emoji} Analysis Complete!** (Source: {status})"

    recommendation = summary.get("overall_recommendation", "Neutral")
    overall_score = summary.get("overall_product_score", 0)
    recommendation_output = {
        "label": recommendation,
        "conf": round(abs(overall_score), 2)
    }

    total = summary.get("total_reviews_analyzed", 0)
    breakdown = summary.get("review_breakdown", {})
    pos = breakdown.get("positive", 0)
    neg = breakdown.get("negative", 0)
    neu = breakdown.get("neutral", 0)
    breakdown_md = f"""
    ### Review Snapshot
    - **Total Reviews Analyzed:** {total}
    - **👍 Positive:** {pos}
    - **👎 Negative:** {neg}
    - **🤔 Neutral:** {neu}
    """

    aspects = summary.get("aspect_summary", {})
    if aspects:
        aspect_md = "### Aspect-Based Insights\n| Aspect | Avg. Score | Recommendation | Mentions (Pos/Neg) |\n| :--- | :---: | :---: | :---: |\n"
        sorted_aspects = sorted(aspects.items(),
                                key=lambda item: item[1]['positive_mentions'] + item[1]['negative_mentions'],
                                reverse=True)
        for aspect, details in sorted_aspects:
            aspect_md += f"| **{aspect}** | `{details.get('average_score', 0)}` | {details.get('label', 'N/A')} | {details.get('positive_mentions', 0)} / {details.get('negative_mentions', 0)} |\n"
    else:
        aspect_md = "### Aspect-Based Insights\nNo specific aspects were mentioned."

    return status_output, recommendation_output, breakdown_md, aspect_md


# --- Gradio Interface Definition ---
with gr.Blocks(theme=gr.themes.Soft(), title="Product Review Analyzer") as app_gradio: # Renamed app to app_gradio to avoid conflict
    gr.Markdown(
        """
        # Product Review Analyzer
        An Expert System by **Group 4: The Star Syndicate**
        """
    )
    with gr.Row():
        reviews_input_gradio = gr.Textbox(
            label="Enter Product Reviews",
            placeholder="Enter each review on a new line...\nExample:\nThis product is great!\nThe quality is amazing for the price.",
            lines=10,
            scale=4
        )
        submit_btn = gr.Button("Analyze Reviews", variant="primary", scale=1)

    gr.Examples(
        [
            "This is an amazing product, highly recommended!\nI love the features and the design.\nBattery life is excellent.",
            "Not happy with the purchase. It broke after a week.\nCustomer service was not helpful."
        ],
        inputs=reviews_input_gradio
    )

    status_output = gr.Markdown(label="Status")
    with gr.Row():
        with gr.Column(scale=1):
            recommendation_output = gr.Label(label="Overall Recommendation")
            breakdown_output = gr.Markdown(label="Review Breakdown")
        with gr.Column(scale=2):
            aspect_output = gr.Markdown(label="Aspect Summary")

    submit_btn.click(
        fn=analyze_product_reviews_gradio,
        inputs=reviews_input_gradio,
        outputs=[status_output, recommendation_output, breakdown_output, aspect_output]
    )

if __name__ == "__main__":
    app_gradio.launch()
