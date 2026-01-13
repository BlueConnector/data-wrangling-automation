# Solutions Guide

This document explains the design decisions, alternative approaches, and key learning points from the exercise solutions.

---

## Exercise 1: Adaptive Web Scraping

### Key Design Decisions

**1. Multiple Selector Strategy Priority**

The solution implements 7 different selector strategies in priority order:

```python
strategies = [
    ('ID selector', '#statistics-table tbody tr'),
    ('Alternative ID', '#stats-data-grid tbody tr'),
    ('Class selector', 'table.data-table tbody tr'),
    ('Alternative class', 'table.stats-grid-view tbody tr'),
    ('Data attribute', 'table[data-content="statistics"] tbody tr'),  # Most stable
    ('ARIA role', 'table[role="grid"] tbody tr'),                      # Most stable
    ('Generic structure', 'table tbody tr'),                           # Last resort
]
```

**Why this order?**
- Start with specific selectors that are fast and precise
- Move to semantic selectors that are stable across redesigns
- End with generic selectors as last resort

**2. Comprehensive Data Validation**

The solution validates:
- Data exists (not empty)
- Correct number of rows (at least 8 expected)
- All required fields present
- Field values are reasonable (name length > 3 chars)
- Indicator codes found in data attributes

**Why validate so thoroughly?**
- Catches extraction failures early
- Prevents bad data from propagating
- Provides clear error messages for debugging
- Builds confidence in automated systems

**3. Logging Strategy**

Every selector attempt is logged with:
- Which strategy was tried
- Success or failure
- Number of rows found
- Validation results

**Why comprehensive logging?**
- Helps identify which selectors work best
- Assists in debugging when things break
- Provides data for improving future selectors
- Creates audit trail for production systems

### Alternative Approaches

**Approach 1: Using XPath Instead of CSS Selectors**

```python
# CSS Selector
rows = soup.select('#statistics-table tbody tr')

# XPath Alternative (requires lxml)
from lxml import html
tree = html.fromstring(html_content)
rows = tree.xpath('//table[@id="statistics-table"]//tbody//tr')
```

**Pros:**
- XPath can be more powerful for complex selections
- Can traverse up the DOM tree (parent::, ancestor::)
- Better for complex conditional logic

**Cons:**
- Less familiar to most developers
- Requires additional library (lxml)
- Syntax is more complex

**When to use:** Complex hierarchical selections or when CSS selectors aren't sufficient.

**Approach 2: Using Playwright for Dynamic Content**

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('https://statistics.example.gov')
    page.wait_for_selector('table')
    html = page.content()
    browser.close()
    
# Then parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')
```

**When to use:**
- Website content loaded via JavaScript
- Need to interact with page (clicks, scrolls)
- Anti-scraping measures require realistic browser behavior

**Trade-offs:**
- Slower (browser overhead)
- More resource-intensive
- More robust for modern web apps

**Approach 3: Machine Learning for Selector Generation**

```python
# Conceptual - not implemented in solution
# Train model to identify data tables based on features:
# - Table structure (rows, columns)
# - Text patterns (numbers, dates)
# - Surrounding context (headers, labels)

def ml_based_selector(html):
    features = extract_features(html)
    table_locations = model.predict(features)
    return select_best_table(table_locations)
```

**When to use:**
- Many different website structures to handle
- Selectors break frequently
- Have labeled training data

**Trade-offs:**
- Complex to implement
- Requires training data
- May have false positives
- Overkill for most use cases

### Common Pitfalls and How to Avoid Them

**Pitfall 1: Relying on a Single Selector**

❌ Bad:
```python
rows = soup.select('#statistics-table tbody tr')
if not rows:
    raise Exception("Failed to find data")
```

✅ Good:
```python
for selector in multiple_selectors:
    rows = soup.select(selector)
    if rows:
        break
else:
    raise Exception("All selectors failed")
```

**Pitfall 2: Not Validating Extracted Data**

❌ Bad:
```python
rows = soup.select(selector)
return parse_rows(rows)  # What if rows is empty or malformed?
```

✅ Good:
```python
rows = soup.select(selector)
data = parse_rows(rows)
if validate_data(data):
    return data
else:
    try_next_strategy()
```

**Pitfall 3: Catching Too Broad Exceptions**

❌ Bad:
```python
try:
    data = scrape_website()
except:  # Catches everything, including KeyboardInterrupt!
    pass
```

✅ Good:
```python
try:
    data = scrape_website()
except (AttributeError, ValueError) as e:
    logging.error(f"Scraping failed: {e}")
    raise
```

### Production Considerations

**1. Monitoring and Alerting**

```python
import sentry_sdk  # or similar monitoring tool

def scrape_with_monitoring():
    try:
        data = scraper.extract_statistics()
        
        # Log success metrics
        metrics.gauge('scraper.rows_extracted', len(data))
        metrics.gauge('scraper.success', 1)
        
    except Exception as e:
        # Alert on failure
        sentry_sdk.capture_exception(e)
        metrics.gauge('scraper.success', 0)
        send_alert(f"Scraper failed: {e}")
        raise
