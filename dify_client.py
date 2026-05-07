"""
Dify API Client - Fixed for 400 errors
"""
import requests
import os

try:
    import streamlit as st
    HAS_STREAMLIT = True
except ImportError:
    HAS_STREAMLIT = False

from dotenv import load_dotenv
load_dotenv()


class DifyClient:
    def __init__(self):
        # Try Streamlit secrets first (cloud), fall back to env vars (local)
        if HAS_STREAMLIT and hasattr(st, 'secrets') and 'DIFY_API_KEY' in st.secrets:
            self.api_key = st.secrets["DIFY_API_KEY"]
            self.api_url = st.secrets.get(
                "DIFY_API_URL", 
                "https://api.dify.ai/v1/chat-messages"
            )
        else:
            self.api_key = os.getenv("DIFY_API_KEY")
            self.api_url = os.getenv(
                "DIFY_API_URL", 
                "https://api.dify.ai/v1/chat-messages"
            )
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_recommendation(self, query: str, user_id: str = "user-001", conversation_id: str = ""):
        """Send query to Dify agent and get recommendation"""
        
        # Build payload — only include conversation_id if it's not empty
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "user": user_id
        }
        
        # CRITICAL FIX: Only add conversation_id if it has a value
        # Empty conversation_id causes 400 error in some Dify versions
        if conversation_id and conversation_id.strip():
            payload["conversation_id"] = conversation_id
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120
            )
            
            # Detailed error handling
            if response.status_code != 200:
                error_msg = f"Status {response.status_code}"
                try:
                    error_json = response.json()
                    error_msg += f" | {error_json.get('message', 'Unknown error')}"
                    error_msg += f" | Code: {error_json.get('code', 'N/A')}"
                except:
                    error_msg += f" | Response: {response.text[:300]}"
                
                return {
                    "success": False,
                    "error": error_msg
                }
            
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
                "error": "Request timed out (120s). The agent is taking too long. Try a simpler query."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Connection error. Check your internet connection."
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"Request error: {str(e)}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }