# Data Wrangling and Automation Training

**A hands-on course for statisticians and data professionals**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](LICENSE)

---

## 🚀 Quick Start

### Starting the Application

#### In GitHub Codespaces
1. Click the "Code" button → "Open with Codespaces"
2. Wait for the environment to set up (installs Python dependencies automatically)
3. Open `index.html` in the browser (right-click → "Open with Live Server" or similar)
4. The web interface will guide you through the exercises
5. **Note:** Exercise 3 runs a local Dash server - follow the in-exercise instructions

#### Locally in VS Code
1. Clone the repository: `git clone <repository-url>`
2. Open in VS Code

Running locally, create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate
```

Remember to deactivate and delete the virtual environment when you are finished:
```bash
deactivate
rm -rf venv
```
3. Install Python dependencies: `pip install -r requirements.txt`
4. Install Playwright browsers (required for web scraping demos):
```bash
playwright install chromium
```
5. Start the backend server

```bash
python src/backend/app.py
```

6. Right-click `index.html` → "Open with Live Server"
7. The web interface will guide you through the exercises
8. **Note:** Exercise 3 runs a local Dash server - follow the in-exercise instructions

### Prerequisites
- Python 3.8 or higher
- VS Code with Live Server extension (for local development)
- Basic Python knowledge
- 2-3 hours for completion
- **Note:** Playwright browsers will be installed during setup (~260 MB download)

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
│   ├── scrapers/          ← Web scraping utilities
│   │   ├── base_scraper.py
│   │   ├── adaptive_scraper.py
│   │   └── selectors.py
│   └── utils/             ← General utilities
│       ├── data_processing.py
│       ├── formatters.py
│       └── validators.py
│
├── exercises/              ← Student exercises (TODO format)
│   ├── exercise_01_scraping.py
│   ├── exercise_02_reports.py
│   └── exercise_03_dashboard.py
│
├── solutions/              ← Complete working solutions
│   ├── solution_01_scraping.py
│   ├── solution_02_reports.py
│   ├── solution_03_dashboard.py
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
Create a web-based dashboard application with interactive charts and filters.
**Note:** This exercise runs a local Dash server at `http://127.0.0.1:8050/`

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

# Install Playwright browsers (required for web scraping demos)
playwright install chromium

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

**Playwright browser not found** (when running Playwright demo)
```bash
# Install Playwright browsers
playwright install chromium
```

**FileNotFoundError**
```bash
# Run from repository root
cd data-wrangling-automation
python exercises/exercise_01_scraping.py
```

**Backend server not running** (for web interface demos)
```bash
# Start the Flask backend
python src/backend/app.py
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