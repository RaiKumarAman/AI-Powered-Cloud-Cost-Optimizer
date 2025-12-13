# AI-Powered Cloud Cost Optimizer (LLM-Driven)

## Overview

An intelligent, menu-driven CLI application that uses Large Language Models (LLM) via HuggingFace Inference API to extract cloud project information, generate synthetic billing data, analyze costs, and provide multi-cloud cost optimization recommendations.

**Key Features:**
- 🤖 **LLM-Driven Profile Extraction** - Uses AI to extract structured project profiles from natural language descriptions
- 💰 **Synthetic Billing Generation** - Generates realistic 12-20 billing records using LLM
- 📊 **Cost Analysis** - Calculates total costs, per-service breakdown, and budget variance
- 🎯 **Smart Recommendations** - Generates 6-10 multi-cloud optimization recommendations with savings estimates
- 🔄 **Automatic Retry Logic** - Robust JSON validation and retry mechanism for LLM responses
- 💾 **Multiple Output Formats** - JSON reports, HTML dashboards, and text exports
- ☁️ **Multi-Cloud Support** - AWS, Azure, GCP, and open-source recommendations
- 🪟 **Windows-Friendly** - No bash dependencies, pure Python
- Python 3.10+ compatible

## Project Structure

```
cloud_optimizer/
├── cost_optimizer.py           # Main CLI orchestrator (menu-driven interface)
├── profile_extractor.py        # LLM-based project profile extraction
├── billing_generator.py        # LLM-based synthetic billing data generation
├── cost_analyzer.py            # Cost analysis and recommendation engine
├── llm_client.py              # HuggingFace Inference API client
├── utils.py                    # Utility functions (file I/O, formatting, etc.)
├── validators.py               # JSON validation and structure validation
├── requirements.txt            # Python dependencies
├── .env.example               # Example environment configuration
├── README.md                   # This file
└── sample_outputs/            # Sample JSON and report files
    ├── project_description.txt # Sample project description
    ├── project_profile.json    # Extracted project profile example
    ├── mock_billing.json       # Generated billing records example
    └── cost_optimization_report.json  # Final analysis report example
```

## Installation

### Prerequisites

- **Python 3.10+** (check with `python --version`)
- **HuggingFace Account** with API key
- **Windows, macOS, or Linux**

### Step 1: Clone or Navigate to Project

```bash
cd cloud_optimizer
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# On Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# On Windows CMD
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

1. **Copy the example .env file:**
```bash
copy .env
```

2. **Edit `.env` with your HuggingFace API key:**
```env
# Get your API key from https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct

# Optional: Set your budget threshold (in USD)
BUDGET_THRESHOLD=5000
```

### Step 5: Verify Installation

```bash
python cost_optimizer.py --help
```

You should see the menu options displayed.

## How to Use

### Running the Application

```bash
python cost_optimizer.py
```

### Menu Options

```
OPTIONS:
  1. Enter New Project Description
  2. Run Complete Cost Analysis
  3. View Recommendations
  4. Export Report
  5. Exit
```

### Typical Workflow

1. **Start Application:**
   ```bash
   python cost_optimizer.py
   ```

2. **Option 1 - Enter Project Description:**
   - Describe your cloud infrastructure in natural language
   - Include: services, platforms, team size, current monthly costs
   - Example:
     ```
     We run an e-commerce platform with 50,000 daily users.
     Currently using AWS with EC2, RDS, S3, and CloudFront.
     Monthly spend is around $8,500 and we want to optimize.
     ```
   - Type `END` when finished
   - The system will:
     - Save your description to `sample_outputs/project_description.txt`
     - Extract structured profile using LLM → `project_profile.json`
     - Display extracted information

3. **Option 2 - Run Complete Cost Analysis:**
   - Generates synthetic billing records (12-20 items) using LLM
   - Analyzes costs and calculates metrics
   - Generates 6-10 optimization recommendations
   - Saves all data as JSON files
   - Displays cost summary

4. **Option 3 - View Recommendations:**
   - Shows top recommendations from analysis
   - Displays potential savings and implementation effort
   - Lists prioritized actions

5. **Option 4 - Export Report:**
   - Generates HTML dashboard report
   - Creates summary statistics
   - Saves as `cost_optimization_report.html`

6. **Option 5 - Exit:**
   - Closes the application

## Example Usage

### Sample Input

```
PROJECT DESCRIPTION:

