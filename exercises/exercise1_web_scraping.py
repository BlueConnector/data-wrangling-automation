"""
Exercise 1: Adaptive Web Scraping
Build a resilient web scraper that can handle changing website layouts

Your Task:
1. Implement multiple selector strategies
2. Add validation logic
3. Test against three HTML versions
4. Verify automatic recovery when selectors break
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
        # TODO: Initialize BeautifulSoup with the HTML content
        self.soup = None  # Replace with: BeautifulSoup(html_content, 'html.parser')
        self.data = []
        
    def extract_statistics(self):
        """
        Extract statistics using multiple selector strategies with fallback
        
        Returns:
            list: List of dictionaries containing indicator data
        """
        # TODO: Implement multiple selector strategies
        # Try each strategy in order until one succeeds
        
        # Strategy 1: Try by specific ID
        # Hint: set selector to: '#statistics-table tbody tr'
        strategy_1_selector = None  # TODO: Add your selector
        
        # Strategy 2: Try by class name
        # Hint: set selector to: 'table.data-table tbody tr'
        strategy_2_selector = None  # TODO: Add your selector
        
        # Strategy 3: Try by data attribute
        # Hint: set selector to: 'table[data-content="statistics"] tbody tr'
        strategy_3_selector = None  # TODO: Add your selector
        
        # Strategy 4: Try by table structure (any table with tbody)
        # Hint: set selector to: 'table tbody tr'
        strategy_4_selector = None  # TODO: Add your selector
        
        # Create a list of strategies to try
        strategies = [
            ('ID selector', strategy_1_selector),
            ('Class selector', strategy_2_selector),
            ('Data attribute selector', strategy_3_selector),
            ('Structure selector', strategy_4_selector),
        ]
        
        # TODO: Try each strategy until one succeeds
        for strategy_name, selector in strategies:
            if selector is None:
                continue
                
            try:
                # TODO: Try to select elements using this selector
                rows = None  # Replace with: self.soup.select(selector)
                
                # TODO: Check if we got results
                if rows and len(rows) > 0:
                    logging.info(f"✓ {strategy_name} succeeded! Found {len(rows)} rows")
                    
                    # TODO: Extract data from rows
                    self.data = self._parse_rows(rows)
                    
                    # TODO: Validate the extracted data
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
                # TODO: Extract data from each row
                # Hint: Use row.select() or row.find() to get individual cells
                # Look for cells with classes like 'indicator-name', 'current-value', etc.
                
                # Get all cells in the row
                cells = row.find_all('td')
                
                if len(cells) >= 4:  # Make sure we have enough cells
                    indicator = {
                        'name': cells[0].text.strip(),
                        'value': cells[1].text.strip(),
                        'change': cells[2].text.strip(),
                        'period': cells[3].text.strip(),
                        'code': row.get('data-indicator-code', 'UNKNOWN')
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
        # TODO: Implement validation checks
        
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
            if len(item['name']) < 3:  # Names should be at least 3 characters
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


def test_scraper():
    """Test the scraper against all three HTML versions"""
    
    html_files = [
        ('data/website_sample_v1.html', 'Original HTML'),
        ('data/website_sample_v2.html', 'Modified HTML (changed IDs/classes)'),
        ('data/website_sample_v3.html', 'Major redesign'),
    ]
    
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
            
        except FileNotFoundError:
            print(f"✗ ERROR: File not found: {filepath}")
            print(f"Make sure you're running this from the repository root directory")
        except Exception as e:
            print(f"✗ FAILED: {str(e)}")


if __name__ == "__main__":
    print("="*80)
    print("Exercise 1: Adaptive Web Scraping")
    print("="*80)
    
    # TODO: Complete the implementation above, then run the test
    test_scraper()
    
    print("\n" + "="*80)
    print("Exercise Complete!")
    print("="*80)
    print("\nNext steps:")
    print("1. Review which selector strategies worked for each HTML version")
    print("2. Consider: What made some selectors more resilient than others?")
    print("3. Think about: How could you make this even more robust?")