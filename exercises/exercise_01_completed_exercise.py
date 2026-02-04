"""
Exercise 1: Build an Adaptive Web Scraper - COMPLETED EXAMPLE

This is a worked example showing all TODOs completed.
Students can reference this file if they get stuck on any step.

Learning Objectives:
- Implement multiple selector strategies
- Handle HTML structure changes gracefully
- Validate scraped data
- Test against different HTML versions

Original file: exercise_01_scraping.py
"""

# TODO 1 (Basic): Import necessary libraries
# COMPLETED: Import BeautifulSoup for HTML parsing, pandas for CSV handling, json for output
from bs4 import BeautifulSoup
import pandas as pd
import json
import os


class AdaptiveScraper:
    """
    A web scraper that adapts to HTML structure changes using multiple selector strategies.

    The scraper tries selectors in priority order (from selectors.csv) until one succeeds.
    This makes it resilient to website redesigns.
    """

    def __init__(self, url):
        """
        Initialize the scraper.

        Args:
            url (str): The URL (file path) to scrape
        """
        self.url = url
        self.data = None

        # TODO 2 (Basic): Load selectors from CSV and filter for this URL
        # COMPLETED: Load all selectors and filter to only those matching this URL
        all_selectors = self.load_selectors()
        self.url_selectors = all_selectors[all_selectors['url'] == url]
        self.progress = []  # Initialize progress tracking list
        self.soup = None    # Will hold parsed HTML

    def load_selectors(self, csv_file='data/selectors.csv'):
        """
        Load selector configuration from CSV file.

        Args:
            csv_file (str): Path to the selectors CSV file

        Returns:
            DataFrame: The loaded selectors configuration

        TODO 3 (Basic): Implement this method
        COMPLETED: Use pandas to read the CSV and return the DataFrame
        """
        return pd.read_csv(csv_file)

    def fetch(self):
        """
        Fetch HTML content from the URL (local file).

        Returns:
            BeautifulSoup: Parsed HTML content

        TODO 4 (Basic): Implement this method
        COMPLETED: Read local HTML file and parse with BeautifulSoup
        """
        # Since we're working with local files, read the file directly
        # For remote URLs, you would use: response = requests.get(self.url)
        with open(self.url, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Parse the HTML content
        self.soup = BeautifulSoup(html_content, 'html.parser')

        # Log progress
        self.log_progress(f"Fetched HTML content from {self.url}")

        return self.soup

    def parse(self):
        """
        Parse HTML using selectors from CSV in priority order.
        Try each enabled selector until one succeeds.

        Returns:
            list: Extracted data as list of dictionaries

        TODO 5 (Intermediate): Implement this method
        COMPLETED: Sort by priority, try each selector, return data on first success
        """
        # Sort selectors by priority (lower number = higher priority = try first)
        sorted_selectors = self.url_selectors.sort_values('priority')

        # Try each selector in priority order
        for _, row in sorted_selectors.iterrows():
            selector_name = row['selector_name']
            selector = row['selector']

            # Skip disabled selectors
            if str(row['enabled']).lower() == 'false':
                self.log_progress(f"Skipping disabled selector: {selector_name}")
                continue

            self.log_progress(f"Trying selector: {selector_name} ({selector})")

            try:
                # Try to find the table using this selector
                # select_one returns the first match, select returns all matches
                rows = self.soup.select(selector)

                if rows and len(rows) > 0:
                    self.log_progress(f"SUCCESS: {selector_name} found {len(rows)} rows")

                    # Extract data from the found rows
                    self.data = self._extract_table_data(rows)

                    if self.data:
                        self.log_progress(f"Extracted {len(self.data)} indicators")
                        return self.data
                else:
                    self.log_progress(f"FAILED: {selector_name} found no elements")

            except Exception as e:
                self.log_progress(f"ERROR with {selector_name}: {str(e)}")
                continue

        # If we get here, all selectors failed
        self.log_progress("All selectors failed to extract data")
        return []

    def _extract_table_data(self, rows):
        """
        Extract data from table rows.

        Args:
            rows: List of BeautifulSoup row elements

        Returns:
            list: List of dictionaries with extracted data
        """
        data = []

        for row in rows:
            try:
                # Get all cells in the row
                cells = row.find_all('td')

                # Skip rows without enough cells (probably header rows)
                if len(cells) < 3:
                    continue

                # Extract indicator data
                indicator = {
                    'name': cells[0].get_text(strip=True),
                    'value': cells[1].get_text(strip=True),
                    'change': cells[2].get_text(strip=True),
                }

                # Try to get period if available (4th column)
                if len(cells) >= 4:
                    indicator['period'] = cells[3].get_text(strip=True)
                else:
                    indicator['period'] = 'N/A'

                # Try to get indicator code from data attribute
                indicator['code'] = row.get('data-indicator-code', 'UNKNOWN')

                # Only add if we have meaningful data
                if indicator['name'] and indicator['value']:
                    data.append(indicator)

            except Exception as e:
                self.log_progress(f"Error parsing row: {str(e)}")
                continue

        return data

    def validate(self):
        """
        Validate that all required fields are present in scraped data.

        Returns:
            bool: True if validation passes, False otherwise

        TODO 6 (Advanced): Implement this method
        COMPLETED: Check for required fields in all data items
        """
        # Check if we have any data
        if not self.data or len(self.data) == 0:
            self.log_progress("Validation FAILED: No data to validate")
            return False

        # Define required fields
        required_fields = ['name', 'value', 'change', 'period']

        # Check each item has all required fields
        for i, item in enumerate(self.data):
            for field in required_fields:
                if field not in item or not item[field]:
                    self.log_progress(f"Validation FAILED: Item {i} missing field '{field}'")
                    return False

        self.log_progress(f"Validation PASSED: All {len(self.data)} items have required fields")
        return True

    def log_progress(self, message):
        """
        Log progress message for both console and web interface.

        Args:
            message (str): The progress message to log

        TODO 7 (Advanced): Implement this method
        COMPLETED: Append to progress list and print to console
        """
        self.progress.append(message)
        print(message)

    def get_progress_json(self):
        """
        Return progress log as JSON string for web interface.

        Returns:
            str: JSON-formatted progress log
        """
        # This is provided for you - no need to modify
        return json.dumps(self.progress)


# TODO 8 (Basic): Test your scraper against all configured URLs
if __name__ == "__main__":
    """
    Main test script to verify your scraper works against all HTML versions.

    COMPLETED: Full implementation of test script
    """

    print("=" * 60)
    print("TESTING ADAPTIVE SCRAPER")
    print("=" * 60)

    # Load selectors CSV to get unique URLs
    selectors_df = pd.read_csv('data/selectors.csv')
    unique_urls = selectors_df['url'].unique()

    print(f"\nFound {len(unique_urls)} unique URLs to test:")
    for url in unique_urls:
        print(f"  - {url}")
    print()

    # Track results for summary
    results = []

    # Test each URL
    for url in unique_urls:
        print("\n" + "-" * 60)
        print(f"Testing: {url}")
        print("-" * 60)

        try:
            # Create scraper for this URL
            scraper = AdaptiveScraper(url)

            # Fetch HTML content
            scraper.fetch()

            # Parse using fallback selectors
            data = scraper.parse()

            # Validate the extracted data
            is_valid = scraper.validate()

            # Record result
            result = {
                'url': url,
                'success': len(data) > 0,
                'valid': is_valid,
                'count': len(data),
                'data': data,
                'progress': scraper.progress
            }
            results.append(result)

            # Print extracted data
            if data:
                print(f"\nExtracted {len(data)} indicators:")
                for item in data[:3]:  # Show first 3
                    print(f"  - {item['name']}: {item['value']} ({item['change']})")
                if len(data) > 3:
                    print(f"  ... and {len(data) - 3} more")

        except FileNotFoundError:
            print(f"ERROR: File not found: {url}")
            results.append({
                'url': url,
                'success': False,
                'valid': False,
                'count': 0,
                'error': 'File not found'
            })
        except Exception as e:
            print(f"ERROR: {str(e)}")
            results.append({
                'url': url,
                'success': False,
                'valid': False,
                'count': 0,
                'error': str(e)
            })

    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    successful = sum(1 for r in results if r['success'])
    validated = sum(1 for r in results if r.get('valid', False))

    for result in results:
        status = "SUCCESS" if result['success'] else "FAILED"
        valid_status = "VALID" if result.get('valid', False) else "INVALID"
        symbol = "+" if result['success'] else "x"
        print(f"[{symbol}] {result['url']}: {status}, {valid_status}, {result['count']} items")

    print(f"\nTotal: {successful}/{len(results)} succeeded, {validated}/{len(results)} validated")
    print("=" * 60)

    # TODO 9 (Advanced): Save results to JSON for web interface
    # COMPLETED: Create output directory and save results
    os.makedirs('output', exist_ok=True)

    # Prepare results for JSON (remove non-serializable items if needed)
    json_results = []
    for r in results:
        json_result = {
            'url': r['url'],
            'success': r['success'],
            'valid': r.get('valid', False),
            'count': r['count'],
            'data': r.get('data', []),
            'progress': r.get('progress', [])
        }
        if 'error' in r:
            json_result['error'] = r['error']
        json_results.append(json_result)

    with open('output/scraping_results.json', 'w') as f:
        json.dump(json_results, f, indent=2)

    print(f"\nResults saved to: output/scraping_results.json")


# ============================================================================
# BONUS SECTION: Introduction to Playwright
# ============================================================================
# After completing TODOs 1-9, try these bonus exercises to learn Playwright!
# Playwright is a more powerful tool for scraping JavaScript-heavy websites.
#
# Prerequisites:
# 1. Watch the instructor's Playwright demo first (index.html or demo file)
# 2. Install Playwright browsers: playwright install
#
# When to use Playwright vs BeautifulSoup:
# - BeautifulSoup: Fast, simple, works for static HTML
# - Playwright: Handles JavaScript, dynamic content, modern web apps
# ============================================================================

def playwright_bonus_exercise():
    """
    BONUS TODO 10: Create a Playwright version of the scraper

    Convert one of your BeautifulSoup scrapers to use Playwright instead.
    Compare the results and performance.

    Steps:
    1. Import Playwright: from playwright.sync_api import sync_playwright
    2. Launch browser: with sync_playwright() as p: browser = p.chromium.launch()
    3. Create page: page = browser.new_page()
    4. Navigate: page.goto(url)
    5. Get content: html = page.content()
    6. Parse with BeautifulSoup (same as before)

    HINT: See solutions/solution_01_scraping.py for complete example
    HINT: Playwright can also use CSS selectors directly: page.query_selector()
    """
    from playwright.sync_api import sync_playwright
    import time

    print("\n" + "=" * 60)
    print("PLAYWRIGHT BONUS EXERCISE")
    print("=" * 60)

    url = 'data/website_samples/v1.html'

    with sync_playwright() as p:
        # Launch browser (headless for speed)
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Navigate to local file
        file_path = os.path.abspath(url)
        page.goto(f'file://{file_path}')

        # Wait for table to load
        page.wait_for_selector('table')

        # Get HTML content
        html = page.content()

        # Parse with BeautifulSoup (same technique as before!)
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.select('table tbody tr')

        print(f"Playwright found {len(rows)} rows")

        # Clean up
        browser.close()


def compare_scrapers():
    """
    BONUS TODO 11: Compare BeautifulSoup vs Playwright

    Run both scrapers on the same URL and compare:
    - Execution time
    - Data extracted
    - Success rate
    - Complexity of code

    Create a comparison report showing when each approach is better.

    HINT: Use time.time() to measure execution time
    HINT: Print a table comparing both approaches
    """
    import time
    from playwright.sync_api import sync_playwright

    url = 'data/website_samples/v1.html'
    selector = 'table tbody tr'

    print("\n" + "=" * 60)
    print("COMPARISON: BeautifulSoup vs Playwright")
    print("=" * 60)

    # Method 1: BeautifulSoup
    start = time.time()
    with open(url, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    bs_rows = soup.select(selector)
    bs_time = (time.time() - start) * 1000

    # Method 2: Playwright
    start = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(f'file://{os.path.abspath(url)}')
        page.wait_for_selector('table')
        pw_rows = page.query_selector_all(selector)
        browser.close()
    pw_time = (time.time() - start) * 1000

    # Print comparison
    print(f"\n{'Method':<20} {'Time (ms)':<15} {'Rows Found':<15}")
    print("-" * 50)
    print(f"{'BeautifulSoup':<20} {bs_time:<15.2f} {len(bs_rows):<15}")
    print(f"{'Playwright':<20} {pw_time:<15.2f} {len(pw_rows):<15}")
    print("-" * 50)
    print(f"\nPlaywright is {pw_time/bs_time:.1f}x slower but handles JavaScript!")
    print("\nRecommendation:")
    print("  - Use BeautifulSoup for static HTML (like our samples)")
    print("  - Use Playwright for JavaScript-heavy sites")


if __name__ == "__main__" and False:  # Change to True to run bonus exercises
    print("\n" + "=" * 60)
    print("BONUS: PLAYWRIGHT EXERCISES")
    print("=" * 60 + "\n")

    # Uncomment to run bonus exercises after completing TODOs 1-9
    # playwright_bonus_exercise()
    # compare_scrapers()
