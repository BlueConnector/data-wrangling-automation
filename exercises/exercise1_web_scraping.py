"""
Exercise 1: Data-Driven Adaptive Web Scraping with Playwright
Build a resilient web scraper using configuration files instead of hardcoded selectors

Your Task:
1. Load selector strategies from a CSV configuration file
2. Implement Playwright-based scraping that tries selectors in priority order
3. Add validation logic
4. Test against multiple HTML pages automatically

Key Advantage: Non-programmers can update selectors by editing the CSV file,
no code changes required!
"""

from playwright.sync_api import sync_playwright
import pandas as pd
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class ConfigDrivenScraper:
    """A web scraper that reads selector strategies from a configuration file"""
    
    def __init__(self, page, selectors_df):
        """
        Initialize the scraper with a Playwright page and selector configuration
        
        Args:
            page: Playwright page object (browser page)
            selectors_df: DataFrame containing selector configurations for this URL
        """
        self.page = page
        self.selectors_df = selectors_df
        self.data = []
        
    def extract_statistics(self):
        """
        Extract statistics using selectors from configuration file
        Tries selectors in priority order until one succeeds
        
        Returns:
            list: List of dictionaries containing indicator data
        """
        # TODO: Sort selectors by priority (lower number = higher priority)
        # Hint: sorted_selectors = self.selectors_df.sort_values('priority')
        sorted_selectors = None  # Replace with sorting logic
        
        # TODO: Try each enabled selector until one succeeds
        for idx, row in sorted_selectors.iterrows():
            # TODO: Skip disabled selectors
            # Hint: if row['enabled'] == 'false': continue
            
            selector_name = row['selector_name']
            selector = row['selector']
            comment = row.get('comment', 'No comment provided')
            
            try:
                # TODO: Log the attempt with comment for context
                # Hint: logging.info(f"Trying {selector_name}: {comment}")
                
                # TODO: Use Playwright to find elements
                # Hint: rows = self.page.query_selector_all(selector)
                rows = None  # Replace with actual query
                
                # TODO: Check if we got results
                if rows and len(rows) > 0:
                    logging.info(f"✓ {selector_name} succeeded! Found {len(rows)} rows")
                    logging.info(f"  → {comment}")
                    
                    # TODO: Extract data from rows
                    self.data = self._parse_rows(rows)
                    
                    # TODO: Validate the extracted data
                    if self.validate_extracted_data(self.data):
                        logging.info(f"✓ Data validation passed")
                        return self.data
                    else:
                        logging.warning(f"✗ Data validation failed for {selector_name}")
                        continue
                else:
                    logging.warning(f"✗ {selector_name} found no rows")
                    logging.info(f"  → Context: {comment}")
                    
            except Exception as e:
                logging.warning(f"✗ {selector_name} failed: {str(e)}")
                logging.info(f"  → Context: {comment}")
                continue
        
        # If we get here, all strategies failed
        raise Exception("All selector strategies failed to extract data")
    
    def _parse_rows(self, rows):
        """
        Parse table rows into structured data using Playwright
        
        Args:
            rows: List of Playwright ElementHandle objects
            
        Returns:
            list: List of dictionaries with indicator data
        """
        data = []
        
        for row in rows:
            try:
                # Get all cells in the row using Playwright
                cells = row.query_selector_all('td')
                
                if len(cells) >= 4:
                    # TODO: Extract text from each cell
                    # Hint: cells[0].text_content().strip()
                    indicator = {
                        'name': None,  # TODO: Get text from first cell
                        'value': None,  # TODO: Get text from second cell
                        'change': None,  # TODO: Get text from third cell
                        'period': None,  # TODO: Get text from fourth cell
                        'code': row.get_attribute('data-indicator-code') or 'UNKNOWN'
                    }
                    data.append(indicator)
                    
            except Exception as e:
                logging.warning(f"Error parsing row: {str(e)}")
                continue
        
        return data
    
    def validate_extracted_data(self, data):
        """
        Validate that the extracted data meets quality standards
        
        Args:
            data (list): The extracted data to validate
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        # Check 1: Do we have data?
        if not data or len(data) == 0:
            logging.error("Validation failed: No data extracted")
            return False
        
        # TODO: Check 2: Do we have the expected number of rows? (should be 8)
        expected_row_count = 8
        if len(data) < expected_row_count:
            logging.error(f"Validation failed: Expected at least {expected_row_count} rows, got {len(data)}")
            return False
        
        # TODO: Check 3: Do all rows have required fields?
        required_fields = ['name', 'value', 'change', 'period']
        for i, item in enumerate(data):
            for field in required_fields:
                if field not in item or not item[field]:
                    logging.error(f"Validation failed: Row {i} missing field '{field}'")
                    return False
        
        # TODO: Check 4: Are indicator names non-empty?
        for item in data:
            if len(item['name']) < 3:
                logging.error(f"Validation failed: Invalid indicator name: '{item['name']}'")
                return False
        
        return True
    
    def display_results(self):
        """Display the extracted data in a readable format"""
        if not self.data:
            print("No data to display")
            return
        
        print(f"\n{'='*80}")
        print(f"Extracted {len(self.data)} indicators:")
        print(f"{'='*80}")
        
        for item in self.data:
            print(f"\nIndicator: {item['name']}")
            print(f"  Code: {item['code']}")
            print(f"  Value: {item['value']}")
            print(f"  Change: {item['change']}")
            print(f"  Period: {item['period']}")
        
        print(f"\n{'='*80}\n")


def load_selector_config(config_file='data/selectors.csv'):
    """
    Load selector configuration from CSV file
    
    Args:
        config_file (str): Path to the selectors CSV file
        
    Returns:
        DataFrame: Selector configuration
    """
    try:
        # TODO: Load the CSV file using pandas
        # Hint: selectors_df = pd.read_csv(config_file)
        selectors_df = None  # Replace with actual file loading
        
        print(f"✓ Loaded {len(selectors_df)} selector configurations from {config_file}")
        
        # TODO: Display sample comments to show analysts what's documented
        # Hint: print("\nSample selector comments:")
        # Hint: for idx, row in selectors_df.head(3).iterrows():
        #           print(f"  • {row['selector_name']}: {row['comment']}")
        
        return selectors_df
    
    except FileNotFoundError:
        print(f"✗ Error: Configuration file not found: {config_file}")
        print("Make sure data/selectors.csv exists in the repository")
        return None


def test_scraper():
    """
    Test the scraper against all pages configured in the selectors file
    Uses Playwright for browser automation
    """
    # TODO: Load selector configuration from CSV
    # Hint: selectors_config = load_selector_config('data/selectors.csv')
    selectors_config = None  # Replace with actual loading
    
    if selectors_config is None:
        print("Cannot proceed without selector configuration")
        return
    
    # TODO: Get unique URLs from the configuration
    # Hint: urls = selectors_config['url'].unique()
    urls = []  # Replace with actual unique URLs
    
    results = []
    
    with sync_playwright() as p:
        # TODO: Launch browser
        # Hint: browser = p.chromium.launch(headless=True)
        browser = None  # Replace with actual browser launch
        
        for url in urls:
            print(f"\n{'='*80}")
            print(f"Testing: {url}")
            print(f"{'='*80}")
            
            try:
                # TODO: Create a new page
                # Hint: page = browser.new_page()
                page = None  # Replace with actual page creation
                
                # TODO: Get selectors for this specific URL
                # Hint: url_selectors = selectors_config[selectors_config['url'] == url]
                url_selectors = None  # Replace with filtering logic
                
                # TODO: Navigate to the file
                # For local files: page.goto(f'file://{os.path.abspath(url)}')
                # For live URLs: page.goto(url)
                
                # TODO: Wait for content to load
                # Hint: page.wait_for_selector('table', timeout=5000)
                
                # Create scraper and extract data
                scraper = ConfigDrivenScraper(page, url_selectors)
                scraper.extract_statistics()
                
                # Display results
                scraper.display_results()
                
                print(f"✓ SUCCESS: Scraper adapted to {url}")
                results.append({'url': url, 'status': 'SUCCESS', 'count': len(scraper.data)})
                
                # TODO: Close the page
                # Hint: page.close()
                
            except FileNotFoundError:
                print(f"✗ ERROR: File not found: {url}")
                print(f"Make sure you're running this from the repository root directory")
                results.append({'url': url, 'status': 'FILE NOT FOUND', 'count': 0})
            except Exception as e:
                print(f"✗ FAILED: {str(e)}")
                results.append({'url': url, 'status': f'FAILED: {str(e)}', 'count': 0})
        
        # TODO: Close the browser
        # Hint: browser.close()
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    for result in results:
        status_symbol = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_symbol} {result['url']}: {result['status']}")
        if result['count'] > 0:
            print(f"  → Extracted {result['count']} indicators")
    print("="*80)


if __name__ == "__main__":
    print("="*80)
    print("Exercise 1: Data-Driven Adaptive Web Scraping")
    print("="*80)
    print("\nThis exercise demonstrates configuration-driven scraping.")
    print("Selectors are loaded from data/selectors.csv")
    print("Non-programmers can update selectors by editing the CSV file!\n")
    
    # TODO: Complete the implementation above, then run the test
    test_scraper()
    
    print("\n" + "="*80)
    print("Exercise Complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Open data/selectors.csv and examine the configuration")
    print("2. Try changing selector priorities or adding new selectors")
    print("3. Test how the scraper adapts without code changes")
    print("\nKey advantages of configuration-driven scraping:")
    print("  • Non-programmers can update selectors")
    print("  • Easy to enable/disable strategies for testing")
    print("  • Clear documentation of what selectors work for which sites")
    print("  • Version control friendly - track selector changes over time")