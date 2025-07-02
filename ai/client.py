# ai/client.py

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def call_openai(prompt, model="gpt-4.1-nano", temperature=0.4):

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert DevOps assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error from OpenAI: {e}"
