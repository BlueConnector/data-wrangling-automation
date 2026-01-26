# Data Wrangling and Automation Training

**A hands-on course for statisticians and data professionals**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)

---

## 🚀 Quick Start

**Get started in 2 minutes:**

1. Open [`index.html`](index.html) in your browser for the full interactive experience
2. Or jump straight to the exercises in the `exercises/` directory

### Prerequisites
- Python 3.8 or higher
- Basic Python knowledge
- 2-3 hours for completion

---

## 📚 What You'll Learn

This hands-on course teaches you to:

- ✅ Build **resilient web scrapers** that adapt to HTML changes
- ✅ **Automate report generation** with Excel and Word
- ✅ Create **interactive dashboards** for data visualization
- ✅ Apply **production-ready** coding patterns

---

## 🏗️ Repository Structure

data-wrangling-automation/
├── index.html              ← START HERE - Interactive learning interface
├── README.md               ← You are here
├── requirements.txt        ← Python dependencies
│
├── assets/                 ← Web interface assets
│   ├── css/               ← Stylesheets
│   │   ├── main.css
│   │   ├── components.css
│   │   └── exercises.css
│   └── js/                ← JavaScript
│       ├── app.js
│       ├── exercise-runner.js
│       └── progress-tracker.js
│
├── src/                    ← Core Python modules
│   ├── scrapers/          ← Web scraping
│   │   ├── base_scraper.py
│   │   ├── adaptive_scraper.py
│   │   └── selectors.py
│   ├── generators/        ← Report generation
│   │   ├── report_generator.py
│   │   ├── press_release.py
│   │   └── dashboard.py
│   └── utils/             ← Utilities
│       ├── data_processing.py
│       ├── formatters.py
│       └── validators.py
│
├── exercises/              ← Student exercises
│   ├── exercise_01_scraping.py
│   ├── exercise_02_reports.py
│   └── exercise_03_dashboard.py
│
├── solutions/              ← Complete solutions
│   ├── solution_01_scraping.py
│   ├── solution_02_reports.py
│   └── SOLUTIONS.md
│
├── data/                   ← Sample datasets
│   ├── sample_monthly_data.csv
│   ├── historical_trends.csv
│   ├── website_samples/
│   │   ├── v1.html
│   │   ├── v2.html
│   │   └── v3.html
│   └── data_dictionary.md
│
├── templates/              ← Output templates
│   ├── monthly_report_template.xlsx
│   └── press_release_template.docx
│
└── output/                 ← Your generated files
└── .gitkeep

---

## 🎯 Exercises

### Exercise 1: Adaptive Web Scraping (20 min)
Build a scraper that handles HTML structure changes using multiple selector strategies.

**File:** `exercises/exercise_01_scraping.py`

### Exercise 2: Automated Report Generation (20 min)
Transform CSV data into professional Excel reports and Word documents.

**File:** `exercises/exercise_02_reports.py`

### Exercise 3: Interactive Dashboards (30 min - Bonus)
Create an HTML dashboard with charts and filters.

**File:** `exercises/exercise_03_dashboard.py`

---

## ⚙️ Setup

### Option 1: GitHub Codespaces (Recommended)

1. Click the **Code** button above
2. Select **Codespaces** tab
3. Click **Create codespace on main**
4. Wait for environment setup
5. Open `index.html` in browser preview

### Option 2: Local Setup
```bash
# Clone repository
git clone https://github.com/BlueConnector/data-wrangling-automation.git
cd data-wrangling-automation

# Create virtual environment
python -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate
# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import pandas, bs4, openpyxl, docx; print('✓ Ready!')"
```

---

## 📊 Data Files

### sample_monthly_data.csv
10 economic indicators (GDP, CPI, Unemployment, etc.) with current, previous month, and previous year values.

### historical_trends.csv
24 months of historical data for trend analysis and visualization.

### website_samples/
Three HTML versions for testing scraper resilience:
- `v1.html` - Original (ID selectors)
- `v2.html` - Modified IDs (class selectors)
- `v3.html` - Redesigned (structural selectors)

---

## 🛠️ Development

### Running Tests
```bash
pytest tests/
```

### Code Style
```bash
flake8 src/ exercises/ solutions/
black src/ exercises/ solutions/
```

---

## ❓ Troubleshooting

**ModuleNotFoundError**
```bash
pip install -r requirements.txt
```

**FileNotFoundError**
```bash
# Run from repository root
cd data-wrangling-automation
python exercises/exercise_01_scraping.py
```

**More help:** Check `index.html` → Resources → Troubleshooting

---

## 📚 Resources

- [pandas Documentation](https://pandas.pydata.org/docs/)
- [BeautifulSoup Guide](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [openpyxl Tutorial](https://openpyxl.readthedocs.io/)
- [python-docx Docs](https://python-docx.readthedocs.io/)

---

## 📧 Contact

**Instructor:** Jon Scheele  
**Email:** jon@blueconnector.co  
**Company:** Blue Connector Pte Ltd

---

## 📄 License

Training materials © 2026 Blue Connector Pte Ltd  
For educational use only

---

**Ready to start?** Open `index.html` in your browser! 🎓