We operate a media streaming platform built on microservices.
Currently deployed on AWS with:
- EC2 instances for video encoding (t3.xlarge x 5)
- RDS PostgreSQL with read replicas
- S3 buckets for video storage (500TB)
- CloudFront CDN for global distribution
- ElastiCache for real-time caching
- Lambda for thumbnail generation

Team: 15 engineers
Monthly spend: $6,200
Goals: Reduce costs by 25%, improve performance, evaluate GCP
```

### Sample Output Files

After analysis, you'll get:

**project_profile.json:**
```json
{
  "project_name": "Media Streaming Platform",
  "description": "Microservices-based video streaming with global CDN",
  "cloud_platforms": ["AWS", "considering GCP"],
  "services": ["EC2", "RDS", "S3", "CloudFront", "Lambda", "ElastiCache"],
  "estimated_monthly_cost": 6200,
  "deployment_regions": ["us-east-1", "eu-west-1"],
  "team_size": 15,
  "scaling_requirements": "Variable based on content popularity"
}
```

**mock_billing.json:**
```json
{
  "billing_records": [
    {
      "service": "EC2",
      "cost": 1250.50,
      "date": "2024-12-01",
      "region": "us-east-1",
      "resource_id": "i-0a1b2c3d4e5f67890",
      "usage_type": "On-Demand"
    },
    ...18 more records...
  ]
}
```

**cost_optimization_report.json:**
```json
{
  "analysis_date": "2024-12-12T15:30:00",
  "project_name": "Media Streaming Platform",
  "cost_analysis": {
    "total_monthly_cost": 6200,
    "budget_variance": 1200,
    "is_over_budget": false,
    "high_cost_services": [...]
  },
  "recommendations": [
    {
      "id": 1,
      "title": "Use Spot Instances for Encoding",
      "description": "Switch video encoding to spot instances for 60% cost savings",
      "potential_savings": 750,
      "implementation_effort": "Medium",
      "cloud_platforms": ["AWS"],
      "risks": "Job interruption; requires restart mechanism",
      "implementation_steps": [...]
    },
    ...5-9 more recommendations...
  ],
  "total_potential_savings": 2450
}
```

## Configuration Details

### HuggingFace Setup

1. **Create Account:**
   - Go to https://huggingface.co
   - Sign up (free)

2. **Get API Key:**
   - Navigate to https://huggingface.co/settings/tokens
   - Create new token (read access)
   - Copy the token

3. **Configure `.env`:**
   ```env
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxx
   HUGGINGFACE_MODEL=meta-llama/Llama-2-7b-chat-hf
   BUDGET_THRESHOLD=5000
   ```

### Supported LLM Models

The application supports any HuggingFace hosted model. Recommended:

- **Fast & Efficient:**
  - `mistralai/Mistral-7B-Instruct-v0.1`
  - `tiiuae/falcon-7b-instruct`

- **Most Capable:**
  - `meta-llama/Llama-2-13b-chat-hf` (requires request approval)
  - `meta-llama/Llama-2-70b-chat-hf`

- **Default (balanced):**
  - `meta-llama/Llama-2-7b-chat-hf`

## Architecture

### Component Flow

```
User Input (Project Description)
           ↓
    ProfileExtractor (LLM)
           ↓
    BillingGenerator (LLM)
           ↓
    CostAnalyzer (LLM)
           ↓
    Validators (JSON Schema)
           ↓
    Report Generation & Export
