"""
Exercise 1 Solution: Data-Driven Adaptive Web Scraping
Complete implementation using configuration file instead of hardcoded selectors

This solution demonstrates:
1. Loading selector strategies from CSV configuration
2. Data-driven scraping approach
3. Easy maintenance without code changes
4. Clear documentation through configuration
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
        # Sort selectors by priority (lower number = higher priority)
        sorted_selectors = self.selectors_df.sort_values('priority')
        
        # Try each enabled selector until one succeeds
        for idx, row in sorted_selectors.iterrows():
            # Skip disabled selectors
            if str(row['enabled']).lower() == 'false':
                logging.info(f"⊘ Skipping disabled selector: {row['selector_name']}")
                if 'comment' in row and pd.notna(row['comment']):
                    logging.info(f"  → Reason: {row['comment']}")
                continue
            
            selector_name = row['selector_name']
            selector = row['selector']
            comment = row.get('comment', 'No comment provided')
            
            try:
                # Log the attempt with comment for context
                logging.info(f"Trying {selector_name}...")
                if pd.notna(comment):
                    logging.info(f"  → Context: {comment}")
                
                # Use Playwright to find elements
                rows = self.page.query_selector_all(selector)
                
                # Check if we got results
                if rows and len(rows) > 0:
                    logging.info(f"✓ {selector_name} succeeded! Found {len(rows)} rows")
                    
                    # Extract data from rows
                    self.data = self._parse_rows(rows)
                    
                    # Validate the extracted data
                    if self.validate_extracted_data(self.data):
                        logging.info(f"✓ Data validation passed")
                        return self.data
                    else:
                        logging.warning(f"✗ Data validation failed for {selector_name}")
                        continue
                else:
                    logging.warning(f"✗ {selector_name} found no rows")
                    if pd.notna(comment):
                        logging.info(f"  → Note: {comment}")
                    
            except Exception as e:
                logging.warning(f"✗ {selector_name} failed: {str(e)}")
                if pd.notna(comment):
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
                
                # Skip rows with insufficient cells
                if len(cells) < 4:
                    continue
                
                # Extract text content from each cell
                indicator = {
                    'name': cells[0].text_content().strip(),
                    'value': cells[1].text_content().strip(),
                    'change': cells[2].text_content().strip(),
                    'period': cells[3].text_content().strip(),
                    'code': row.get_attribute('data-indicator-code') or 'UNKNOWN'
                }
                
                # Only add if we got meaningful data
                if indicator['name'] and indicator['value']:
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
        
        # Check 2: Do we have the expected number of rows?
        expected_row_count = 8
        if len(data) < expected_row_count:
            logging.error(f"Validation failed: Expected at least {expected_row_count} rows, got {len(data)}")
            return False
        
        # Check 3: Do all rows have required fields?
        required_fields = ['name', 'value', 'change', 'period']
        for i, item in enumerate(data):
            for field in required_fields:
                if field not in item or not item[field]:
                    logging.error(f"Validation failed: Row {i} missing field '{field}'")
                    return False
        
        # Check 4: Are indicator names non-empty and reasonable length?
        for item in data:
            if len(item['name']) < 3:
                logging.error(f"Validation failed: Invalid indicator name: '{item['name']}'")
                return False
        
        # Check 5: Do we have indicator codes?
        codes_found = sum(1 for item in data if item['code'] != 'UNKNOWN')
        if codes_found > 0:
            logging.info(f"✓ Found {codes_found} indicator codes in data attributes")
        
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
        # Load the CSV file
        selectors_df = pd.read_csv(config_file)
        
        # Validate required columns
        required_columns = ['url', 'selector_name', 'selector', 'priority', 'enabled']
        missing_columns = [col for col in required_columns if col not in selectors_df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        print(f"✓ Loaded {len(selectors_df)} selector configurations from {config_file}")
        
        # Show summary
        unique_urls = selectors_df['url'].nunique()
        print(f"  → Configurations for {unique_urls} different pages")
        
        # Display sample comments to show what's documented
        if 'comment' in selectors_df.columns:
            print(f"\n📝 Sample selector documentation:")
            for idx, row in selectors_df.head(3).iterrows():
                if pd.notna(row.get('comment')):
                    print(f"  • {row['selector_name']}: {row['comment']}")
        
        return selectors_df
    
    except FileNotFoundError:
        print(f"✗ Error: Configuration file not found: {config_file}")
        print("Make sure data/selectors.csv exists in the repository")
        return None
    except Exception as e:
        print(f"✗ Error loading configuration: {str(e)}")
        return None


def test_scraper():
    """
    Test the scraper against all pages configured in the selectors file
    Uses Playwright for browser automation
    """
    # Load selector configuration from CSV
    selectors_config = load_selector_config('data/selectors.csv')
    
    if selectors_config is None:
        print("Cannot proceed without selector configuration")
        return
    
    # Get unique URLs from the configuration
    urls = selectors_config['url'].unique()
    
    print(f"\n✓ Found {len(urls)} unique pages to scrape")
    
    results = []
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        
        for url in urls:
            print(f"\n{'='*80}")
            print(f"Testing: {url}")
            print(f"{'='*80}")
            
            try:
                # Create a new page (tab)
                page = browser.new_page()
                
                # Get selectors for this specific URL
                url_selectors = selectors_config[selectors_config['url'] == url]
                
                print(f"  → Found {len(url_selectors)} configured selectors for this page")
                
                # Navigate to the file (local file path)
                file_path = os.path.abspath(url)
                page.goto(f'file://{file_path}')
                
                # For live URLs, you would use:
                # page.goto(url)
                
                # Wait for the table to be loaded
                page.wait_for_selector('table', timeout=5000)
                
                # Create scraper and extract data
                scraper = ConfigDrivenScraper(page, url_selectors)
                scraper.extract_statistics()
                
                # Display results
                scraper.display_results()
                
                print(f"✓ SUCCESS: Scraper adapted to {url}")
                results.append({'url': url, 'status': 'SUCCESS', 'count': len(scraper.data)})
                
                # Close the page
                page.close()
                
            except FileNotFoundError:
                print(f"✗ ERROR: File not found: {url}")
                print(f"Make sure you're running this from the repository root directory")
                results.append({'url': url, 'status': 'FILE NOT FOUND', 'count': 0})
            except Exception as e:
                print(f"✗ FAILED: {str(e)}")
                results.append({'url': url, 'status': f'FAILED: {str(e)}', 'count': 0})
        
        # Close the browser
        browser.close()
    
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


def demonstrate_config_advantages():
    """
    Demonstrate the advantages of configuration-driven scraping
    """
    print("\n" + "="*80)
    print("ADVANTAGES OF CONFIGURATION-DRIVEN SCRAPING")
    print("="*80)
    
    print("""
1. NON-PROGRAMMERS CAN UPDATE SELECTORS
   • Open data/selectors.csv in Excel or any text editor
   • Add new selectors or modify existing ones
   • Change priorities to test different strategies
   • Enable/disable selectors without touching code

2. CLEAR DOCUMENTATION
   • The CSV file serves as documentation
   • Anyone can see what selectors work for which pages
   • Priority order is explicit and visible
   • Easy to understand what the scraper is trying

3. VERSION CONTROL FRIENDLY
   • Track selector changes over time in Git
   • See when selectors were added or modified
   • Understand why selectors were changed (commit messages)
   • Roll back to previous configurations if needed

4. EASY TESTING AND DEBUGGING
   • Temporarily disable failing selectors
   • Test new selectors by adding them to CSV
   • Compare different selector strategies easily
   • No risk of breaking code syntax

5. SEPARATION OF CONCERNS
   • Business logic (what to scrape) separate from code (how to scrape)
   • Data team can manage selectors
   • Development team maintains core scraping logic
   • Reduces deployment risk

EXAMPLE WORKFLOW:

When a website changes:
1. Data analyst opens selectors.csv
2. Adds new selector for the changed page
3. Sets appropriate priority
4. Runs scraper to test
5. Adjusts priority or adds more selectors as needed
6. Commits changes to Git with description

No code deployment needed!
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    print("="*80)
    print("Exercise 1 Solution: Data-Driven Adaptive Web Scraping")
    print("="*80)
    print("\nThis solution demonstrates configuration-driven scraping.")
    print("Selectors are loaded from data/selectors.csv")
    print("Non-programmers can update selectors by editing the CSV file!\n")
    
    # Run the tests
    test_scraper()
    
    # Show advantages
    demonstrate_config_advantages()
    
    print("\n" + "="*80)
    print("Exercise Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. Configuration files separate data from code logic")
    print("2. Non-technical users can maintain selector strategies")
    print("3. Changes don't require code deployment")
    print("4. Clear documentation through CSV structure")
    print("5. Easy to test and debug different strategies")
    print("\nNext Steps:")
    print("- Open data/selectors.csv and examine the structure")
    print("- Try changing priorities or adding new selectors")
    print("- Test how easy it is to maintain without coding")
    print("- Apply this pattern to your production scrapers")