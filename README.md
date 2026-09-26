Learning how to build AI applications, step by step.

This repo is my hands-on journey from "what is an API key" to shipping
real AI apps. Each file is one lesson.

## Stack

- **Python 3.14** (in a virtualenv)
- **Groq** as the LLM provider — free tier, OpenAI-compatible API
- **openai** Python SDK (points at Groq's endpoint)
- **python-dotenv** for loading secrets from `.env`

No OpenAI account or credit card required. Get a free Groq key at
https://console.groq.com/keys

## Model used

`openai/gpt-oss-120b` — Groq's 120B open-weight model.
Fast, free tier, supports tools + JSON + reasoning.

Fallback if rate-limited: `openai/gpt-oss-20b`

## Setup

1. Clone and enter:
   ```bash
   git clone <your-repo-url>
   cd ai-app

2.Create and activate a virtual environment:python3 -m venv .venv
source .venv/bin/activate      # macOS/Linux
# .venv\Scripts\activate       # Windows

3.install dependencies
pip install openai python-dotenv

4.Create a .env file in the project root:

GROQ_API_KEY=gsk_your_key_here

5. to run cd ~/ai-app
source .venv/bin/activate
python hello_ai.py

expeected output 
<one-sentence explanation of tokenization>

--- usage ---
input tokens : 32
output tokens: 27
total tokens : 59
