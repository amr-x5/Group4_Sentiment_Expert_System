# Shopee Review Sentiment Analysis Expert System

**Project for WID2001: Knowledge Representation and Reasoning**
**Group 4: The Star Syndicate**

This project is a prototype rule-based expert system designed to perform aspect-based sentiment analysis on product reviews. It features a modern, single-file web interface that runs entirely in the browser, providing transparent, actionable insights for both consumers and sellers and aligning with UN Sustainable Development Goal 12.

##  Key Features

* **Aspect-Based Analysis**: Goes beyond simple positive/negative labels to identify sentiment towards specific product aspects like `Quality`, `Shipping`, and `Authenticity`.
* **Modern UI**: A clean, responsive, and intuitive user interface for a professional presentation.
* **Zero Installation**: Runs directly in any modern web browser with no need for Python, servers, or dependencies.
* **Explainable AI (XAI)**: Provides a clear explanation of which rules and keywords were used to reach its conclusion, ensuring transparency.
* **SME-Informed**: The knowledge base is built upon insights from a real Subject Matter Expert (SME) to handle domain-specific language.

##  System Architecture

The system is a self-contained HTML application that implements a classic expert system architecture using client-side JavaScript:

1.  **Knowledge Base**: A JavaScript object containing factual knowledge (lexicons for sentiment, aspects, n-grams).
2.  **Inference Engine**: A forward-chaining reasoning engine, written in JavaScript, that processes reviews sentence by sentence to infer sentiment.
3.  **User Interface**: A responsive and interactive UI built with HTML and styled with Tailwind CSS.

##  How to Run

Running this project is incredibly simple:

1.  Download the `app.html` file.
2.  Double-click the `app.html` file to open it in your favorite web browser (like Chrome, Firefox, or Edge).

That's it! No command line or installation is required.

##  Team Members (Group 4: The Star Syndicate)

* **Amro Rashed** - *Project Manager*
* **Idlan Asyraaf** - *Knowledge Engineer*
* **Amjad Alzain** - *Programmer*
* **Muhamad Afif** - *Domain Expert*
* **Nicolas Perera** - *End User*