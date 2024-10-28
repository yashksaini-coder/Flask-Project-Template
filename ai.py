import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is not set. Please check your .env file.")
else:
    client = Groq(api_key=api_key)

def analyze_sentiment(text):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Analyze the sentiment of the following text and return the sentiment result in simple words. Indicate whether the sentiment is positive, neutral, or negative."
                },
                {
                    "role": "user",
                    "content": text,
                },
            ]
        )
                
        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "No response from the API."
    except Exception as e:
        return f"An error occurred: {e}"