```

**2. Rate Limiting and Politeness**

```python
import time

def scrape_multiple_pages(urls):
    for url in urls:
        data = scrape_page(url)
        process_data(data)
        
        # Be polite - don't hammer the server
        time.sleep(1)  # Wait 1 second between requests
```

**3. Caching and Incremental Updates**

```python
def scrape_with_cache(url, cache_ttl=3600):
    cache_key = f"scrape:{url}"
    cached = redis.get(cache_key)
    
    if cached:
        return json.loads(cached)
    
    data = scrape_page(url)
    redis.setex(cache_key, cache_ttl, json.dumps(data))
    return data
```

---

## Exercise 2: Automated Report Generation

### Key Design Decisions

**1. Metric Calculation Logic**

The solution calculates two key growth metrics:

```python
# Month-over-month
mom_growth = ((current - previous_month) / previous_month) * 100

# Year-over-year
yoy_growth = ((current - previous_year) / previous_year) * 100
```

**Why both?**
- MoM shows recent trends and momentum
- YoY removes seasonal effects
- Together they provide complete picture

**2. Rule-Based Insight Generation**

```python
if mom_growth > 5:
    insight = f"{name} showed significant growth..."
elif mom_growth < -3:
    insight = f"{name} decreased by {abs(mom_growth)}%..."
```

**Why rule-based?**
- Transparent and explainable
- Easy to maintain and update
- No external dependencies
- Deterministic (same data = same insights)

**Alternative:** AI-powered insights (covered in future sessions)

**3. Template-Based Document Generation**

The solution uses:
- Existing Excel template with formulas
- Programmatic population of cells
- Preservation of formatting and charts

**Why templates?**
- Non-technical staff can update layouts
- Consistent formatting across reports
- Formulas in Excel automatically recalculate
- Easier to maintain than generating from scratch

**4. Error Handling Strategy**

```python
try:
    workbook = openpyxl.load_workbook(template_path)
except FileNotFoundError:
    # Fallback: create basic report without template
    create_basic_excel_report(metrics, output_path)
```

**Why fallback approach?**
- System degrades gracefully
- Partial success better than complete failure
- Users still get useful output

### Alternative Approaches

**Approach 1: Database-Driven Reports**

```python
# Store metrics in database
def save_to_database(metrics):
    for code, data in metrics.items():
        db.execute("""
            INSERT INTO monthly_metrics 
            (indicator_code, period, value, mom_growth, yoy_growth)
            VALUES (?, ?, ?, ?, ?)
        """, (code, data['period'], data['current_value'], 
              data['mom_growth'], data['yoy_growth']))
    db.commit()

# Generate reports from database
def generate_report_from_db(period):
    metrics = db.execute("""
        SELECT * FROM monthly_metrics 
        WHERE period = ?
    """, (period,)).fetchall()
    
    return create_report(metrics)
```

**Pros:**
- Historical data readily available
- Easy to generate custom date ranges
- Can power multiple reports
- Enables ad-hoc queries

**Cons:**
- Additional infrastructure
- More complex to set up
- Requires database maintenance

**When to use:** Multiple report consumers, need historical analysis, scaling to many indicators

**Approach 2: Template Engines (Jinja2)**

```python
from jinja2 import Template

template = Template("""
In {{ period }}, {{ indicator }} {{ direction }} by {{ change }}%, 
compared to the previous period.
""")

narrative = template.render(
    period="October 2024",
    indicator="GDP",
    direction="increased",
    change="0.78"
)
```

**Pros:**
- More flexible than string formatting
- Templates separate from logic
- Supports complex conditionals and loops
- Templates can be in separate files

**Cons:**
- Additional dependency
- Learning curve for template syntax

**When to use:** Complex narratives, non-technical template editing, multiple similar reports

**Approach 3: Business Intelligence Tools Integration**

```python
# Export to format compatible with Tableau, Power BI, etc.
def export_for_bi_tool(metrics, output_path):
    # Create data in format BI tools expect
    rows = []
    for code, data in metrics.items():
        rows.append({
            'Indicator': data['name'],
            'Period': data['period'],
            'Value': data['current_value'],
            'MoM_Change': data['mom_growth'],
            'YoY_Change': data['yoy_growth']
        })
    
    df = pd.DataFrame(rows)
    df.to_csv(output_path, index=False)
```

**Pros:**
- Leverage powerful visualization tools
- Interactive dashboards
- Non-technical users can create reports

**Cons:**
- Requires BI tool licenses
- Users need training
- Less control over exact output

**When to use:** Organization already uses BI tools, need interactive exploration, many stakeholders

### Common Pitfalls and How to Avoid Them

**Pitfall 1: Division by Zero**

❌ Bad:
```python
growth = (current - previous) / previous  # What if previous is 0?
```

✅ Good:
```python
if previous and previous != 0:
    growth = (current - previous) / previous
else:
    growth = None
