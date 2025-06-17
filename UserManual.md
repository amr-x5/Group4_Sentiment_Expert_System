# User Manual
## Shopee Review Sentiment Analysis Expert System v2.0

**Project by: Group 4 (The Star Syndicate)**
**Course: WID2001 - Knowledge Representation and Reasoning**

---

### 1. Introduction

Welcome to the User Manual for the Shopee Review Sentiment Analysis Expert System. This document provides all the necessary information to understand and operate this modern web-based prototype.

The system is a rule-based expert system designed to analyze product reviews. Its primary goal is to automatically classify sentiment not only as a whole (Positive, Negative, Neutral) but also for specific **product aspects** such as Quality, Shipping, or Authenticity. The entire application runs directly in your web browser, requiring no complex setup.

### 2. System Requirements

*   Python 3.7 or higher.
*   A modern web browser (e.g., Google Chrome, Mozilla Firefox, Microsoft Edge) for the Gradio and Flask interfaces.
*   Internet connection (for downloading dependencies and NLTK data during initial setup).

### 3. Installation and Setup Guide

1.  **Clone or Download the Project:**
    Obtain the project files and navigate to the project directory in your terminal.

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    ```
    Activate the virtual environment:
    *   On Windows: `venv\Scripts\activate`
    *   On macOS/Linux: `source venv/bin/activate`

3.  **Install Dependencies:**
    Install all required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```
    This will install Flask, Gradio, NLTK, python-dotenv, and requests.

4.  **Download NLTK Data:**
    The system uses the NLTK library for natural language processing. Run the provided script to download the necessary 'punkt' tokenizer models:
    ```bash
    python download_nltk_data.py
    ```
    If this step is skipped, the `nlp_pipeline.py` will attempt to download it on first run, but it's better to do it beforehand.

### 4. How to Use the System

You can run the system using one of the three interfaces:

#### A. Command-Line Interface (CLI)

1.  Open your terminal or command prompt.
2.  Navigate to the project's root directory.
3.  Ensure your virtual environment (if created) is activated.
4.  Run the `main.py` script:
    ```bash
    python main.py
    ```
5.  The application will start and prompt you to:
    *   Enter product reviews one by one. Press Enter after each review.
    *   Type `done` on a new line and press Enter when you have finished entering all reviews for the current product.
    *   Type `exit` to quit the application.
6.  The analysis results will be printed in the console in JSON format.

#### B. Gradio Web Interface

1.  Open your terminal or command prompt.
2.  Navigate to the project's root directory.
3.  Ensure your virtual environment is activated.
4.  Run the `app.py` script:
    ```bash
    python app.py
    ```
5.  The script will start a local web server and usually print a URL like `Running on local URL: http://127.0.0.1:7860` (the port may vary).
6.  Open this URL in your web browser.
7.  You will see a textbox labeled "Enter Product Reviews".
8.  Type or paste your product reviews into the textbox. It's best to put each review on a new line.
9.  Click the **"Analyze Reviews"** button.
10. The analysis results (status, overall recommendation, review breakdown, and aspect summary) will be displayed on the page.

#### C. Flask Web Application

1.  Open your terminal or command prompt.
2.  Navigate to the project's root directory.
3.  Ensure your virtual environment is activated.
4.  Run the `server.py` script:
    ```bash
    python server.py
    ```
5.  The script will start a local web server, typically at `http://127.0.0.1:5000`.
6.  Open this URL in your web browser.
7.  You will see a page with a textarea.
8.  Type or paste your product reviews into the textarea, with each review on a new line.
9.  Click the **"Analyze Reviews"** button (or similar, depending on the HTML design).
10. The analysis results will be displayed on the page, usually showing overall sentiment and aspect details.

### 5. Interpreting the Output

Regardless of the interface used, the system provides a structured analysis:

*   **Overall Product Score/Recommendation**: An aggregate sentiment score for the product based on all provided reviews, typically labeled as Positive, Negative, or Neutral.
*   **Review Breakdown**: Statistics on the number of positive, negative, and neutral reviews analyzed.
*   **Aspect Summary/Insights**: A detailed breakdown of sentiment for specific product features (aspects) identified in the reviews. Each aspect will show:
    *   Its name (e.g., "Battery", "Screen").
    *   An average sentiment score for that aspect.
    *   A sentiment label (Positive, Negative, Neutral) for that aspect.
    *   The number of positive and negative mentions for that aspect.
*   **Data Source**: Indicates that the input was "Manual Input".

The goal is to provide a clear and understandable summary of the sentiment expressed in the product reviews.

---
*Thank you for using our prototype!*
*Group 4: The Star Syndicate*
