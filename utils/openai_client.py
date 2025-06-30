import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_text(content):
    prompt = (
        "You are an ESG compliance assistant. Summarize the following news article, policy, or regulatory change "
        "into a clear and concise executive summary suitable for a compliance digest:\n\n"
        f"{content}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[Summary failed: {e}]"
