from flask import Blueprint, request, jsonify
import requests
import json
import re


ai_bp = Blueprint('ai', __name__, url_prefix='/api/ai')

# API Key and User ID (consider using environment variables for security)
API_KEY = "cuua2u8f3ojkcr6rb0b0"  # Replace with your actual API key
USER_ID = "1"


# Global variable to store the current conversation ID
current_conversation_id = None

def create_conversation_api():
    """Creates a new conversation with the LLM API."""
    global current_conversation_id
    url = "https://agent.tongji.edu.cn/api/proxy/api/v1/create_conversation"
    headers = {
        'Apikey': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "AppKey": API_KEY,
        "Inputs": {"var": "value"}, # Optional
        "UserID": USER_ID
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raises an exception for bad status codes
        conversation_id = response.json().get('Conversation', {}).get('AppConversationID')
        if conversation_id:
            current_conversation_id = conversation_id
            return conversation_id
        else:
            print(f"Error in API response (create_conversation): {response.json()}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed (create_conversation): {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response (create_conversation): {response.text}")
        return None

def send_query_api(conversation_id, query):
    """Sends a query to the LLM API and gets a streaming response."""
    url = "https://agent.tongji.edu.cn/api/proxy/api/v1/chat_query"
    headers = {
        'Apikey': API_KEY,
        'Content-Type': 'application/json'
    }
    payload = {
        "Query": query,
        "AppConversationID": conversation_id,
        "AppKey": API_KEY,
        "ResponseMode": "streaming",
        "UserID": USER_ID
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response.encoding = 'utf-8'

        full_answer = ""
        # for line in response.iter_lines(decode_unicode=True):
        #     if line and line.startswith('data:'):
        #         try:
        #             # Remove 'data: ' prefix and parse JSON
        #             json_str = line[len('data: '):]
        #             json_data = json.loads(json_str)
        #             if "answer" in json_data:
        #                 full_answer += json_data["answer"]
        #         except json.JSONDecodeError:
        #             # print(f"Skipping line, not valid JSON: {line}") # For debugging
        #             continue # Skip if a line fragment is not valid JSON
        response_text = response.text
        json_pattern = r'data: (\{.*?\})'
        matches = re.findall(json_pattern, response_text)
        for match in matches:
            try:
                json_data = json.loads(match)
                if "answer" in json_data:
                    # 对于流式响应，累积答案片段
                    answer_segment = json_data["answer"]
                    full_answer += answer_segment
            except json.JSONDecodeError:
                continue
        return full_answer
    except requests.exceptions.RequestException as e:
        print(f"Request failed (send_query): {e}")
        return "Error: Could not reach the AI service."
    except json.JSONDecodeError:
        print(f"Failed to decode JSON in streaming response: {response.text}")
        return "Error: Invalid response from AI service."


@ai_bp.route('/chat', methods=['POST'])
def chat():
    global current_conversation_id
    data = request.json
    user_query = data.get('query')

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    # Create a new conversation if one doesn't exist
    # For this project, we'll create a new conversation for each interaction
    # to ensure only the current dialogue is processed, as per requirements.
    # If you want to maintain a session, you might adjust this logic.
    # However, the requirement is "only the current conversation",
    # implying a stateless approach per query from the frontend perspective,
    # but the backend API might require a conversation ID.
    # Let's re-create conversation for simplicity and to match test.py flow
    # when it's run multiple times (it creates a new conversation each run).
    # For a web app, you might want to create it once when the page loads
    # or manage it more carefully if the API supports longer sessions.

    # For this version, we will try to use an existing conversation ID
    # or create a new one if none exists. This is closer to how `test.py`
    # first creates a conversation and then uses it.
    # A truly "current dialogue only" might mean each query is a new conversation.
    # Let's assume we want one conversation per user session on the webpage.
    # Since we don't have user sessions here, we'll use one global ID.

    if not current_conversation_id:
        if not create_conversation_api():
             return jsonify({"error": "Failed to create a new conversation with the AI service."}), 500

    if not current_conversation_id: # Check again if creation failed
        return jsonify({"error": "Failed to initialize conversation."}), 500

    ai_response = send_query_api(current_conversation_id, user_query)

    if ai_response is None: # send_query_api can return None on error
        return jsonify({"error": "Failed to get response from AI."}), 500

    return jsonify({"user_query": user_query, "ai_response": ai_response})

@ai_bp.route('/reset_conversation', methods=['POST'])
def reset_conversation():
    global current_conversation_id
    new_conversation_id = create_conversation_api()
    if new_conversation_id:
        return jsonify({"message": "Conversation reset successfully.", "conversation_id": new_conversation_id}), 200
    else:
        return jsonify({"error": "Failed to reset conversation."}), 500