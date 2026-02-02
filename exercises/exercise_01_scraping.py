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

Instructions:
1. Complete the TODOs marked as "Basic" first
2. Then move on to "Intermediate" TODOs
3. Finally, tackle "Advanced" TODOs if you have time
4. Test your scraper against all three HTML versions (v1, v2, v3)
5. The scraper should work across all versions using fallback strategies

Reference:
- If you get stuck, check exercise_01_scraping_OLD.py for reference
- The solution file is available in solutions/solution_01_scraping.py
"""

# TODO 1 (Basic): Import necessary libraries
# HINT: You'll need BeautifulSoup, requests, pandas, and json
# from bs4 import BeautifulSoup
# import requests
# import pandas as pd
# import json

from src.scrapers.base_scraper import BaseScraper
from src.utils.validators import validate_data_completeness


class AdaptiveScraper(BaseScraper):
    """
    A web scraper that adapts to HTML structure changes using multiple selector strategies.

    The scraper tries selectors in priority order (from selectors.csv) until one succeeds.
    This makes it resilient to website redesigns.
    """

    def __init__(self, url):
        """
        Initialize the scraper.

        Args:
            url (str): The URL to scrape
        """
        super().__init__(url)

        # TODO 2 (Basic): Load selectors from CSV and filter for this URL
        # HINT: Use self.load_selectors() to read data/selectors.csv
        # HINT: Filter the DataFrame where 'url' column matches this URL
        # HINT: Store filtered selectors in self.url_selectors
        # HINT: Initialize self.progress = [] for tracking progress
        pass

    def load_selectors(self, csv_file='data/selectors.csv'):
        """
        Load selector configuration from CSV file.

        Args:
            csv_file (str): Path to the selectors CSV file

        Returns:
            DataFrame: The loaded selectors configuration

        TODO 3 (Basic): Implement this method
        HINT: Use pandas to read the CSV file
        HINT: Return the DataFrame
        """
        pass

    def fetch(self):
        """
        Fetch HTML content from the URL.

        Returns:
            BeautifulSoup: Parsed HTML content

        TODO 4 (Basic): Implement this method
        HINT: Use requests.get() to fetch the URL
        HINT: Check response.raise_for_status() for errors
        HINT: Parse with BeautifulSoup(response.content, 'html.parser')
        HINT: Store the soup in self.soup
        HINT: Call self.log_progress() to log "Fetched HTML content"
        HINT: Return self.soup
        """
        pass

    def parse(self):
        """
        Parse HTML using selectors from CSV in priority order.
        Try each enabled selector until one succeeds.

        Returns:
            list: Extracted data as list of dictionaries

        TODO 5 (Intermediate): Implement this method
        HINT: Sort self.url_selectors by 'priority' column (lower = higher priority)
        HINT: Loop through each selector row
        HINT: Skip if row['enabled'] is False
        HINT: Try the selector using self.soup.select_one(row['selector'])
        HINT: If it finds a table, extract data with self._extract_table_data(table)
        HINT: Log progress with self.log_progress() for each attempt
        HINT: Return data on first success
        HINT: If all fail, return empty list []
        """
        pass

    def validate(self):
        """
        Validate that all required fields are present in scraped data.

        Returns:
            bool: True if validation passes, False otherwise

        TODO 6 (Advanced): Implement this method
        HINT: Check if self.data exists and is not empty
        HINT: Define required_fields = ['name', 'value', 'change', 'period']
        HINT: For each item in self.data, check all required fields exist and are not empty
        HINT: Return True if all items valid, False otherwise
        """
        pass

    def log_progress(self, message):
        """
        Log progress message for both console and web interface.

        Args:
            message (str): The progress message to log

        TODO 7 (Advanced): Implement this method
        HINT: Append message to self.progress list
        HINT: Also print(message) to show in console
        """
        pass

    def get_progress_json(self):
        """
        Return progress log as JSON string for web interface.

        Returns:
            str: JSON-formatted progress log
        """
        # This is provided for you - no need to modify
        import json
        return json.dumps(self.progress)


# TODO 8 (Basic): Test your scraper against all configured URLs
if __name__ == "__main__":
    """
    Main test script to verify your scraper works against all HTML versions.

    TODO: Implement the test code below
    HINT: Load all unique URLs from data/selectors.csv
    HINT: Create an AdaptiveScraper for each URL
    HINT: Call fetch(), parse(), and validate() for each
    HINT: Store results in a list
    HINT: Print summary of results
    """

    print("="*60)
    print("TESTING ADAPTIVE SCRAPER")
    print("="*60)

    # TODO: Your test code here
    # HINT: Read selectors CSV with pandas
    # HINT: Get unique URLs from 'url' column
    # HINT: Loop through each URL and test the scraper
    # HINT: Track success/failure for each URL

    pass

    # TODO 9 (Advanced): Save results to JSON for web interface
    # HINT: Create output/ directory if it doesn't exist
    # HINT: Save results list to output/scraping_results.json
    # HINT: Use json.dump() with indent=2 for readable formatting


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
    pass


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
    pass


if __name__ == "__main__" and False:  # Change to True to run bonus exercises
    print("\n" + "="*60)
    print("BONUS: PLAYWRIGHT EXERCISES")
    print("="*60 + "\n")

    # Uncomment to run bonus exercises after completing TODOs 1-9
    # playwright_bonus_exercise()
    # compare_scrapers()
