# ai/summarizer.py

from ai.client import call_openai

def generate_summary(results, tone="helpful"):
    prompt = (
        f"You are a {tone} DevOps engineer and code reviewer. Summarize the following "
        "linting issues in plain English. Group them by rule. Don't repeat file "
        "names unless needed. No introductions are needed. Do not offer further help. "
        "This is the only interaction you will have with this review.\n\n"
        f"{results}"
    )
    return call_openai(prompt)
