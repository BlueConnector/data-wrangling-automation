# Data Analytics and AI Tools Training Repository
Data Wrangling and Automation Tools for Statisticians

Welcome to the hands-on repository for the Data Analytics Training Session!

## Repository Structure

```
data-wrangling-automation/
├── README.md                          # This file
├── requirements.txt                   # Python dependencies
├── .devcontainer/
│   └── devcontainer.json             # GitHub Codespaces configuration
├── data/
│   ├── sample_monthly_data.csv       # Monthly statistics for Exercise 2
│   ├── historical_trends.csv         # Historical data for visualizations
│   ├── website_sample_v1.html        # Original HTML for Exercise 1
│   ├── website_sample_v2.html        # Modified HTML (changed IDs)
│   ├── website_sample_v3.html        # Redesigned HTML (major changes)
│   └── data_dictionary.md            # Data schema documentation
├── templates/
│   ├── monthly_report_template.xlsx  # Excel template for reports
│   ├── press_release_template.docx   # Word template for press releases
│   └── dashboard_config.json         # Dashboard configuration
├── exercises/
│   ├── exercise1_web_scraping.py     # Exercise 1 starter code
│   ├── exercise2_report_generation.py # Exercise 2 starter code
│   └── helper_functions.py           # Utility functions
├── solutions/
│   ├── exercise1_solution.py         # Complete solution for Exercise 1
│   ├── exercise2_solution.py         # Complete solution for Exercise 2
│   └── solutions_readme.md           # Solution explanations
├── output/
│   └── .gitkeep                      # Placeholder for your outputs
└── demos/
    ├── demo1_resilient_scraper.py    # Instructor demo code
    ├── demo2_report_automation.py    # Instructor demo code
    └── demo_outputs/                 # Example outputs
```

## Quick Start Guide

### Option 1: Using GitHub Codespaces (Recommended)

1. Click the **Code** button above
2. Select **Codespaces** tab
3. Click **Create codespace on main**
4. Wait 1-2 minutes for environment to set up
5. You're ready to go! All dependencies are pre-installed.

### Option 2: Local Setup

If you prefer to work locally:

```bash
# Clone the repository
git clone https://github.com/BlueConnector/data-wrangling-automation.git
cd data-wrangling-automation

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# For Playwright browser (if doing web scraping)
playwright install chromium
```

## Exercises

### Exercise 1: Adaptive Web Scraping (20 minutes)

**File:** `exercises/exercise1_web_scraping.py`

**Objective:** Build a web scraper that adapts to changing HTML layouts

**Tasks:**
1. Implement multiple selector strategies
2. Add data validation
3. Test against three different HTML versions
4. Verify automatic recovery when selectors break

**To run:**
```bash
python exercises/exercise1_web_scraping.py
```

### Exercise 2: Automated Report Generation (20 minutes)

**File:** `exercises/exercise2_report_generation.py`

**Objective:** Automate the creation of reports and press releases

**Tasks:**
1. Load and process monthly statistics data
2. Calculate key metrics (growth rates, trends)
3. Generate insights using rule-based logic
4. Create Excel report with charts
5. Generate Word press release
6. (Bonus) Build interactive dashboard

**To run:**
```bash
python exercises/exercise2_report_generation.py
```

## Data Files

### sample_monthly_data.csv
Contains 10 economic indicators for October 2024 with:
- Current values
- Previous month values (for MoM calculation)
- Previous year values (for YoY calculation)

**Indicators included:**
- GDP, CPI, Unemployment Rate, Retail Sales
- Industrial Production, Housing Starts
- Exports, Imports, Wages, Business Confidence

### historical_trends.csv
Contains 24 months of historical data for:
- GDP
- CPI
- Unemployment
- Retail Sales

Used for creating trend visualizations and dashboards.

### HTML Files (website_sample_v1/v2/v3.html)
Three versions of a mock statistics portal:
- **v1**: Original design with standard IDs and classes
- **v2**: Redesign with changed IDs and classes (tests fallback)
- **v3**: Major redesign with new structure (tests deep resilience)

## Templates

### monthly_report_template.xlsx
Pre-formatted Excel workbook with:
- Summary sheet with indicator table
- Built-in formulas for calculations
- Chart placeholder for trends
- Named ranges for easy scripting

### press_release_template.docx
Word document template with:
- Standard header and formatting
- Placeholder sections for content
- Professional styling

## Helper Functions

The `helper_functions.py` file provides utilities to reduce boilerplate:
- `format_percentage()` - Format decimals as percentages
- `format_currency()` - Add thousand separators
- `determine_trend()` - Classify trend direction
- `load_template()` - Load Excel/Word templates with error handling
- `save_output()` - Save files with error handling

## Output Directory

All generated files will be saved to the `output/` directory:
- `monthly_report_Oct2024.xlsx` - Generated Excel report
- `press_release_Oct2024.docx` - Generated press release
- `dashboard.html` - Interactive dashboard (bonus)

## Getting Help

### During the Training Session
- Raise your hand for instructor assistance
- Check the hints in TODO comments
- Collaborate with your neighbors

### Common Issues

**Issue: "ModuleNotFoundError"**
- Solution: Make sure you ran `pip install -r requirements.txt`

**Issue: "FileNotFoundError"**
- Solution: Make sure you're running scripts from the repository root
- Check: `pwd` (Mac/Linux) or `cd` (Windows) to see current directory

**Issue: Excel file won't open**
- Solution: Ensure openpyxl is installed
- Try: `pip install openpyxl --upgrade`

**Issue: Codespace won't start**
- Solution: Refresh browser, check internet connection
- Alternative: Download repository and work locally

## Tips for Success

1. **Read the TODO comments carefully** - They guide you through each step
2. **Test frequently** - Run your code after each change
3. **Use print statements** - Debug by printing intermediate results
4. **Check the data files** - Open them to understand the structure
5. **Don't aim for perfection** - Focus on understanding concepts

## After the Training

### Continue Learning
- Review the solution files in `solutions/`
- Try modifying the code to work with your own data
- Experiment with the bonus dashboard creation
- Apply these techniques to a real DOS process

### Next Steps
1. Identify a manual process in your work to automate
2. Start with a small pilot project
3. Build on the techniques from today
4. Share your learnings with colleagues

## Additional Resources

**Documentation:**
- BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/
- pandas: https://pandas.pydata.org/
- openpyxl: https://openpyxl.readthedocs.io/
- python-docx: https://python-docx.readthedocs.io/

**Tutorials:**
- Real Python: https://realpython.com/
- DataCamp: https://www.datacamp.com/
- Automate the Boring Stuff: https://automatetheboringstuff.com/

## Contact

**Instructor:** Jon Scheele  
**Email:** jon@blueconnector.co

## License

Training materials © 2026 Blue Connector Pte Ltd  
For educational use only

---

**Questions?** Check the solutions, ask the instructor, or post in the training chat!

Happy coding! 🚀