"""
Dify API Client - Fixed for Agent apps (streaming mode)
"""
import requests
import os
import json

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
        """
        Send query to Dify Agent and get recommendation.
        Uses STREAMING mode (required for Agent apps).
        """
        
        # Agent apps require streaming mode
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "streaming",  # CHANGED from "blocking" to "streaming"
            "user": user_id
        }
        
        # Only include conversation_id if it has a value
        if conversation_id and conversation_id.strip():
            payload["conversation_id"] = conversation_id
        
        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=120,
                stream=True  # Enable streaming
            )
            
            # Check for HTTP errors
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
            
            # Parse streaming response
            full_answer = ""
            conversation_id_received = ""
            message_id_received = ""
            
            for line in response.iter_lines():
                if not line:
                    continue
                
                # Decode the line
                line_str = line.decode('utf-8')
                
                # Streaming responses come as "data: {json}"
                if line_str.startswith('data: '):
                    json_str = line_str[6:]  # Remove "data: " prefix
                    
                    try:
                        data = json.loads(json_str)
                        event_type = data.get('event', '')
                        
                        # Handle different event types
                        if event_type == 'agent_message':
                            # Agent message chunks
                            full_answer += data.get('answer', '')
                            conversation_id_received = data.get('conversation_id', conversation_id_received)
                            message_id_received = data.get('message_id', message_id_received)
                        
                        elif event_type == 'message':
                            # Regular message chunks
                            full_answer += data.get('answer', '')
                            conversation_id_received = data.get('conversation_id', conversation_id_received)
                            message_id_received = data.get('message_id', message_id_received)
                        
                        elif event_type == 'message_end':
                            # End of message
                            conversation_id_received = data.get('conversation_id', conversation_id_received)
                        
                        elif event_type == 'error':
                            # Error event
                            return {
                                "success": False,
                                "error": f"Agent error: {data.get('message', 'Unknown error')}"
                            }
                    
                    except json.JSONDecodeError:
                        # Skip lines that can't be parsed
                        continue
            
            # Return the complete response
            if full_answer:
                return {
                    "success": True,
                    "answer": full_answer,
                    "conversation_id": conversation_id_received,
                    "message_id": message_id_received
                }
            else:
                return {
                    "success": False,
                    "error": "No response received from agent"
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out (120s). Agent took too long. Try a simpler query."
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