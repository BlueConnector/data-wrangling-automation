# Data Dictionary

## sample_monthly_data.csv

Monthly statistical indicators for October 2024.

| Column Name | Data Type | Description | Example Values |
|------------|-----------|-------------|----------------|
| indicator_code | String | Unique code identifying the indicator | GDP, CPI, UNEMPLOYMENT |
| indicator_name | String | Full name of the indicator | Gross Domestic Product |
| period | String | Reporting period in YYYY-MM format | 2024-10 |
| value | Float | Current value for the indicator | 542300 |
| unit | String | Unit of measurement | millions, percentage, index |
| previous_month_value | Float | Value from previous month (for MoM calculation) | 538100 |
| previous_year_value | Float | Value from same month last year (for YoY calculation) | 521400 |

### Indicators Included

| Code | Name | Unit | Description |
|------|------|------|-------------|
| GDP | Gross Domestic Product | millions | Total value of goods and services produced |
| CPI | Consumer Price Index | index | Measure of average price changes |
| UNEMPLOYMENT | Unemployment Rate | percentage | Percent of labor force without jobs |
| RETAIL_SALES | Retail Sales | millions | Total retail trade sales |
| INDUSTRIAL_PROD | Industrial Production Index | index | Measure of manufacturing output |
| HOUSING_STARTS | Housing Starts | units | Number of new residential construction projects |
| EXPORTS | Total Exports | millions | Value of goods exported |
| IMPORTS | Total Imports | millions | Value of goods imported |
| WAGES | Average Weekly Wages | dollars | Mean weekly earnings |
| BUSINESS_CONFIDENCE | Business Confidence Index | index | Business sentiment indicator |

### Data Quality Notes

- All values are for October 2024
- Previous month values are for September 2024
- Previous year values are for October 2023
- Missing values should be represented as null/empty
- Negative values are possible for percentage changes
- All monetary values are in local currency

---

## historical_trends.csv

Historical time series data for selected indicators over 24 months.

| Column Name | Data Type | Description | Example Values |
|------------|-----------|-------------|----------------|
| indicator_code | String | Unique code identifying the indicator | GDP, CPI |
| period | String | Month in YYYY-MM format | 2023-10 |
| value | Float | Value for that month | 521400 |

### Time Period

- Start: November 2022
- End: October 2024
- Frequency: Monthly
- Total observations: 24 months per indicator

### Indicators Included

- GDP (Gross Domestic Product)
- CPI (Consumer Price Index)
- UNEMPLOYMENT (Unemployment Rate)
- RETAIL_SALES (Retail Sales)

### Uses

This dataset is designed for:
- Creating trend line charts
- Analyzing seasonal patterns
- Calculating moving averages
- Building interactive dashboards
- Year-over-year comparisons

### Data Quality Notes

- Complete time series with no gaps
- All values use consistent units as defined in sample_monthly_data.csv
- Values are actual (not seasonally adjusted unless specified)
- Suitable for training forecasting models

---

## HTML Files (website_sample_v*.html)

Mock statistics portal pages for web scraping exercises.

### Common Structure

All three versions contain the same data but with different HTML structures:

| Element | Description | Availability |
|---------|-------------|--------------|
| Header | Page title and description | All versions |
| Main content | Statistical indicators table | All versions |
| Table rows | 8 indicator rows | All versions |
| Metadata | Last updated date | All versions |
| Footer | Contact information | All versions |

### Data Attributes

The following data attributes are present in ALL versions (these are the most stable selectors):

- `data-indicator-code`: Unique code (e.g., "GDP", "CPI")
- `data-category`: Category classification
- `data-content`: Identifies statistics tables
- `role`: ARIA role attributes
- `aria-label`: Accessibility labels

### Version Differences

**Version 1 (website_sample_v1.html):**
- Original design
- ID: `statistics-table`
- Classes: `data-table`, `stats-portal`
- Simple structure

**Version 2 (website_sample_v2.html):**
- Redesigned layout
- ID changed to: `stats-data-grid`
- Classes changed to: `stats-grid-view`, `modern-table`
- Modified CSS classes for styling
- Same semantic attributes maintained

**Version 3 (website_sample_v3.html):**
- Major redesign
- No specific IDs on table
- Generic classes only
- Additional nested wrapper divs
- Same data attributes and ARIA labels maintained
- Completely different visual style (dark theme)

### Scraping Strategy

Students should implement selectors in this priority order:
1. Data attributes (most stable)
2. Semantic/ARIA attributes
3. Structural selectors (table > tbody > tr)
4. ID selectors (if available)
5. Class selectors (least stable)

---

## Template Files

### monthly_report_template.xlsx

Excel workbook template for automated report generation.

**Sheets:**

1. **Summary**
   - Cell B2: Report title (to be filled)
   - Cell B3: Reporting period (to be filled)
   - Cells B5:B12: Indicator names (pre-filled)
   - Cells C5:C12: Current values (to be filled)
   - Cells D5:D12: Previous month values (to be filled)
   - Cells E5:E12: Change % (formula: `=(C5-D5)/D5`)
   - Cells B15:B20: Key insights (to be filled)

2. **Trends Chart**
   - Pre-configured line chart
   - Data range: References Summary sheet
   - Chart title: "Monthly Trends"

3. **Historical Data**
   - Column headers for time series
   - Empty cells for data population

**Named Ranges:**
- `ReportTitle`: Cell B2
- `ReportPeriod`: Cell B3
- `IndicatorData`: Cells B5:E12
- `Insights`: Cells B15:B20

### press_release_template.docx

Word document template for press releases.

**Structure:**
- Header: Organization name and "PRESS RELEASE"
- Date placeholder
- Title placeholder
- Summary paragraph placeholder
- "Key Highlights" section
- Bullet point placeholders
- Contact information footer

**Styles Used:**
- Heading 1: Main title
- Heading 2: Section headings
- Normal: Body text
- List Bullet: Key highlights

### dashboard_config.json

Configuration for dashboard layout and charts.

**Schema:**
```json
{
  "title": "Dashboard title",
  "layout": {
    "theme": "plotly_white",
    "rows": 2,
    "columns": 2
  },
  "charts": [
    {
      "id": "unique_id",
      "type": "line|bar|indicator",
      "title": "Chart title",
      "indicators": ["GDP", "CPI"],
      "position": {"row": 1, "col": 1}
    }
  ]
}
```

---

## Output Files (Generated by Students)

### monthly_report_Oct2024.xlsx

Student-generated Excel report with:
- Populated indicator values
- Calculated change percentages
- Generated insights
- Updated charts

### press_release_Oct2024.docx

Student-generated press release with:
- Data-driven summary paragraph
- Rule-based insights as bullet points
- Proper formatting and styling

### dashboard.html (Bonus)

Interactive dashboard (if bonus completed) with:
- Trend line charts
- Comparison bar charts
- Key metric indicators
- Interactive filtering

---

## Usage Notes

1. **File Paths**: All file paths in exercises are relative to repository root
2. **Encoding**: All CSV files use UTF-8 encoding
3. **Decimal Separator**: Period (.) used for decimals
4. **Thousand Separator**: Comma (,) used in display but not in CSV data
5. **Date Format**: YYYY-MM for periods
6. **Missing Data**: Represented as empty cells (not "N/A" or null strings)

## Data Integrity

- All data is synthetic for training purposes
- Values are realistic but not actual government statistics
- Relationships between indicators (MoM, YoY) are mathematically consistent
- HTML versions contain identical data in different structures