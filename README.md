# Exploring AI Integration & Automation with Python

> A modular playground for experimenting with LLM APIs, automation patterns,
> and real-world AI use cases using Python.

This project demonstrates how to integrate various AI models (Google Gemini and Groq)
into a Python application. It explores capabilities such as sentiment analysis,
email summarization, Q&A generation, and chatbot interactions, all structured in a
modular and scalable way.

> ⚠️ **Disclaimer**  
> This is an exploratory and learning-focused project.  
> The codebase evolves continuously as new concepts, patterns, and limitations
> are discovered during the learning process.

---

## 🎯 Why this project?

This repository was created to explore how AI models can be integrated into
real-world automation scenarios using Python.

The focus is not on building a single product, but on:

- Understanding LLM API limitations and behavior
- Designing reusable AI utilities and abstractions
- Handling structured vs unstructured model outputs
- Exploring batch processing and cost-aware strategies
- Bridging no/low-code automation tools with custom Python logic

---

## 🚀 Features

- **Multi-Model Support**: Seamlessly switch between Google Gemini and Groq (Llama, etc.).
- **Batch & Single Call Strategies**: Efficient handling of multiple AI requests.
- **Structured Output Validation**: Parsing and validating LLM responses.
- **Review Analysis**: Analyze product reviews for customer sentiment (Positive, Neutral, Negative).
- **Email Automation**: Generate realistic test emails and summarize existing ones using AI.
- **Data Transformation**: Tools for processing TXT and CSV files, including filtering and translation.
- **Chatbot**: A terminal-based interactive chat interface.
- **Q&A Generation**: Automatically create Question & Answer pairs for datasets or testing.
- **Cost-Aware Design**: Experiments with batching, prompt constraints, and token efficiency.

---

## 📂 Project Structure

The project is organized into modular components for better maintainability:

| File | Purpose |
|------|---------|
| `main.py` | **Entry point**. Contains examples of how to run all features. |
| `clients.py` | Configuration and initialization of AI clients (Gemini & Groq). |
| `ai_utils.py` | Core wrapper functions for AI API interactions. |
| `review_analyzer.py` | Specialized logic for analyzing text and reviews. |
| `email_utils.py` | Tools to generate and summarize emails. |
| `qa_generator.py` | Utilities for generating Q&A pairs in batch. |
| `file_utils.py` | Helpers for reading and writing CSV and TXT files. |
| `data_transform.py` | DataFrame filtering and translation utilities. |
| `challenge_utils.py` | End-to-end challenge pipeline for review processing. |
| `prompts.py` | Centralized storage for AI prompts and data mappings. |

---

## 🛠️ Prerequisites

- Python 3.10+
- A Google Gemini API Key
- A Groq API Key

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv

   # On Windows:
   .\venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**

   ```bash
   cp .env.example .env
   ```

   Edit the `.env` file and add your API keys.

---

## ▶️ Usage

The project is designed to be explored via the `main.py` file.
Open it to see various examples commented out and uncomment the ones you want to run.

To run the main script:

   ```bash
   python main.py
   ```

### Examples included in `main.py`:

* **Simple Question**: Ask a single question to an AI model.
* **Chat Session**: Start an interactive chat loop.
* **Email Summarization**: Generate dummy emails and summarize them.
* **CSV Processing**: Read, filter, and translate CSV datasets.
* **Review Analysis**: Process a list of reviews to detect sentiment.
* **Negative Review Categorization**: Identify categories from negative feedback.
* **Challenge**: Run the full review processing challenge pipeline.

---

## 🧪 Testing & Validation

You can verify that your environment is set up correctly (without making API calls)
by running:

   ```bash
   python -c "from clients import get_gemini_client; print('Setup OK')"
   ```

To list available Gemini models:

   ```bash
   python list_models.py
   ```

---

## 📝 License

This project is intended for educational and experimental purposes.
Feel free to explore, learn from it, and adapt the ideas.