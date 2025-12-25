# Installation & Validation Checklist

**AI-Powered Cloud Cost Optimizer**

Before running the application, complete all verification steps below to ensure a correct and stable setup.

---

## ✅ Step 1: File Structure Verification

Ensure the following files and directories exist in the project root.

### Required Files (14 Total)

* `.env` – Configuration template
* `__init__.py` – Package initialization
* `billing_generator.py` – Billing data generator
* `cost_analyzer.py` – Cost analysis & recommendations
* `cost_optimizer.py` – Main CLI application
* `llm_client.py` – HuggingFace API client
* `profile_extractor.py` – Project profile extractor
* `PROJECT_COMPLETION_SUMMARY.md` – Project summary
* `QUICKSTART.md` – Quick start guide
* `README.md` – Full documentation
* `requirements.txt` – Python dependencies
* `utils.py` – Utility functions
* `validators.py` – JSON validation logic
* `sample_outputs/` – Sample data directory

### Sample Output Files (4 Expected)

Inside `sample_outputs/`:

* `project_description.txt`
* `project_profile.json`
* `mock_billing.json`
* `cost_optimization_report.json`

---

## 🐍 Step 2: Python Version Check

Open **PowerShell / Command Prompt** and run:

```bash
python --version
```

**Expected:** Python **3.10 or higher**

If your version is lower, download the latest version from:
👉 [https://www.python.org](https://www.python.org)

---

## 📦 Step 3: Virtual Environment Setup

Run the following commands from the project directory.

### Option A: PowerShell (Windows)

```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Option B: Command Prompt

```bash
python -m venv venv
venv\Scripts\activate
```

✅ **Verification:** Your terminal prompt should show `(venv)`.

---

## 📥 Step 4: Install Dependencies

With the virtual environment activated:

```bash
pip install -r requirements.txt
```

### Expected Packages

* `python-dotenv >= 1.0.0`
* `requests >= 2.31.0`

Verify installation:

```bash
pip list
```

---

## 🔐 Step 5: Environment Configuration

### 1. Obtain HuggingFace API Key

* Visit: [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
* Create a **Read** access token
* Copy the token (starts with `hf_`)

### 2. Create `.env` File

```bash
copy .env
```

### 3. Edit `.env`

```env
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_MODEL=meta-llama/Meta-Llama-3-8B-Instruct
BUDGET_THRESHOLD=5000
```

### 4. Verify Configuration

* No extra spaces in values
* File name is exactly `.env`
* File is in the project root directory

---

## 🧪 Step 6: Test Configuration

Run:

```bash
python cost_optimizer.py
```

### Expected Behavior

* Menu appears
* No API key errors
* CLI is responsive
* Option **1** can be selected

---

## 📁 Step 7: Sample Data Verification

List sample files:

```bash
ls sample_outputs/
```

### Expected Files

* `cost_optimization_report.json`
* `mock_billing.json`
* `project_description.txt`
* `project_profile.json`

### Approximate File Sizes

| File                          | Size     |
| ----------------------------- | -------- |
| cost_optimization_report.json | 30–50 KB |
| mock_billing.json             | 5–10 KB  |
| project_profile.json          | 0.5–1 KB |
| project_description.txt       | 2–3 KB   |

---

## ▶ Step 8: First Run Test

Execute:

```bash
python cost_optimizer.py
```

### Test Actions

1. Select **Option 1**
2. Enter:

   ```
   Simple web app on AWS with EC2 and RDS, 5 developers, $1000/month
   ```
3. Type `END` and press Enter
4. Wait 5–15 seconds

### Expected Output

* ✅ Profile extracted successfully
* ✅ Profile displayed in terminal
* ✅ Files saved in `sample_outputs/`

### Common Issues

* ❌ API key error → Check `.env`
* ❌ JSON error → Auto-retries up to 3 times
* ❌ Timeout → Check internet
* ❌ Module not found → Check virtual environment

---

## 🔄 Step 9: Complete Workflow Test

Select **Option 2: Run Complete Cost Analysis**

### Expected Process

1. Billing generation (10–20 sec)
2. Cost analysis (15–30 sec)
3. Summary displayed
4. Output files saved

### Console Messages

* `Generating synthetic billing data...`
* `Analyzing costs...`
* `Cost analysis complete`
* `Files saved`

### Files Created / Updated

* `sample_outputs/mock_billing.json`
* `sample_outputs/cost_optimization_report.json`

---

## 📤 Step 10: Export Report

Select **Option 4: Export Report**

### Expected Result

* `sample_outputs/cost_optimization_report.html` created successfully

Verify:

```bash
ls sample_outputs/
```

---

## 🛠 Troubleshooting Checklist

### Import Errors

* Activate virtual environment
* Reinstall dependencies
* Confirm Python 3.10+

### API Key Issues

* Verify `.env` exists
* Check key format
* Restart application

### JSON Validation Errors

* Auto-retries enabled
* Check internet
* Try another model

### Timeout Errors

* Wait 1–2 minutes
* Retry operation
* Check HuggingFace service status

### File Permission Errors

* Close open files
* Check write permissions
* Disable antivirus blocking

---

## ✅ Verification Result

✔ All steps completed successfully
🎉 **Application is ready for production use**

If any step fails:

1. Review the related troubleshooting section
2. Fix the issue
3. Repeat the step

---

## 🚀 Next Steps

1. Read `README.md` (full documentation)
2. Review `QUICKSTART.md`
3. Explore sample outputs
4. Test different project types
5. Export and analyze reports

---

## 📌 Quick Reference

### Common Commands

```bash
python cost_optimizer.py
pip install -r requirements.txt
pip list
python --version
```

### Key Locations

* Project root: `cloud_optimizer/`
* Sample outputs: `sample_outputs/`
* Configuration: `.env`
* Dependencies: `requirements.txt`

---

## 📞 Support & Resources

* HuggingFace: [https://huggingface.co](https://huggingface.co)
* HuggingFace API Docs: [https://huggingface.co/docs/api-inference](https://huggingface.co/docs/api-inference)
* Python: [https://python.org](https://python.org)

---

**Checklist Date:** December 2025
**Status:** Ready for Production Use ✅