```

### LLM Integration

1. **Prompt Engineering:**
   - Crafted prompts for JSON-only responses
   - Temperature: 0.3-0.7 for deterministic output
   - Automatic retry on invalid JSON

2. **Retry Logic:**
   - Max 3 retries on validation failure
   - Exponential backoff on API errors
   - Graceful degradation

3. **Validation:**
   - Strict JSON schema validation
   - Required field checking
   - Record count verification (12-20 for billing)

## Cost Analysis Details

### Metrics Calculated

1. **Total Monthly Cost** - Sum of all billing records
2. **Cost Per Service** - Breakdown by service type
3. **High-Cost Services** - Top 5 most expensive services
4. **Budget Variance** - Difference from budget threshold
5. **Over Budget Flag** - Boolean indicating if over threshold

### Recommendation Features

Each recommendation includes:

- **Potential Savings** - Estimated monthly savings in USD
- **Implementation Effort** - Low/Medium/High scale
- **Cloud Platforms** - Applicable clouds (AWS/Azure/GCP)
- **Risks** - Considerations and potential issues
- **Implementation Steps** - 3-5 actionable steps
- **ROI Score** - Calculated based on savings/effort ratio
- **Priority** - High/Medium/Low based on ROI

### Recommendation Categories

- Reserved Instances & Commitment Discounts
- Right-Sizing & Optimization
- Auto-Scaling & Load Balancing
- Storage Optimization (S3, etc.)
- Data Transfer Optimization
- Serverless Migration
- Multi-Cloud Strategies
- Managed Service Migration
- License Optimization

## Troubleshooting

### Issue: "HUGGINGFACE_API_KEY not found"

**Solution:**
1. Verify `.env` file exists in project root
2. Check API key is correct in `.env`
3. Ensure no typos or extra spaces
4. Restart the application

### Issue: "Invalid JSON response from LLM"

**Solution:**
- The application will automatically retry (max 3 times)
- If persists:
  1. Check model availability on HuggingFace
  2. Try a different model in `.env`
  3. Reduce prompt complexity

### Issue: "Model loading (503 error)"

**Solution:**
- The model is loading on HuggingFace servers
- Application automatically retries
- Wait 1-2 minutes and try again
- Consider using a smaller model

### Issue: "Request timeout"

**Solution:**
- HuggingFace API might be overloaded
- Wait a few minutes and retry
- Check internet connection
- Try different time of day

### Issue: Application exits unexpectedly

**Solution:**
1. Run with detailed error output
2. Check `.env` configuration
3. Verify internet connectivity
4. Check HuggingFace API status

## Sample Data

The project includes sample outputs demonstrating:

- **project_description.txt** - E-commerce platform description
- **project_profile.json** - Extracted profile with AWS/Azure platforms
- **mock_billing.json** - 18 realistic billing records
- **cost_optimization_report.json** - 10 recommendations with $6,055 potential savings

These demonstrate the system's capabilities and expected output format.

## Output Files Location

All generated files are saved to:
```
cloud_optimizer/sample_outputs/
```

File naming convention:
- `project_description.txt` - Original description
- `project_profile.json` - Extracted profile
- `mock_billing.json` - Generated billing records
- `cost_optimization_report.json` - Analysis and recommendations
- `cost_optimization_report.html` - Dashboard visualization

## Performance

### Typical Execution Times

- Profile Extraction: 5-15 seconds
- Billing Generation: 10-20 seconds
- Cost Analysis: 15-30 seconds
- Total Analysis: 30-60 seconds

Times depend on model size and HuggingFace server load.

## Features Explained

### 1. LLM-Only Profile Extraction

No regex or rule-based parsing. The system uses LLM to:
- Parse natural language project descriptions
- Extract structured JSON with semantic understanding
- Identify cloud platforms and services automatically
- Estimate costs from context

### 2. Synthetic Billing Generation

LLM generates realistic billing records:
- 12-20 records per analysis (validated)
- Realistic service names and costs
- Proper date ranges and region information
- Internally consistent data

### 3. Automatic Retry & Validation

Ensures data quality:
- JSON schema validation
- Required field checking
- Type validation
- Automatic retry on failure (max 3x)
- Graceful fallback

### 4. Multi-Cloud Recommendations

Provides actionable advice for:
- AWS optimization (Reserved Instances, Spot, Right-sizing)
- Azure alternatives
- GCP options
- Open-source solutions
- Hybrid cloud strategies

## System Requirements

| Requirement | Specification |
|-------------|----------------|
| Python | 3.10 or higher |
| OS | Windows, macOS, Linux |
| RAM | 2GB minimum |
| Internet | Required for HuggingFace API |
| Dependencies | Listed in requirements.txt |

## Dependencies

- `python-dotenv>=1.0.0` - Environment configuration
- `requests>=2.31.0` - HTTP client for API calls

## License

This project is open-source and available for educational and commercial use.

## Support & Issues

For issues or questions:
1. Check the Troubleshooting section
2. Review sample outputs for format reference
3. Verify HuggingFace API configuration
4. Check internet connectivity

## Future Enhancements

- Web UI dashboard
- Database persistence
- Real cloud provider API integration
- Advanced forecasting models
- Automated cost monitoring
- Custom recommendation rules
- Team collaboration features

## Contributing

Contributions welcome! Areas for enhancement:
- Additional LLM models
- More cloud platforms
- Enhanced validation
- UI improvements
- Documentation updates

## Conclusion

The AI-Powered Cloud Cost Optimizer provides intelligent, LLM-driven cloud cost analysis and optimization recommendations. It combines natural language understanding with structured data analysis to deliver actionable insights for cloud infrastructure optimization.

**Get started:** Follow the Installation section and run the CLI to analyze your first project!

---

**Version:** 1.0.0  
**Last Updated:** December 2024

