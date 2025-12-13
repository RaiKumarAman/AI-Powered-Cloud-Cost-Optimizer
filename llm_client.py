
import json
import os
from typing import Dict, Any
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from utils import parse_json_response

# Load environment variables from .env file
load_dotenv()


class HFInferenceClient:
    """Client for HuggingFace Inference API."""
    
    def __init__(self, api_key: str = None, model: str = None):
        
        # Load from environment if not provided
        api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        model = model or os.getenv("HUGGINGFACE_MODEL", "meta-llama/Meta-Llama-3-8B-Instruct")
        
        if not api_key:
            raise ValueError(
                "HUGGINGFACE_API_KEY not found. "
                "Please set it in .env file or pass it as argument."
            )
        
        self.api_key = api_key
        self.model = model
        self.client = InferenceClient(api_key=api_key)
    
    def query(self, prompt: str, max_retries: int = 3, temperature: float = 0.7) -> str:
        
        for attempt in range(max_retries):
            try:
                # Use conversational API with system and user messages
                messages = [
                    {"role": "system", "content": "You are a helpful assistant that provides structured JSON responses."},
                    {"role": "user", "content": prompt}
                ]
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=2000,
                    top_p=0.9
                )
                
                # Extract the response text
                if hasattr(response, 'choices') and len(response.choices) > 0:
                    message = response.choices[0].message
                    if hasattr(message, 'content'):
                        return message.content
                    else:
                        return str(message)
                
                return str(response)
            
            except Exception as e:
                error_str = str(e).lower()
                
                # Check for specific error types
                if "model is overloaded" in error_str or "overloaded" in error_str:
                    if attempt < max_retries - 1:
                        print(f"Model overloaded, retrying... (attempt {attempt + 1}/{max_retries})")
                        continue
                
                elif "not found" in error_str or "404" in error_str:
                    if attempt < max_retries - 1:
                        print(f"Model not found, retrying... (attempt {attempt + 1}/{max_retries})")
                        continue
                
                elif "timeout" in error_str or "timed out" in error_str:
                    if attempt < max_retries - 1:
                        print(f"Request timeout, retrying... (attempt {attempt + 1}/{max_retries})")
                        continue
                
                elif "rate limit" in error_str or "rate_limit" in error_str:
                    if attempt < max_retries - 1:
                        print(f"Rate limited, retrying... (attempt {attempt + 1}/{max_retries})")
                        continue
                
                else:
                    if attempt < max_retries - 1:
                        print(f"Error: {str(e)}, retrying... (attempt {attempt + 1}/{max_retries})")
                        continue
                
                # Final attempt failed
                raise Exception(f"HuggingFace API Error: {str(e)}")
        
        raise Exception("Max retries exceeded")
    
    def query_json(self, prompt: str, max_retries: int = 3) -> Dict[str, Any]:
       
        response_text = self.query(prompt, max_retries=max_retries, temperature=0.3)
        return parse_json_response(response_text)

