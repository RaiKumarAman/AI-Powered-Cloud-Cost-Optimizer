

import json
from typing import Dict, Any, List
from datetime import datetime

from llm_client import HFInferenceClient
from validators import validate_recommendations


class CostAnalyzer:
   
    def __init__(self, api_key: str = None, model: str = None, budget_threshold: float = 5000):
        
        self.client = HFInferenceClient(api_key=api_key, model=model)
        self.budget_threshold = budget_threshold
    
    def analyze(self, project_profile: Dict[str, Any], billing_data: List[Dict[str, Any]]) -> Dict[str, Any]:
       
        # Calculate cost metrics
        metrics = self._calculate_metrics(billing_data, project_profile)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            project_profile, 
            billing_data, 
            metrics
        )
        
        # Compile report with new schema
        report = {
            "analysis": {
                "total_monthly_cost": metrics["total_cost"],
                "budget": project_profile.get("budget_inr_per_month", 50000),
                "budget_variance": metrics["total_cost"] - project_profile.get("budget_inr_per_month", 50000),
                "is_over_budget": metrics["total_cost"] > project_profile.get("budget_inr_per_month", 50000),
                "service_costs": metrics["cost_per_service"],
                "high_cost_services": {s["service"]: s["cost"] for s in metrics["high_cost_services"]}
            },
            "recommendations": recommendations.get("recommendations", []),
            "summary": recommendations.get("summary", {})
        }
        
        return report
    
    def _calculate_metrics(self, billing_data: List[Dict[str, Any]], project_profile: Dict[str, Any]) -> Dict[str, Any]:
        
        # Handle both list and dict formats
        if isinstance(billing_data, dict) and "billing_records" in billing_data:
            records = billing_data["billing_records"]
        else:
            records = billing_data if isinstance(billing_data, list) else []
        
        # Total cost
        total_cost = sum(record.get("cost_inr", 0) for record in records)
        
        # Cost per service
        cost_per_service = {}
        for record in records:
            service = record.get("service", "Unknown")
            cost = record.get("cost_inr", 0)
            cost_per_service[service] = cost_per_service.get(service, 0) + cost
        
        # High cost services (top 5)
        high_cost_services = sorted(
            cost_per_service.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        return {
            "total_cost": round(total_cost, 2),
            "cost_per_service": {k: round(v, 2) for k, v in cost_per_service.items()},
            "high_cost_services": [
                {"service": service, "cost": round(cost, 2)}
                for service, cost in high_cost_services
            ]
        }
    
    def _generate_recommendations(
        self, 
        project_profile: Dict[str, Any],
        billing_data: List[Dict[str, Any]],
        metrics: Dict[str, Any],
        max_retries: int = 3
    ) -> Dict[str, Any]:
        
        prompt = self._build_recommendations_prompt(
            project_profile,
            billing_data,
            metrics
        )
        
        for attempt in range(max_retries):
            try:
                # Query LLM
                response = self.client.query(prompt, max_retries=2, temperature=0.3)
                
                # Parse JSON
                recommendations = self._parse_response(response)
                
                # Validate structure
                is_valid, error_msg = validate_recommendations(recommendations)
                if is_valid:
                    return recommendations
                
                # If validation failed, retry
                if attempt < max_retries - 1:
                    print(f"Recommendations validation failed: {error_msg}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                
                return recommendations if isinstance(recommendations, dict) else {}
            
            except json.JSONDecodeError as e:
                if attempt < max_retries - 1:
                    print(f"JSON parsing failed: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"Error generating recommendations: {str(e)}")
                    print(f"Retrying... (attempt {attempt + 1}/{max_retries})")
                    continue
                raise
        
        raise Exception("Failed to generate recommendations after max retries")
    
    def _build_recommendations_prompt(
        self,
        project_profile: Dict[str, Any],
        billing_data: List[Dict[str, Any]],
        metrics: Dict[str, Any]
    ) -> str:
       
        name = project_profile.get("name", "Unknown")
        budget = project_profile.get("budget_inr_per_month", 50000)
        tech_stack = project_profile.get("tech_stack", {})
        high_cost = metrics["high_cost_services"]
        
        return f"""Generate cost optimization recommendations for a cloud project.

Project Details:
- Name: {name}
- Budget: ₹{budget}/month
- Current Monthly Cost: ₹{metrics['total_cost']}
- Budget Variance: ₹{metrics['total_cost'] - budget}
- Tech Stack: {json.dumps(tech_stack)}
- High Cost Services: {", ".join([f"{s['service']} (₹{s['cost']})" for s in high_cost[:3]])}

Generate 6-10 specific, actionable cost optimization recommendations covering:
- Reserved Instances/Commitments
- Auto-scaling & Right-sizing
- Multi-cloud & Open-source alternatives
- Caching & Data optimization
- Serverless & Managed services

Return ONLY valid JSON with this exact structure:
{{
  "analysis": {{
    "total_monthly_cost": {metrics['total_cost']},
    "budget": {budget},
    "budget_variance": {metrics['total_cost'] - budget},
    "is_over_budget": {str(metrics['total_cost'] > budget).lower()},
    "service_costs": {json.dumps(metrics['cost_per_service'])},
    "high_cost_services": {json.dumps({s['service']: s['cost'] for s in high_cost})}
  }},
  "recommendations": [
    {{
      "title": "Recommendation Title",
      "service": "Service Name",
      "current_cost": number (current monthly cost in INR),
      "potential_savings": number (estimated savings in INR),
      "recommendation_type": string (e.g., "Reserved Instances", "Auto-scaling", "Right-sizing"),
      "description": "Detailed explanation of the recommendation",
      "implementation_effort": "low|medium|high",
      "risk_level": "low|medium|high",
      "steps": ["Step 1", "Step 2", "Step 3"],
      "cloud_providers": ["AWS", "Azure", "GCP", "Open-source"]
    }}
  ],
  "summary": {{
    "total_potential_savings": number (sum of all potential savings),
    "savings_percentage": number (% of total monthly cost),
    "recommendations_count": number,
    "high_impact_recommendations": number (count of high-impact recommendations)
  }}
}}

Rules:
- All costs in INR
- Ensure 6-10 recommendations
- Potential savings should be realistic (typically 10-40% of service cost)
- Include both AWS and cloud-agnostic recommendations
- Return ONLY the JSON object, no other text
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        
        # Try direct parsing
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            pass
        
        # Try to extract JSON object from text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                json_str = response_text[start_idx:end_idx + 1]
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        raise json.JSONDecodeError("Could not extract valid JSON", response_text, 0)

