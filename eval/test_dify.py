import requests
import os
from dotenv import load_dotenv
load_dotenv()

DIFY_API_KEY = os.getenv("DIFY_API_KEY")

API_URL = "http://srv01.dev.keycenter.ai:3000/v1/chat-messages"

headers = {
    "Authorization": f"Bearer {DIFY_API_KEY}",
    "Content-Type": "application/json"
}

def send_message_with_inputs(query, inputs=None, user_id="user-123", conversation_id=""):
    payload = {
        "inputs": inputs or {},
        "query": query,
        "response_mode": "blocking",
        "conversation_id": conversation_id,
        "user": user_id
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Example with variables
inputs = {
    "customer_name": "John",
    "room_number": "21",
    "db_uri": "mongodb://localhost:27017",
}

result = send_message_with_inputs(
    query="any food recommendations with high protein?",
    inputs=inputs
)
print(result)