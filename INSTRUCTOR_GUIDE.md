# Instructor Guide

## Course Flow

### Part 1: Web Scraping with Selector Fallback Strategies

#### 1. Introduction (5 min)
- Open `index.html` in browser
- Explain the "No-Code Walkthrough" section
- Show the three HTML versions (v1, v2, v3)

#### 2. Interactive Demo: Selector Fallback (10 min)
- Use the "Interactive Demo: Selector Fallback Strategy" section
- Run the demo for each version:
  - **v1**: Show original selectors working
  - **v2**: Show v1 selectors FAILING, v2 selectors succeeding
  - **v3**: Show only semantic selectors working
- Emphasize: Multiple strategies = resilience!

#### 3. (Optional) Step-by-Step Selector Demo (10 min)
- Click "🎬 Instructor Demo (Step-by-Step)" button
- Walk through each selector being tested
- Show students how the scraper tries selectors in priority order

#### 4. Student Exercise (20 min)
**Students do NOT use the web interface for coding!**

Students should:
1. Open `exercises/exercise_01_scraping.py` in their code editor
2. Complete TODO sections 1-9
3. Run their code: `python exercises/exercise_01_scraping.py`
4. If stuck, reference: `exercises/exercise_01_scraping_OLD.py`

#### 5. Bonus: Playwright (Optional, 10 min)
- After students complete the basic exercise
- Show how to attempt TODO 10-11 (Playwright bonus)
- Reference: `solutions/solution_01_scraping.py`

---

### Part 2: Excel/Reports Automation

#### 1. Instructor Demo (10 min)
Run the demo script and explain each step:
```bash
python src/demos/demo_02_excel_to_reports.py
```

This demonstrates:
- Loading CSV data
- Calculating metrics (MoM, YoY growth)
- Populating Excel templates
- Generating reports

#### 2. Student Exercise 2 (20 min)
Students should:
1. Open `exercises/exercise_02_reports.py`
2. Complete TODO sections 1-7
3. Run their code: `python exercises/exercise_02_reports.py`
4. Check output folder for generated files

#### 3. Student Exercise 3 - Dashboard (20 min, Bonus)
Students should:
1. Open `exercises/exercise_03_dashboard.py`
2. Complete TODO sections 1-6
3. Run their dashboard: `python exercises/exercise_03_dashboard.py`
4. View at: `http://127.0.0.1:8050/`

---

## Common Issues

### "Start Exercise 1" Button Confusion
**Question**: "What does the 'Start Exercise 1' button do?"

**Answer**: It's an **instructor demo tool**, not for student coding!
- Shows step-by-step selector testing
- For demonstration purposes only
- Students code in `exercises/exercise_01_scraping.py`

### Backend Server Not Running
**Symptom**: Web demos fail with "Failed to connect"

**Solution**:
```bash
python src/backend/app.py
```
Server must run on port 8080 for web demos to work.

### Playwright Browsers Not Installed
**Symptom**: Error about missing chromium executable

**Solution**:
```bash
playwright install chromium
```

### Empty Data Files
**Symptom**: Exercise 2/3 fail with "no data found"

**Solution**: Data files should contain:
- `data/sample_monthly_data.csv` - 11 lines (10 indicators)
- `data/historical_trends.csv` - 97 lines (96 data points)

---

## File Purposes

### Web Interface (`index.html`)
- **For**: Instructor demonstrations
- **Purpose**: Show concepts visually before students code
- **NOT for**: Student coding exercises

### Exercise Files (`exercises/*.py`)
- **For**: Students to complete
- **Purpose**: Hands-on coding practice
- **Structure**: TODO sections with hints

### Solution Files (`solutions/*.py`)
- **For**: Reference and answers
- **Purpose**: Show complete working implementations
- **When to show**: After students attempt exercises

### Demo Scripts (`src/demos/*.py`)
- **For**: Instructor to run
- **Purpose**: Live demonstration of concepts
- **When to use**: Before students attempt related exercise

---

## Timing Recommendations

| Activity | Time | Type |
|----------|------|------|
| Part 1 Intro | 5 min | Lecture |
| Selector Fallback Demo | 10 min | Demo |
| Exercise 1 | 20 min | Hands-on |
| **Break** | **10 min** | |
| Excel Demo | 10 min | Demo |
| Exercise 2 | 20 min | Hands-on |
| Exercise 3 (Bonus) | 20 min | Hands-on |
| **Total** | **1hr 35min** | |

---

## Assessment Checklist

Students should be able to:
- ✅ Explain why multiple selector strategies are needed
- ✅ Implement priority-based fallback logic
- ✅ Load data from CSV files
- ✅ Calculate growth metrics (MoM, YoY)
- ✅ Populate Excel templates programmatically
- ✅ Generate Word documents from templates
- ✅ (Bonus) Create interactive dashboards

---

## Support

**Instructor**: Jon Scheele
**Email**: jon@blueconnector.co
**Company**: Blue Connector Pte Ltd
