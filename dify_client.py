"""
Dify API Client - Handles communication with Dify Agent
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

class DifyClient:
    def __init__(self):
        self.api_key = os.getenv("DIFY_API_KEY")
        self.api_url = os.getenv("DIFY_API_URL", "https://api.dify.ai/v1/chat-messages")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_recommendation(self, query: str, user_id: str = "user-001", conversation_id: str = ""):
        """Send query to Dify agent and get recommendation"""
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": conversation_id,
            "user": user_id
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120  # Agents can take time
            )
            response.raise_for_status()
            data = response.json()
            
            return {
                "success": True,
                "answer": data.get("answer", "No response received"),
                "conversation_id": data.get("conversation_id", ""),
                "message_id": data.get("message_id", "")
            }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. The agent is taking too long. Please try again."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API Error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }