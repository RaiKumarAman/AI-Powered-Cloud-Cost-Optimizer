

import json
from typing import Dict, Any, List

from llm_client import HFInferenceClient
from validators import validate_billing


class BillingGenerator:
   
    
    def __init__(self, api_key: str = None, model: str = None):
       
        self.client = HFInferenceClient(api_key=api_key, model=model)
    
    def generate(self, project_profile: Dict[str, Any], max_retries: int = 3) -> List[Dict[str, Any]]:
       
        prompt = self._build_prompt(project_profile)
        
        for attempt in range(max_retries):
            try:
                # Query LLM
                response = self.client.query(prompt, max_retries=2, temperature=0.5)
                
                # Parse JSON
                billing_data = self._parse_response(response)
                
                # Validate structure
                is_valid, error_msg = validate_billing(billing_data)
                if is_valid:
                    return billing_data
                
                # If validation failed, retry
                if attempt < max_retries - 1:
                    print(f"Billing validation failed: {error_msg}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                
                # Last attempt
                print(f"Final attempt: {error_msg}")
                return billing_data if isinstance(billing_data, list) else []
            
            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    print(f"JSON parsing failed: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error generating billing: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
        
        raise Exception("Failed to generate billing data after max retries")
    
    def _build_prompt(self, project_profile: Dict[str, Any]) -> str:
        
        name = project_profile.get("name", "Unknown Project")
        budget = project_profile.get("budget_inr_per_month", 50000)
        description = project_profile.get("description", "")
        tech_stack = project_profile.get("tech_stack", {})
        
        return f"""Generate realistic synthetic cloud billing records for the following project:
Project: {name}
Budget: ₹{budget}/month
Description: {description}
Tech Stack: {json.dumps(tech_stack)}

Return a JSON array with 12-20 billing records. Each record must match this schema:
{{
  "month": "YYYY-MM",
  "service": string (e.g., "Compute", "Database", "Storage", "CDN", "Networking"),
  "resource_id": string (e.g., "instance-001", "db-primary"),
  "region": string (e.g., "ap-south-1", "us-east-1", "europe-west1"),
  "usage_type": string (e.g., "On-Demand", "Reserved", "Spot"),
  "usage_quantity": number,
  "unit": string (e.g., "hours", "GB", "requests", "GB-transfer"),
  "cost_inr": number (realistic cost in INR),
  "desc": string (human-readable description, 1 line)
}}

Rules:
- Total monthly cost should be close to the budget (±10%)
- Use realistic service costs for India region (ap-south-1)
- Include diverse services: compute, database, storage, networking, monitoring
- Use current month (2025-12) and previous month (2025-11)
- All costs in INR
- Generate 12-20 records
- Return ONLY the JSON array, no other text

Example format:
[
  {{
    "month": "2025-12",
    "service": "Compute",
    "resource_id": "web-server-01",
    "region": "ap-south-1",
    "usage_type": "On-Demand",
    "usage_quantity": 720,
    "unit": "hours",
    "cost_inr": 8640,
    "desc": "Web application server t3.medium instance"
  }}
]
"""
    
    def _parse_response(self, response_text: str) -> List[Dict[str, Any]]:
        
        # Try direct parsing (for array format)
        try:
            parsed = json.loads(response_text)
            if isinstance(parsed, list):
                return parsed
            elif isinstance(parsed, dict) and 'billing_records' in parsed:
                return parsed.get('billing_records', [])
            return [parsed] if isinstance(parsed, dict) else []
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON array from text
        start_idx = response_text.find('[')
        if start_idx != -1:
            end_idx = response_text.rfind(']')
            if end_idx != -1 and end_idx > start_idx:
                try:
                    json_str = response_text[start_idx:end_idx + 1]
                    parsed = json.loads(json_str)
                    if isinstance(parsed, list):
                        return parsed
                except json.JSONDecodeError:
                    pass
        
        # Try to extract JSON object from text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                json_str = response_text[start_idx:end_idx + 1]
                parsed = json.loads(json_str)
                if isinstance(parsed, dict) and 'billing_records' in parsed:
                    return parsed.get('billing_records', [])
            except json.JSONDecodeError:
                pass
        
        raise json.JSONDecodeError("Could not extract valid JSON", response_text, 0)

