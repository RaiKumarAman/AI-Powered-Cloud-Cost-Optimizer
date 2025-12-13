

import json
import os
from pathlib import Path
from typing import Any, Dict


def load_env_file(env_path: str = ".env") -> Dict[str, str]:
    
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
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Error loading JSON from {filepath}: {str(e)}")
    return {}


def save_text(content: str, filepath: str) -> bool:
    
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error saving text to {filepath}: {str(e)}")
        return False


def load_text(filepath: str) -> str:
    
    try:
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                return f.read()
    except Exception as e:
        print(f"Error loading text from {filepath}: {str(e)}")
    return ""


def format_currency(amount: float) -> str:
    
    return f"inr{amount:,.2f}"


def format_percentage(value: float) -> str:
    
    return f"{value:.1f}%"


def ensure_json_string(data: Any) -> str:
   
    if isinstance(data, str):
        return data
    return json.dumps(data)


def parse_json_response(response_text: str) -> Dict[str, Any]:
   
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

