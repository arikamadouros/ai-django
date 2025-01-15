# bot_app/services.py
import requests

def fetch_ai_response(prompt):
    """
    Send a prompt to the AI app and fetch the response.
    """
    try:
        ai_url = "http://localhost:8000/api/openai/get-ai-response/"  # Update with actual URL
        headers = {"Content-Type": "application/json"}
        payload = {"prompt": prompt}
        response = requests.post(ai_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {str(e)}"