```

**Pitfall 2: Not Handling Missing Data**

❌ Bad:
```python
mom_growth = ((row['value'] - row['previous_month']) / 
              row['previous_month']) * 100
# What if previous_month is NaN or missing?
```

✅ Good:
```python
if pd.notna(row['previous_month']) and row['previous_month'] != 0:
    mom_growth = ((row['value'] - row['previous_month']) / 
                  row['previous_month']) * 100
else:
    mom_growth = None
```

**Pitfall 3: Hardcoding File Paths**

❌ Bad:
```python
data = pd.read_csv('C:\\Users\\John\\Documents\\data.csv')
```

✅ Good:
```python
import os
data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
data_file = os.path.join(data_dir, 'sample_monthly_data.csv')
data = pd.read_csv(data_file)
```

**Pitfall 4: Not Testing with Edge Cases**

Always test with:
- Missing values (NaN, None, empty strings)
- Zero values
- Negative values
- Very large or small numbers
- Unexpected data types

### Production Considerations

**1. Scheduling Automation**

```python
# Using cron (Linux/Mac)
# Run on 1st of month at 9 AM
# 0 9 1 * * /path/to/venv/bin/python /path/to/report_generation.py

# Using Windows Task Scheduler
# Or using Apache Airflow for complex workflows:

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

dag = DAG(
    'monthly_report',
    start_date=datetime(2024, 1, 1),
    schedule_interval='0 9 1 * *'  # 9 AM on 1st of month
)

generate_report_task = PythonOperator(
    task_id='generate_report',
    python_callable=main,
    dag=dag
)
```

**2. Email Distribution**

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def email_report(report_path, recipients):
    msg = MIMEMultipart()
    msg['Subject'] = 'Monthly Statistics Report - October 2024'
    msg['From'] = 'statistics@gov.example'
    msg['To'] = ', '.join(recipients)
    
    # Attach file
    with open(report_path, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', 
                            f'attachment; filename={os.path.basename(report_path)}')
        msg.attach(attachment)
    
    # Send
    with smtplib.SMTP('smtp.gov.example') as server:
        server.send_message(msg)
```

**3. Version Control for Outputs**

```python
import shutil
from datetime import datetime

def archive_report(report_path):
    # Create archive with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_dir = 'archive/reports'
    os.makedirs(archive_dir, exist_ok=True)
    
    filename = os.path.basename(report_path)
    archive_path = os.path.join(archive_dir, f'{timestamp}_{filename}')
    
    shutil.copy2(report_path, archive_path)
    print(f"Archived to: {archive_path}")
```

**4. Data Quality Checks**

```python
def validate_metrics(metrics):
    """Run data quality checks before generating reports"""
    issues = []
    
    # Check for anomalies
    for code, data in metrics.items():
        # Flag unusual changes
        if data['mom_growth'] and abs(data['mom_growth']) > 50:
            issues.append(f"{code}: Unusually large change ({data['mom_growth']:.1f}%)")
        
        # Check for missing data
        if data['current_value'] is None:
            issues.append(f"{code}: Missing current value")
    
    if issues:
        logging.warning("Data quality issues detected:")
        for issue in issues:
            logging.warning(f"  - {issue}")
        
        # Optionally halt or require manual approval
        if input("Continue anyway? (y/n): ").lower() != 'y':
            raise Exception("Report generation cancelled due to data quality issues")
```

---

## Extension Ideas

### For Exercise 1 (Web Scraping)

1. **Add retry logic with exponential backoff**
2. **Implement proxy rotation** for large-scale scraping
3. **Add screenshot capture** when selectors fail (for debugging)
4. **Create a selector testing framework** that runs against archived HTML
5. **Build a selector library** for commonly scraped sites

### For Exercise 2 (Report Generation)

1. **Add trend analysis** (moving averages, seasonality)
2. **Implement forecasting** (simple linear regression)
3. **Create comparison reports** (compare multiple months)
4. **Add data visualization improvements** (more chart types)
5. **Build an email distribution system** with scheduled sending
6. **Create a web interface** for report parameters
7. **Implement A/B testing** for different insight generation rules

---

## Learning Resources

**Web Scraping:**
- "Web Scraping with Python" by Ryan Mitchell
- Real Python web scraping tutorials
- ScrapingHub blog

**Data Processing:**
- "Python for Data Analysis" by Wes McKinney
- pandas documentation
- DataCamp courses

**Automation:**
- "Automate the Boring Stuff with Python" by Al Sweigart
- Apache Airflow documentation
- Prefect tutorials

**Best Practices:**
- "The Pragmatic Programmer"
- "Clean Code" by Robert C. Martin
- Python PEP 8 Style Guide

---

## Getting Help

If you're stuck or want to discuss design decisions:
1. Review this solutions README
2. Check the inline comments in solution files
3. Ask in the training Slack channel
4. Email the instructor
5. Pair program with a colleague

Remember: There's rarely one "correct" solution. The best approach depends on your specific requirements, constraints, and context.