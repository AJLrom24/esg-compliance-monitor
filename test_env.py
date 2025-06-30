from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Get the key
api_key = os.getenv("OPENAI_API_KEY")

# Print it masked
if api_key:
    print("✅ API key loaded:", api_key[:10] + "..." + api_key[-5:])
else:
    print("❌ API key NOT loaded. Check your .env or dotenv config.")

