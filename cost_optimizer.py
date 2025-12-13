
import json
import os
import sys
from typing import Dict, Any

from profile_extractor import ProfileExtractor
from billing_generator import BillingGenerator
from cost_analyzer import CostAnalyzer
from utils import (
    save_json, 
    load_json, 
    save_text, 
    load_text,
    load_env_file,
    create_project_structure
)


class CloudCostOptimizer:
    
    def __init__(self):
        """Initialize the optimizer."""
        self.project_description = None
        self.project_profile = None
        self.billing_data = None
        self.cost_report = None
        self.budget_threshold = 5000
        
        # Load environment
        self._load_env()
        
        # Create project structure
        create_project_structure()
    
    def _load_env(self):
        """Load environment configuration."""
        env_vars = load_env_file(".env")
        self.budget_threshold = float(env_vars.get("BUDGET_THRESHOLD", 5000))
    
    def run(self):
        """Run the main CLI menu."""
        print("\n" + "="*60)
        print("  AI-Powered Cloud Cost Optimizer (LLM-Driven)")
        print("="*60 + "\n")
        
        while True:
            self._display_menu()
            choice = input("\nEnter your choice (1-5): ").strip()
            
            if choice == "1":
                self._menu_enter_description()
            elif choice == "2":
                self._menu_run_analysis()
            elif choice == "3":
                self._menu_view_recommendations()
            elif choice == "4":
                self._menu_export_report()
            elif choice == "5":
                print("\nExiting Cloud Cost Optimizer. Goodbye!\n")
                sys.exit(0)
            else:
                print("\nInvalid choice. Please enter 1-5.\n")
    
    def _display_menu(self):
        """Display main menu options."""
        print("OPTIONS:")
        print("  1. Enter New Project Description")
        print("  2. Run Complete Cost Analysis")
        print("  3. View Recommendations")
        print("  4. Export Report")
        print("  5. Exit")
    
    def _menu_enter_description(self):
        """Menu option: Enter project description."""
        print("\n" + "-"*60)
        print("Enter New Project Description")
        print("-"*60)
        
        print("\nDescribe your cloud project in detail.")
        print("Include: services used, cloud platforms, team size, current costs.")
        print("(Type 'END' on a new line to finish)\n")
        
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        
        self.project_description = "\n".join(lines).strip()
        
        if not self.project_description:
            print("\nNo description entered.")
            return
        
        # Save description
        save_text(self.project_description, "sample_outputs/project_description.txt")
        print(f"\n✓ Description saved ({len(self.project_description)} characters)")
        
        # Extract profile
        print("\nExtracting project profile using LLM...")
        try:
            extractor = ProfileExtractor()
            self.project_profile = extractor.extract(self.project_description)
            
            save_json(self.project_profile, "sample_outputs/project_profile.json")
            print("✓ Profile extracted and saved")
            
            print(f"\nProject Profile:")
            print(f"  Name: {self.project_profile.get('name')}")
            print(f"  Budget (INR): ₹{self.project_profile.get('budget_inr_per_month')} /month")
            print(f"  Description: {self.project_profile.get('description')[:60]}...")
        
        except Exception as e:
            print(f"✗ Error extracting profile: {str(e)}")
            self.project_profile = None
    
    def _menu_run_analysis(self):
        """Menu option: Run complete analysis."""
        print("\n" + "-"*60)
        print("Run Complete Cost Analysis")
        print("-"*60)
        
        # Check prerequisites
        if not self.project_description:
            print("\n✗ Please enter a project description first (Option 1)")
            return
        
        if not self.project_profile:
            print("\nNo profile found. Would you like to extract one? (y/n): ", end="")
            if input().strip().lower() != 'y':
                return
            
            print("Extracting profile...")
            try:
                extractor = ProfileExtractor()
                self.project_profile = extractor.extract(self.project_description)
                save_json(self.project_profile, "sample_outputs/project_profile.json")
            except Exception as e:
                print(f"✗ Error: {str(e)}")
                return
        
        # Generate billing data
        print("\nGenerating synthetic billing data (12-20 records)...")
        try:
            generator = BillingGenerator()
            billing_array = generator.generate(self.project_profile)
            self.billing_data = billing_array  # Store as list directly
            save_json(billing_array, "sample_outputs/mock_billing.json")
            print(f"✓ Generated {len(billing_array)} billing records")
        except Exception as e:
            print(f"✗ Error generating billing: {str(e)}")
            return
        
        # Analyze costs
        print("\nAnalyzing costs and generating recommendations...")
        try:
            analyzer = CostAnalyzer(budget_threshold=self.budget_threshold)
            self.cost_report = analyzer.analyze(self.project_profile, billing_array)
            save_json(self.cost_report, "sample_outputs/cost_optimization_report.json")
            print("✓ Cost analysis complete")
        except Exception as e:
            print(f"✗ Error analyzing costs: {str(e)}")
            return
        
        # Display summary
        self._display_cost_summary()
    
    def _menu_view_recommendations(self):
        """Menu option: View recommendations."""
        print("\n" + "-"*60)
        print("Cost Optimization Recommendations")
        print("-"*60)
        
        if not self.cost_report:
            # Try to load from file
            self.cost_report = load_json("sample_outputs/cost_optimization_report.json")
            if not self.cost_report:
                print("\n✗ No cost analysis available. Run analysis first (Option 2)")
                return
        
        self._display_recommendations()
    
    def _menu_export_report(self):
        """Menu option: Export report."""
        print("\n" + "-"*60)
        print("Export Report")
        print("-"*60)
        
        if not self.cost_report:
            self.cost_report = load_json("sample_outputs/cost_optimization_report.json")
            if not self.cost_report:
                print("\n✗ No report available. Run analysis first (Option 2)")
                return
        
        # Generate HTML report
        html_content = self._generate_html_report()
        
        html_path = "sample_outputs/cost_optimization_report.html"
        save_text(html_content, html_path)
        print(f"\n✓ Report exported to {html_path}")
        
        # Also show JSON path
        json_path = "sample_outputs/cost_optimization_report.json"
        print(f"✓ JSON report available at {json_path}")
    
    def _display_cost_summary(self):
        """Display cost analysis summary."""
        if not self.cost_report:
            return
        
        analysis = self.cost_report.get("analysis", {})
        summary = self.cost_report.get("summary", {})
        
        print("\n" + "-"*40)
        print("COST ANALYSIS SUMMARY")
        print("-"*40)
        print(f"Total Monthly Cost: ₹{analysis.get('total_monthly_cost', 0):,.2f}")
        print(f"Budget:             ₹{analysis.get('budget', 0):,.2f}")
        print(f"Budget Variance:    ₹{analysis.get('budget_variance', 0):,.2f}")
        
        if analysis.get("is_over_budget"):
            print("⚠️  OVER BUDGET")
        else:
            print("✓ Within budget")
        
        print(f"\nTotal Potential Savings: ₹{summary.get('total_potential_savings', 0):,.2f}")
        print(f"Savings Percentage: {summary.get('savings_percentage', 0):.1f}%")
        print(f"Number of Recommendations: {summary.get('recommendations_count', 0)}")
    
    def _display_recommendations(self):
        """Display cost optimization recommendations."""
        recommendations = self.cost_report.get("recommendations", [])
        
        if not recommendations:
            print("\nNo recommendations available.")
            return
        
        summary = self.cost_report.get("summary", {})
        total_savings = summary.get("total_potential_savings", 0)
        
        print(f"\nTotal Potential Savings: ₹{total_savings:,.2f}\n")
        
        for idx, rec in enumerate(recommendations[:5], 1):
            print(f"{idx}. {rec.get('title', 'Unknown')}")
            print(f"   Service: {rec.get('service', 'Unknown')}")
            print(f"   Potential Savings: ₹{rec.get('potential_savings', 0):,.2f}")
            print(f"   Type: {rec.get('recommendation_type', 'Unknown')}")
            print(f"   Effort: {rec.get('implementation_effort', 'Unknown')}")
            print(f"   Risk: {rec.get('risk_level', 'Unknown')}")
            print()
        
        if len(recommendations) > 5:
            print(f"... and {len(recommendations) - 5} more recommendations\n")
    
    def _generate_html_report(self) -> str:
       
        if not self.cost_report:
            return ""
        
        analysis = self.cost_report.get("analysis", {})
        recommendations = self.cost_report.get("recommendations", [])
        summary = self.cost_report.get("summary", {})
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Cloud Cost Optimization Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .container {{ max-width: 1000px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        h1 {{ color: #333; border-bottom: 2px solid #007bff; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        .metric {{ display: inline-block; margin: 10px 20px 10px 0; padding: 15px; background: #f9f9f9; border-left: 4px solid #007bff; border-radius: 4px; }}
        .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
        .metric-label {{ font-size: 12px; color: #666; text-transform: uppercase; }}
        .over-budget {{ border-left-color: #dc3545; }}
        .over-budget .metric-value {{ color: #dc3545; }}
        .within-budget {{ border-left-color: #28a745; }}
        .within-budget .metric-value {{ color: #28a745; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #007bff; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .footer {{ margin-top: 30px; color: #666; font-size: 12px; text-align: center; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Cloud Cost Optimization Report</h1>
        
        <h2>Cost Analysis Summary</h2>
        <div class="metric {'over-budget' if analysis.get('is_over_budget') else 'within-budget'}">
            <div class="metric-label">Total Monthly Cost</div>
            <div class="metric-value">₹{analysis.get('total_monthly_cost', 0):,.0f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Budget</div>
            <div class="metric-value">₹{analysis.get('budget', 0):,.0f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Budget Variance</div>
            <div class="metric-value">₹{analysis.get('budget_variance', 0):,.0f}</div>
        </div>
        <div class="metric">
            <div class="metric-label">Total Potential Savings</div>
            <div class="metric-value">₹{summary.get('total_potential_savings', 0):,.0f}</div>
        </div>
        
        <h2>High-Cost Services</h2>
        <table>
            <tr>
                <th>Service</th>
                <th>Monthly Cost (INR)</th>
            </tr>
"""
        
        for service, cost in analysis.get("high_cost_services", {}).items():
            html += f"""            <tr>
                <td>{service}</td>
                <td>₹{cost:,.2f}</td>
            </tr>
"""
        
        html += """        </table>
        
        <h2>Cost Optimization Recommendations</h2>
        <table>
            <tr>
                <th>Recommendation</th>
                <th>Service</th>
                <th>Potential Savings</th>
                <th>Type</th>
                <th>Effort</th>
                <th>Risk</th>
            </tr>
"""
        
        for rec in recommendations[:10]:
            html += f"""            <tr>
                <td><strong>{rec.get('title', 'Unknown')}</strong></td>
                <td>{rec.get('service', 'Unknown')}</td>
                <td>₹{rec.get('potential_savings', 0):,.0f}</td>
                <td>{rec.get('recommendation_type', 'Unknown')}</td>
                <td>{rec.get('implementation_effort', 'Unknown')}</td>
                <td>{rec.get('risk_level', 'Unknown')}</td>
            </tr>
"""
        
        html += f"""        </table>
        
        <h2>Summary</h2>
        <ul>
            <li><strong>Total Potential Savings:</strong> ₹{summary.get('total_potential_savings', 0):,.0f}</li>
            <li><strong>Savings Percentage:</strong> {summary.get('savings_percentage', 0):.1f}%</li>
            <li><strong>Total Recommendations:</strong> {summary.get('recommendations_count', 0)}</li>
            <li><strong>High-Impact Recommendations:</strong> {summary.get('high_impact_recommendations', 0)}</li>
        </ul>
        
        <div class="footer">
            <p>Generated by AI-Powered Cloud Cost Optimizer</p>
            <p>For more details, see the JSON report files</p>
        </div>
    </div>
</body>
</html>
"""
        return html


def main():
    """Main entry point."""
    try:
        optimizer = CloudCostOptimizer()
        optimizer.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Fatal error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

