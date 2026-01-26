"""
Exercise 1: Build an Adaptive Web Scraper

Learning Objectives:
- Implement multiple selector strategies
- Handle HTML structure changes gracefully
- Validate scraped data
- Test against different HTML versions

Estimated Time: 20 minutes

Difficulty Levels:
- Basic: Implement single selector strategy
- Intermediate: Add multiple strategies with fallback
- Advanced: Add validation and error handling
"""

# TODO 1: Import necessary libraries
# HINT: You'll need BeautifulSoup, requests, pandas, and json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

from src.scrapers.base_scraper import BaseScraper
from src.utils.validators import validate_data_completeness


class AdaptiveScraper(BaseScraper):
    # TODO 2: Initialize scraper with URL and load selectors from CSV
    def __init__(self, url):
        super().__init__(url)
        # TODO: Load selectors from CSV and filter for this URL
        self.selectors_df = self.load_selectors()
        self.url_selectors = self.selectors_df[self.selectors_df['url'] == url]
        self.progress = []  # For tracking progress
    
    # TODO 3: Load selectors from CSV (Basic)
    def load_selectors(self, csv_file='data/selectors.csv'):
        """Load selector configuration from CSV"""
        # Your code here
        df = pd.read_csv(csv_file)
        return df
    
    # TODO 4: Implement the fetch method
    def fetch(self):
        """Fetch HTML content from the URL"""
        # Your code here
        response = requests.get(self.url)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.content, 'html.parser')
        self.log_progress("Fetched HTML content")
        return self.soup
    
    # TODO 5: Implement the parse method with priority-based fallback (Intermediate)
    def parse(self):
        """
        Parse HTML using selectors from CSV in priority order.
        Try each enabled selector until one succeeds.
        """
        # TODO: Sort selectors by priority (lower number = higher priority)
        sorted_selectors = self.url_selectors.sort_values('priority')
        
        for _, row in sorted_selectors.iterrows():
            # TODO: Skip disabled selectors
            if not row['enabled']:
                continue
            
            selector = row['selector']
            selector_name = row['selector_name']
            
            try:
                self.log_progress(f"Trying {selector_name}: {row['comment']}")
                
                # TODO: Use BeautifulSoup to find table
                table = self.soup.select_one(selector)
                
                if table:
                    self.log_progress(f"✓ {selector_name} succeeded")
                    # Extract data from table
                    data = self._extract_table_data(table)
                    self.data = data
                    return data
                else:
                    self.log_progress(f"✗ {selector_name} found no table")
                    
            except Exception as e:
                self.log_progress(f"✗ {selector_name} failed: {str(e)}")
                continue
        
        self.log_progress("All selectors failed")
        return []
    
    # TODO 6: Implement validation (Advanced)
    def validate(self):
        """Ensure all required fields are present"""
        # Your code here
        if not hasattr(self, 'data') or not self.data:
            return False
        required_fields = ['name', 'value', 'change', 'period']
        for item in self.data:
            if not all(field in item and item[field] for field in required_fields):
                return False
        return True
    
    # TODO 7: Add progress logging for web interface (Advanced)
    def log_progress(self, message):
        """Log progress message for web interface"""
        self.progress.append(message)
        print(message)  # Also print to console
    
    def get_progress_json(self):
        """Return progress as JSON for web interface"""
        return json.dumps(self.progress)


# TODO 8: Test your scraper against all configured URLs (Basic)
if __name__ == "__main__":
    # TODO: Load all unique URLs from selectors CSV
    selectors_df = pd.read_csv('data/selectors.csv')
    test_urls = selectors_df['url'].unique()
    
    results = []
    for url in test_urls:
        print(f"\nTesting {url}")
        scraper = AdaptiveScraper(url)
        try:
            scraper.fetch()
            data = scraper.parse()
            if scraper.validate():
                print(f"✓ Success: Extracted {len(data)} items")
            else:
                print("✗ Validation failed")
                results.append({'url': url, 'status': 'VALIDATION_FAILED', 'count': 0})
        except Exception as e:
            print(f"✗ Error: {e}")
            results.append({'url': url, 'status': f'ERROR: {str(e)}', 'count': 0})
    
    # TODO 9: Save results to JSON for web interface (Advanced)
    with open('output/scraping_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("SCRAPING COMPLETE")
    print(f"{'='*60}")
    for result in results:
        status_icon = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_icon} {result['url']}: {result['status']}")
        if result['count'] > 0:
            print(f"  → Extracted {result['count']} indicators")
