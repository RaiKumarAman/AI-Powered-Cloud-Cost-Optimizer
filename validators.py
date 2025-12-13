"""
JSON Validators for Cloud Cost Optimizer.

This module provides validation functions for JSON responses from LLM,
ensuring data integrity and format compliance.
"""

import json
from typing import Any, Dict, List, Tuple


def validate_json_structure(data: Any, required_keys: List[str]) -> Tuple[bool, str]:
    """
    Validate that data is valid JSON and contains required keys.
    
    Args:
        data: Data to validate (dict or JSON string)
        required_keys: List of keys that must be present
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        # If data is a string, parse it
        if isinstance(data, str):
            parsed_data = json.loads(data)
        else:
            parsed_data = data
        
        # Check if it's a dictionary
        if not isinstance(parsed_data, dict):
            return False, "Response must be a JSON object (dict), not a list or primitive"
        
        # Check required keys
        missing_keys = [key for key in required_keys if key not in parsed_data]
        if missing_keys:
            return False, f"Missing required keys: {', '.join(missing_keys)}"
        
        return True, ""
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_profile(data: Any) -> Tuple[bool, str]:
    """
    Validate project profile JSON structure.
    
    Args:
        data: Profile data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if isinstance(data, str):
            parsed_data = json.loads(data)
        else:
            parsed_data = data
        
        if not isinstance(parsed_data, dict):
            return False, "Profile must be a JSON object (dict)"
        
        # Check required keys
        required_keys = ["name", "budget_inr_per_month", "description", "tech_stack", "non_functional_requirements"]
        missing_keys = [key for key in required_keys if key not in parsed_data]
        if missing_keys:
            return False, f"Missing required keys: {', '.join(missing_keys)}"
        
        # Validate types
        if not isinstance(parsed_data.get("name"), str):
            return False, "'name' must be a string"
        
        if not isinstance(parsed_data.get("budget_inr_per_month"), (int, float)):
            return False, "'budget_inr_per_month' must be a number"
        
        if not isinstance(parsed_data.get("description"), str):
            return False, "'description' must be a string"
        
        if not isinstance(parsed_data.get("tech_stack"), dict):
            return False, "'tech_stack' must be a dictionary"
        
        # Validate tech_stack keys
        expected_tech_keys = ["frontend", "backend", "database", "proxy", "hosting"]
        for key in expected_tech_keys:
            if key not in parsed_data["tech_stack"]:
                return False, f"tech_stack missing key: {key}"
        
        if not isinstance(parsed_data.get("non_functional_requirements"), list):
            return False, "'non_functional_requirements' must be a list"
        
        return True, ""
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_billing(data: Any) -> Tuple[bool, str]:
    """
    Validate mock billing JSON structure (array format).
    
    Args:
        data: Billing data to validate (array of records)
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if isinstance(data, str):
            parsed_data = json.loads(data)
        else:
            parsed_data = data
        
        # Handle both array and object with billing_records key
        if isinstance(parsed_data, dict):
            if "billing_records" in parsed_data:
                records = parsed_data["billing_records"]
            else:
                return False, "Billing data must be an array or object with 'billing_records' key"
        elif isinstance(parsed_data, list):
            records = parsed_data
        else:
            return False, "Billing data must be an array or object"
        
        if not isinstance(records, list):
            return False, "'billing_records' must be a list"
        
        if len(records) < 12:
            return False, f"Expected at least 12 billing records, got {len(records)}"
        
        if len(records) > 20:
            return False, f"Expected at most 20 billing records, got {len(records)}"
        
        # Validate each record has required fields
        required_fields = ["month", "service", "resource_id", "region", "usage_type", "usage_quantity", "unit", "cost_inr", "desc"]
        for idx, record in enumerate(records):
            if not isinstance(record, dict):
                return False, f"Record {idx} is not a dictionary"
            
            missing = [f for f in required_fields if f not in record]
            if missing:
                return False, f"Record {idx} missing fields: {', '.join(missing)}"
            
            # Validate cost_inr is a number
            if not isinstance(record.get("cost_inr"), (int, float)):
                return False, f"Record {idx}: cost_inr must be a number, got {type(record.get('cost_inr'))}"
            
            # Validate month format
            if not isinstance(record.get("month"), str) or len(record["month"]) != 7:
                return False, f"Record {idx}: month must be in YYYY-MM format"
        
        return True, ""
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_recommendations(data: Any) -> Tuple[bool, str]:
    """
    Validate cost optimization report JSON structure.
    
    Args:
        data: Report data to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        if isinstance(data, str):
            parsed_data = json.loads(data)
        else:
            parsed_data = data
        
        if not isinstance(parsed_data, dict):
            return False, "Report must be a JSON object"
        
        # Check top-level keys
        required_top_keys = ["analysis", "recommendations", "summary"]
        missing_keys = [key for key in required_top_keys if key not in parsed_data]
        if missing_keys:
            return False, f"Missing required keys: {', '.join(missing_keys)}"
        
        # Validate analysis object
        analysis = parsed_data.get("analysis", {})
        analysis_keys = ["total_monthly_cost", "budget", "budget_variance", "is_over_budget", "service_costs", "high_cost_services"]
        for key in analysis_keys:
            if key not in analysis:
                return False, f"analysis missing key: {key}"
        
        # Validate recommendations array
        if not isinstance(parsed_data.get("recommendations"), list):
            return False, "'recommendations' must be a list"
        
        if len(parsed_data["recommendations"]) < 6:
            return False, f"Expected at least 6 recommendations, got {len(parsed_data['recommendations'])}"
        
        if len(parsed_data["recommendations"]) > 10:
            return False, f"Expected at most 10 recommendations, got {len(parsed_data['recommendations'])}"
        
        # Validate each recommendation
        req_fields = ["title", "service", "current_cost", "potential_savings", "recommendation_type", "description", "implementation_effort", "risk_level", "steps", "cloud_providers"]
        for idx, rec in enumerate(parsed_data["recommendations"]):
            if not isinstance(rec, dict):
                return False, f"Recommendation {idx} is not a dictionary"
            
            missing = [f for f in req_fields if f not in rec]
            if missing:
                return False, f"Recommendation {idx} missing fields: {', '.join(missing)}"
            
            # Validate effort and risk levels
            if rec.get("implementation_effort") not in ["low", "medium", "high"]:
                return False, f"Recommendation {idx}: implementation_effort must be 'low', 'medium', or 'high'"
            
            if rec.get("risk_level") not in ["low", "medium", "high"]:
                return False, f"Recommendation {idx}: risk_level must be 'low', 'medium', or 'high'"
            
            if not isinstance(rec.get("steps"), list):
                return False, f"Recommendation {idx}: steps must be a list"
            
            if not isinstance(rec.get("cloud_providers"), list):
                return False, f"Recommendation {idx}: cloud_providers must be a list"
        
        # Validate summary object
        summary = parsed_data.get("summary", {})
        summary_keys = ["total_potential_savings", "savings_percentage", "recommendations_count", "high_impact_recommendations"]
        for key in summary_keys:
            if key not in summary:
                return False, f"summary missing key: {key}"
        
        return True, ""
    
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {str(e)}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"
