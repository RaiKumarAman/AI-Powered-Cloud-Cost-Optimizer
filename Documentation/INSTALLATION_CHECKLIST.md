INSTALLATION & VALIDATION CHECKLIST
====================================

Before running the application, verify all components are in place.

STEP 1: FILE STRUCTURE VERIFICATION
===================================

Expected Files (14 total):
□ .env.example                        ✅ Configuration template

□ __init__.py                         ✅ Package initialization

□ billing_generator.py                ✅ Billing generation module

□ cost_analyzer.py                    ✅ Analysis & recommendations

□ cost_optimizer.py                   ✅ Main CLI application

□ llm_client.py                       ✅ HuggingFace API client

□ profile_extractor.py                ✅ Profile extraction module

□ PROJECT_COMPLETION_SUMMARY.md       ✅ Project summary

□ QUICKSTART.md                       ✅ Quick start guide

□ README.md                           ✅ Full documentation

□ requirements.txt                    ✅ Python dependencies

□ utils.py                            ✅ Utility functions

□ validators.py                       ✅ JSON validators

□ sample_outputs/                     ✅ Sample data directory


Sample Output Files (4 expected):
□ sample_outputs/project_description.txt
□ sample_outputs/project_profile.json
□ sample_outputs/mock_billing.json
□ sample_outputs/cost_optimization_report.json

STEP 2: PYTHON VERSION CHECK
=============================

Open PowerShell/CMD and run:
  python --version

Expected output: Python 3.10 or higher

If version < 3.10, download from python.org

STEP 3: VIRTUAL ENVIRONMENT SETUP
=================================

Run these commands in project directory:

Option A - PowerShell:
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  
Option B - Command Prompt:
  python -m venv venv
  venv\Scripts\activate

Verify: Your command prompt should show "(venv)" prefix

STEP 4: INSTALL DEPENDENCIES
============================

With virtual environment activated:
  pip install -r requirements.txt

Expected packages:
  □ python-dotenv>=1.0.0
  □ requests>=2.31.0

Verify installation:
  pip list

Should show both packages listed.

STEP 5: CONFIGURE ENVIRONMENT
=============================

Create .env file with your HuggingFace API key:

1. Get API key:
   a. Visit https://huggingface.co/settings/tokens
   b. Create new token with read access
   c. Copy the token (starts with "hf_")

2. Create .env file:
   Copy .env.example to .env
   
3. Edit .env:
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
   HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
   BUDGET_THRESHOLD=5000

4. Verify:
   - API key is correct (no typos, no spaces)
   - File is named exactly ".env" (no .env.txt)
   - File is in project root directory

STEP 6: TEST CONFIGURATION
==========================

Run quick test:
  python cost_optimizer.py

Expected behavior:
  1. Menu should display
  2. No API key errors
  3. CLI is responsive
  4. Can enter option 1

STEP 7: SAMPLE DATA VERIFICATION
================================

Verify sample outputs exist:
  ls sample_outputs/
  
Expected files:
  □ cost_optimization_report.json (Large JSON file)
  □ mock_billing.json            (~10KB JSON)
  □ project_description.txt      (Text file)
  □ project_profile.json         (Small JSON)

File sizes reference:
  - cost_optimization_report.json: 30-50 KB
  - mock_billing.json: 5-10 KB
  - project_profile.json: 0.5-1 KB
  - project_description.txt: 2-3 KB

STEP 8: FIRST RUN TEST
======================

Execute:
  python cost_optimizer.py

Actions:
1. Menu appears
2. Select option 1
3. Type test project description:
   "Simple web app on AWS with EC2 and RDS, 5 developers, $1000/month"
4. Type END and press Enter
5. Wait for profile extraction (5-15 seconds)

Expected output:
  ✓ Profile extracted
  ✓ Profile displays on screen
  ✓ Files saved to sample_outputs/

Issues to watch for:
  ✗ API key error → Check .env file
  ✗ JSON error → Retry (auto-retries up to 3x)
  ✗ Timeout → Check internet connection
  ✗ Module not found → Check Python path

STEP 9: COMPLETE WORKFLOW TEST
==============================

Continue with option 2:
  Select menu option 2: "Run Complete Cost Analysis"
  
Expected process:
  1. Billing data generation (10-20 seconds)
  2. Cost analysis (15-30 seconds)
  3. Summary displayed
  4. Files saved

Monitor console for:
  ✓ Generating synthetic billing data...
  ✓ Analyzing costs...
  ✓ Cost analysis complete
  ✓ Files saved to sample_outputs/

Files created:
  □ sample_outputs/mock_billing.json (new/updated)
  □ sample_outputs/cost_optimization_report.json (new/updated)

STEP 10: EXPORT REPORT
======================

Select option 4: "Export Report"

Expected output:
  ✓ Report exported to sample_outputs/cost_optimization_report.html

Verify file created:
  ls sample_outputs/

Should see:
  □ cost_optimization_report.html

TROUBLESHOOTING CHECKLIST
=========================

Issue: Module not found (ImportError)
  □ Check virtual environment is activated
  □ Run: pip install -r requirements.txt again
  □ Check Python version (3.10+)

Issue: API key not found error
  □ Verify .env file exists in project root
  □ Check API key is correct (no spaces, valid format)
  □ Ensure file is named ".env" (not ".env.txt")
  □ Restart Python application after .env change

Issue: JSON validation error
  □ Application auto-retries (up to 3 times)
  □ If persists, check internet connection
  □ Try different model in .env file
  □ Verify HuggingFace API is accessible

Issue: Timeout error
  □ Check internet connection
  □ Wait 1-2 minutes (model may be loading)
  □ Retry operation
  □ Check HuggingFace status

Issue: File permission denied
  □ Close any open files in sample_outputs/
  □ Ensure you have write permissions
  □ Check antivirus isn't blocking file access

VERIFICATION RESULTS
====================

All checks passed? ✅ Ready to use!

If any check failed:
  1. Review corresponding troubleshooting section
  2. Fix the issue
  3. Repeat failed check
  4. Contact support if unresolved

NEXT STEPS
==========

1. Review README.md for detailed documentation
2. Read QUICKSTART.md for usage examples
3. Explore sample outputs in sample_outputs/ folder
4. Try analyzing different project types
5. Export reports and review recommendations

QUICK REFERENCE
===============

Common Commands:
  python cost_optimizer.py          - Start application
  pip install -r requirements.txt    - Install dependencies
  pip list                          - Check installed packages
  python --version                  - Check Python version

File Locations:
  Project root: cloud_optimizer/
  Sample data: sample_outputs/
  Config: .env
  Dependencies: requirements.txt

Getting Help:
  - See README.md (comprehensive guide)
  - See QUICKSTART.md (fast reference)
  - Check PROJECT_COMPLETION_SUMMARY.md (overview)
  - Review sample outputs for format reference

Support Resources:
  HuggingFace: https://huggingface.co
  HuggingFace Docs: https://huggingface.co/docs/api-inference
  Python: https://python.org

---

Checklist Date: December 2025
Status: Ready for Production Use
Contact Support: rai.aman1909@gmail.com


