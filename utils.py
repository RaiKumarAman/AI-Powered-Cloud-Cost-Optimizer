"""
Utility functions for Cloud Cost Optimizer.

This module provides helper functions for file I/O, formatting, and data processing.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict


def load_env_file(env_path: str = ".env") -> Dict[str, str]:
    """
    Load environment variables from .env file.
    
    Args:
        env_path: Path to .env file
        
    Returns:
        Dictionary of environment variables
    """
    env_vars = {}
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        env_vars[key.strip()] = value.strip()
    return env_vars


def save_json(data: Dict[str, Any], filepath: str) -> bool:
    """
    Save data as JSON to file.
    
    Args:
        data: Data to save
        filepath: Path to output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving JSON to {filepath}: {str(e)}")
        return False


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load JSON from file.
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data or empty dict if file not found
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {filepath}: {str(e)}")
    return {}


def save_text(content: str, filepath: str) -> bool:
    """
    Save text content to file.
    
    Args:
        content: Text content
        filepath: Path to output file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving text to {filepath}: {str(e)}")
        return False


def load_text(filepath: str) -> str:
    """
    Load text from file.
    
    Args:
        filepath: Path to text file
        
    Returns:
        File content or empty string if not found
    """
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
    except Exception as e:
        print(f"Error loading text from {filepath}: {str(e)}")
    return ""


def format_currency(amount: float) -> str:
    """
    Format amount as USD currency string.
    
    Args:
        amount: Numeric amount
        
    Returns:
        Formatted currency string
    """
    return f"${amount:,.2f}"


def format_percentage(value: float) -> str:
    """
    Format value as percentage string.
    
    Args:
        value: Numeric value
        
    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"


def ensure_json_string(data: Any) -> str:
    """
    Ensure data is a JSON string.
    
    Args:
        data: Data to convert
        
    Returns:
        JSON string representation
    """
    if isinstance(data, str):
        return data
    return json.dumps(data)


def parse_json_response(response_text: str) -> Dict[str, Any]:
    """
    Extract and parse JSON from LLM response text.
    
    Args:
        response_text: Raw response text from LLM
        
    Returns:
        Parsed JSON dictionary
    """
    # Try direct parsing first
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from response (between first { and last })
    start_idx = response_text.find('{')
    end_idx = response_text.rfind('}')
    
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        try:
            json_str = response_text[start_idx:end_idx + 1]
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    return {}


def create_project_structure():
    """Create necessary project directories."""
    directories = [
        "sample_outputs",
        "temp"
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
