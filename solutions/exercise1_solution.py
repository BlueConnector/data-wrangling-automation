"""
Exercise 1 Solution: Adaptive Web Scraping
Complete implementation of a resilient web scraper

This solution demonstrates:
1. Multiple selector strategies with fallback
2. Comprehensive data validation
3. Robust error handling
4. Logging for debugging and monitoring
"""

from bs4 import BeautifulSoup
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class AdaptiveScraper:
    """A web scraper that adapts to changing HTML layouts"""
    
    def __init__(self, html_content):
        """
        Initialize the scraper with HTML content
        
        Args:
            html_content (str): The HTML to parse
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.data = []
        
    def extract_statistics(self):
        """
        Extract statistics using multiple selector strategies with fallback
        
        Returns:
            list: List of dictionaries containing indicator data
        """
        # Define multiple selector strategies in order of preference
        # More specific selectors first, more general ones as fallback
        
        strategies = [
            # Strategy 1: Specific ID selector (works for v1)
            ('ID selector (#statistics-table)', '#statistics-table tbody tr'),
            
            # Strategy 2: Alternative ID selector (works for v2)
            ('Alternative ID (#stats-data-grid)', '#stats-data-grid tbody tr'),
            
            # Strategy 3: Class-based selector (works for v1)
            ('Class selector (.data-table)', 'table.data-table tbody tr'),
            
            # Strategy 4: Alternative class selector (works for v2)
            ('Alternative class (.stats-grid-view)', 'table.stats-grid-view tbody tr'),
            
            # Strategy 5: Data attribute selector (works for all versions - MOST STABLE)
            ('Data attribute selector', 'table[data-content="statistics"] tbody tr'),
            
            # Strategy 6: ARIA role selector (works for all versions)
            ('ARIA role selector', 'table[role="grid"] tbody tr, table[role="table"] tbody tr'),
            
            # Strategy 7: Generic table structure (last resort, works for all)
            ('Generic table structure', 'table tbody tr'),
        ]
        
        # Try each strategy until one succeeds
        for strategy_name, selector in strategies:
            try:
                rows = self.soup.select(selector)
                
                # Check if we got results
                if rows and len(rows) > 0:
                    logging.info(f"✓ {strategy_name} succeeded! Found {len(rows)} rows")
                    
                    # Extract data from rows
                    self.data = self._parse_rows(rows)
                    
                    # Validate the extracted data
                    if self.validate_extracted_data(self.data):
                        logging.info(f"✓ Data validation passed")
                        return self.data
                    else:
                        logging.warning(f"✗ Data validation failed for {strategy_name}")
                        continue
                else:
                    logging.warning(f"✗ {strategy_name} found no rows")
                    
            except Exception as e:
                logging.warning(f"✗ {strategy_name} failed: {str(e)}")
                continue
        
        # If we get here, all strategies failed
        raise Exception("All selector strategies failed to extract data")
    
    def _parse_rows(self, rows):
        """
        Parse table rows into structured data
        
        Args:
            rows: BeautifulSoup result set of table rows
            
        Returns:
            list: List of dictionaries with indicator data
        """
        data = []
        
        for row in rows:
            try:
                # Get all cells in the row
                cells = row.find_all('td')
                
                # Skip rows with insufficient cells
                if len(cells) < 4:
                    continue
                
                # Extract data from cells
                # Most tables have: Indicator Name | Value | Change | Period
                indicator = {
                    'name': cells[0].text.strip(),
                    'value': cells[1].text.strip(),
                    'change': cells[2].text.strip(),
                    'period': cells[3].text.strip(),
                    'code': row.get('data-indicator-code', 'UNKNOWN')
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
        
        # Check 5: Do we have indicator codes? (from data-indicator-code attribute)
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


def test_scraper():
    """Test the scraper against all three HTML versions"""
    
    html_files = [
        ('data/website_sample_v1.html', 'Original HTML'),
        ('data/website_sample_v2.html', 'Modified HTML (changed IDs/classes)'),
        ('data/website_sample_v3.html', 'Major redesign'),
    ]
    
    results = []
    
    for filepath, description in html_files:
        print(f"\n{'='*80}")
        print(f"Testing: {description}")
        print(f"File: {filepath}")
        print(f"{'='*80}")
        
        try:
            # Load the HTML file
            with open(filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Create scraper and extract data
            scraper = AdaptiveScraper(html_content)
            scraper.extract_statistics()
            
            # Display results
            scraper.display_results()
            
            print(f"✓ SUCCESS: Scraper adapted to {description}")
            results.append({'file': description, 'status': 'SUCCESS', 'count': len(scraper.data)})
            
        except FileNotFoundError:
            print(f"✗ ERROR: File not found: {filepath}")
            print(f"Make sure you're running this from the repository root directory")
            results.append({'file': description, 'status': 'FILE NOT FOUND', 'count': 0})
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")
            results.append({'file': description, 'status': f'FAILED: {str(e)}', 'count': 0})
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    for result in results:
        status_symbol = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_symbol} {result['file']}: {result['status']}")
        if result['count'] > 0:
            print(f"  → Extracted {result['count']} indicators")
    print("="*80)


def demonstrate_selector_strategies():
    """
    Demonstrate why different selector strategies work for different versions
    """
    print("\n" + "="*80)
    print("SELECTOR STRATEGY ANALYSIS")
    print("="*80)
    
    print("""
Why Multiple Strategies Work:

1. ID Selectors (#statistics-table, #stats-data-grid)
   - PRO: Fast and specific
   - CON: Break when IDs change (v1 → v2 transition)
   - Works for: v1, v2 (different selectors needed)

2. Class Selectors (.data-table, .stats-grid-view)
   - PRO: Commonly used for styling
   - CON: Frequently changed during redesigns
   - Works for: v1, v2 (different selectors needed)

3. Data Attribute Selectors ([data-content="statistics"])
   - PRO: Semantic meaning, rarely changed
   - CON: Not always present
   - Works for: ALL VERSIONS ✓ (Most stable!)

4. ARIA Selectors ([role="grid"], [role="table"])
   - PRO: Accessibility attributes, stable
   - CON: Not universally used
   - Works for: ALL VERSIONS ✓

5. Structural Selectors (table tbody tr)
   - PRO: Always works if structure is similar
   - CON: Too generic, may catch wrong tables
   - Works for: ALL VERSIONS (but least specific)

KEY INSIGHT: Semantic and accessibility attributes (data-*, role, aria-*)
are the most resilient because they describe WHAT the content is, not
HOW it looks. They survive redesigns better than IDs and classes.
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    print("="*80)
    print("Exercise 1 Solution: Adaptive Web Scraping")
    print("="*80)
    
    # Run the tests
    test_scraper()
    
    # Show strategy analysis
    demonstrate_selector_strategies()
    
    print("\n" + "="*80)
    print("Exercise Complete!")
    print("="*80)
    print("\nKey Takeaways:")
    print("1. Always implement multiple selector fallback strategies")
    print("2. Prioritize semantic attributes (data-*, aria-*) over IDs/classes")
    print("3. Validate data at every step to catch extraction failures early")
    print("4. Log which strategies work to improve future selectors")
    print("5. Plan for failure - websites WILL change")
    print("\nNext Steps:")
    print("- Apply this pattern to your actual data sources")
    print("- Set up monitoring to detect when selectors break")
    print("- Build a library of reusable scraper components")