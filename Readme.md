# Sentiment_Expert_System

A rule-based expert system for analyzing product sentiment from user reviews. This system processes review texts, identifies aspects, and determines overall sentiment and aspect-specific sentiments.

## Features

*   **Sentiment Analysis:** Classifies reviews as Positive, Negative, or Neutral.
*   **Aspect-Based Sentiment:** Identifies sentiment towards specific product features (e.g., "battery life," "screen quality").
*   **Multiple Interfaces:**
    *   Command-Line Interface (CLI)
    *   Gradio Web Interface
    *   Flask Web Application

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd sentiment_expert_system
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```
    Then install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Download NLTK data:**
    The system uses NLTK for text processing. Run the following script to download necessary NLTK resources (specifically 'punkt' for tokenization):
    ```bash
    python download_nltk_data.py
    ```
    Alternatively, the `nlp_pipeline.py` will attempt to download 'punkt' if it's not found, but running the script ensures all data is ready.

## Usage

You can interact with the system through one of the following interfaces:

### 1. Command-Line Interface (CLI)

Run `main.py` to start the CLI:
```bash
python main.py
```
The application will prompt you to enter product reviews one by one. Type `done` when you have finished entering all reviews for a product, or `exit` to quit.

### 2. Gradio Web Interface

Run `app.py` to launch the Gradio interface:
```bash
python app.py
```
This will typically start a local web server (e.g., at `http://127.0.0.1:7860`). Open this URL in your web browser. You can then paste multiple reviews (one per line) into the textbox and click "Analyze Reviews".

### 3. Flask Web Application

Run `server.py` to launch the Flask application:
```bash
python server.py
```
This will start a local web server (usually at `http://127.0.0.1:5000`). Open this URL in your browser. The interface allows you to paste multiple reviews (one per line) into a textarea and get the analysis.

## Project Structure

*   `main.py`: Entry point for the CLI application.
*   `app.py`: Entry point for the Gradio web interface.
*   `server.py`: Entry point for the Flask web server.
*   `templates/app.html`: HTML template for the Flask web interface.
*   `inference_engine.py`: Contains the core logic for the expert system, including rule application and sentiment calculation.
*   `knowledge_base.py`: Loads and provides access to the sentiment lexicons and aspect keywords.
    *   `unigrams.json`: Contains sentiment scores for individual words.
    *   `ngrams.json`: Contains sentiment scores for multi-word phrases.
    *   `aspects.json`: Maps keywords to product aspects.
*   `nlp_pipeline.py`: Handles text preprocessing tasks like sentence splitting and tokenization using NLTK.
*   `data_fetcher.py`: (Modified) Processes manually input review lists. Originally used for web scraping.
*   `download_nltk_data.py`: Script to download necessary NLTK resources.
*   `requirements.txt`: Lists Python package dependencies.
*   `UserManual.md`: Provides a user guide for the system.

## How It Works

1.  **Input:** The system accepts a list of product reviews.
2.  **Preprocessing:** Each review is processed by `nlp_pipeline.py`, which tokenizes the text into sentences and then into words.
3.  **Inference:** The `InferenceEngine` takes the processed reviews:
    *   It iterates through each sentence of each review.
    *   It uses the `knowledge_base` (unigrams, ngrams, aspects, negations) to identify sentiment-bearing words/phrases and associated aspects.
    *   Negation handling is applied.
    *   Scores are aggregated for each aspect and for the overall review.
4.  **Summarization:** Results from all analyzed reviews are aggregated to provide:
    *   Overall product sentiment score and recommendation.
    *   Breakdown of positive, negative, and neutral reviews.
    *   Summary of sentiments for each identified aspect.
5.  **Output:** The analysis summary is presented to the user through the chosen interface.
