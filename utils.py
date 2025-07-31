from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("API_KEY")
CLIENT = OpenAI(api_key=API_KEY, base_url="https://api.groq.com/openai/v1")
print("Accessing LLM with API_KEY: \n", API_KEY )
def query_llm(message: str) -> str:
    """
    Provided function to query the LLM.
    Args:
        message: The prompt to send to the LLM
    Returns:
        The LLM's response as a string
    """
    response = CLIENT.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]
    )
    return response.choices[0].message.content
    