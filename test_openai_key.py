import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

# Load environment variables from .env
load_dotenv()

# Get API key from env
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not set")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

try:
    # Make a simple embedding request
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input=["Test input for API key verification"]
    )
    print("✅ Success! First 5 values of embedding:")
    print(response.data[0].embedding[:5])
except OpenAIError as e:
    print("❌ OpenAI API error:", e)
except Exception as e:
    print("❌ General error:", e)

