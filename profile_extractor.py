"""
Project Profile Extractor using LLM.

This module extracts structured project information from descriptions using LLM,
with no rule-based parsing.
"""

import json
from typing import Dict, Any

from llm_client import HFInferenceClient
from validators import validate_profile


class ProfileExtractor:
    """Extract project profile from description using LLM."""
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize profile extractor.
        
        Args:
            api_key: HuggingFace API key
            model: Model name
        """
        self.client = HFInferenceClient(api_key=api_key, model=model)
    
    def extract(self, project_description: str, max_retries: int = 3) -> Dict[str, Any]:
        """
        Extract project profile from description.
        
        Args:
            project_description: Project description text
            max_retries: Number of retries if JSON validation fails
            
        Returns:
            Validated project profile dictionary
        """
        prompt = self._build_prompt(project_description)
        
        for attempt in range(max_retries):
            try:
                # Query LLM
                response = self.client.query(prompt, max_retries=2, temperature=0.3)
                
                # Try to parse JSON
                profile = self._parse_response(response)
                
                # Validate structure
                is_valid, error_msg = validate_profile(profile)
                if is_valid:
                    return profile
                
                # If validation failed, retry
                if attempt < max_retries - 1:
                    print(f"Profile validation failed: {error_msg}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                
                # Last attempt failed, return best effort
                print(f"Final attempt: {error_msg}")
                return profile if isinstance(profile, dict) else {}
            
            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    print(f"JSON parsing failed: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error extracting profile: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
        
        raise Exception("Failed to extract profile after max retries")
    
    def _build_prompt(self, project_description: str) -> str:
        """
        Build LLM prompt for profile extraction.
        
        Args:
            project_description: Project description
            
        Returns:
            Formatted prompt string
        """
        return f"""Extract project information from the description and return ONLY valid JSON matching this schema:
{{
  "name": string,
  "budget_inr_per_month": integer (monthly budget in INR),
  "description": string (2-3 sentences),
  "tech_stack": {{
    "frontend": string | null,
    "backend": string | null,
    "database": string | null,
    "proxy": string | null,
    "hosting": string | null
  }},
  "non_functional_requirements": string[] (array of requirements like "high availability", "low latency", etc)
}}

Project Description:
{project_description}

Rules:
- budget_inr_per_month MUST be an integer
- Extract tech stack components from the description
- If a component is not mentioned, use null
- non_functional_requirements should be an empty array if none are mentioned
- Return ONLY the JSON object, no other text
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from response text.
        
        Args:
            response_text: Raw response from LLM
            
        Returns:
            Parsed JSON dictionary
        """
        # Try direct parsing
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON from text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                json_str = response_text[start_idx:end_idx + 1]
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        raise json.JSONDecodeError("Could not extract valid JSON", response_text, 0)
