"""
Demo 1: Building a Resilient Web Scraper
Instructor demonstration showing adaptive scraping patterns

This demo is designed for live presentation and includes:
- Step-by-step progression from fragile to resilient
- Clear console output for audience visibility
- Deliberate failures to demonstrate problems
- Recovery mechanisms to show solutions
"""

from bs4 import BeautifulSoup
import logging
import time

# Configure logging for demo visibility
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)


class Demo:
    """Helper class for demo presentation"""
    
    @staticmethod
    def pause(message="Press Enter to continue...", seconds=0):
        """Pause for audience comprehension"""
        if seconds > 0:
            time.sleep(seconds)
        else:
            input(f"\n{message}")
    
    @staticmethod
    def section(title):
        """Print a section header"""
        print("\n" + "="*80)
        print(f"  {title}")
        print("="*80 + "\n")


def demo_fragile_scraper():
    """
    DEMO PART 1: Show why scrapers break
    Demonstrate a fragile scraper that only works with v1
    """
    Demo.section("PART 1: The Fragile Scraper (Why Scrapers Break)")
    
    print("Let's start with a simple, straightforward scraper...")
    print("We'll use a specific ID selector: '#statistics-table'\n")
    
    Demo.pause()
    
    # Load v1 HTML
    print("Testing with Original HTML (v1)...")
    with open('data/website_sample_v1.html', 'r', encoding='utf-8') as f:
        html_v1 = f.read()
    
    soup = BeautifulSoup(html_v1, 'html.parser')
    
    # Fragile selector - only works for v1
    print("Using selector: #statistics-table tbody tr")
    rows = soup.select('#statistics-table tbody tr')
    
    if rows:
        print(f"✓ SUCCESS! Found {len(rows)} rows")
        print(f"  First indicator: {rows[0].find_all('td')[0].text.strip()}")
    else:
        print("✗ FAILED! No data found")
    
    Demo.pause()
    
    # Now try with v2 - this will fail!
    print("\nTesting with Modified HTML (v2)...")
    print("(Website had a redesign - ID changed to 'stats-data-grid')\n")
    
    with open('data/website_sample_v2.html', 'r', encoding='utf-8') as f:
        html_v2 = f.read()
    
    soup = BeautifulSoup(html_v2, 'html.parser')
    
    print("Using SAME selector: #statistics-table tbody tr")
    rows = soup.select('#statistics-table tbody tr')
    
    if rows:
        print(f"✓ SUCCESS! Found {len(rows)} rows")
    else:
        print("✗ FAILED! No data found")
        print("   The scraper broke because the ID changed!")
        print("   This is exactly what happens in production...")
    
    Demo.pause()
    
    print("\n🔍 KEY INSIGHT:")
    print("   ID and class selectors are FRAGILE - they break when")
    print("   websites update their styling or structure.")
    print("   We need a more resilient approach...")
    
    Demo.pause()


def demo_fallback_strategy():
    """
    DEMO PART 2: Implement fallback selectors
    Show how multiple strategies make scrapers resilient
    """
    Demo.section("PART 2: The Resilient Scraper (Multiple Fallback Strategies)")
    
    print("Let's improve our scraper with MULTIPLE selector strategies...")
    print("We'll try several selectors until one works.\n")
    
    Demo.pause()
    
    # Define fallback strategies
    strategies = [
        ('Primary ID selector', '#statistics-table tbody tr'),
        ('Alternative ID selector', '#stats-data-grid tbody tr'),
        ('Data attribute selector', 'table[data-content="statistics"] tbody tr'),
        ('Generic table selector', 'table tbody tr'),
    ]
    
    print("Our fallback strategies:")
    for i, (name, selector) in enumerate(strategies, 1):
        print(f"  {i}. {name}")
        print(f"     → {selector}")
    
    Demo.pause()
    
    # Test against v2
    print("\nTesting against Modified HTML (v2)...\n")
    
    with open('data/website_sample_v2.html', 'r', encoding='utf-8') as f:
        html_v2 = f.read()
    
    soup = BeautifulSoup(html_v2, 'html.parser')
    
    # Try each strategy
    for i, (name, selector) in enumerate(strategies, 1):
        print(f"Attempting strategy {i}: {name}")
        print(f"  Selector: {selector}")
        
        rows = soup.select(selector)
        
        if rows and len(rows) >= 8:
            print(f"  ✓ SUCCESS! Found {len(rows)} rows")
            print(f"  First indicator: {rows[0].find_all('td')[0].text.strip()}")
            print(f"\n🎯 Strategy {i} worked! Moving on...")
            break
        else:
            print(f"  ✗ Failed (found {len(rows)} rows)")
            if i < len(strategies):
                print(f"  → Trying next strategy...")
        
        print()
        time.sleep(1)  # Pause for visibility
    
    Demo.pause()
    
    print("\n🔍 KEY INSIGHT:")
    print("   With fallback strategies, the scraper AUTOMATICALLY")
    print("   adapts when the website changes. No manual intervention!")
    
    Demo.pause()


def demo_validation():
    """
    DEMO PART 3: Add validation
    Show why validation is critical for data quality
    """
    Demo.section("PART 3: Adding Validation (Catching Bad Data)")
    
    print("Finding data is not enough - we need to VALIDATE it!")
    print("Let's add validation checks...\n")
    
    Demo.pause()
    
    # Load HTML
    with open('data/website_sample_v1.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.select('#statistics-table tbody tr')
    
    print(f"Extracted {len(rows)} rows")
    print("\nRunning validation checks:\n")
    
    time.sleep(1)
    
    # Check 1: Row count
    print("1. Checking row count...")
    expected_rows = 8
    if len(rows) >= expected_rows:
        print(f"   ✓ Found {len(rows)} rows (expected at least {expected_rows})")
    else:
        print(f"   ✗ Only found {len(rows)} rows (expected at least {expected_rows})")
    
    time.sleep(1)
    
    # Check 2: Data structure
    print("\n2. Checking data structure...")
    first_row_cells = rows[0].find_all('td')
    if len(first_row_cells) >= 4:
        print(f"   ✓ Each row has {len(first_row_cells)} cells (need at least 4)")
    else:
        print(f"   ✗ Rows only have {len(first_row_cells)} cells")
    
    time.sleep(1)
    
    # Check 3: Data quality
    print("\n3. Checking data quality...")
    indicator_name = first_row_cells[0].text.strip()
    if len(indicator_name) > 3:
        print(f"   ✓ Indicator names are non-empty: '{indicator_name}'")
    else:
        print(f"   ✗ Indicator names are too short or empty")
    
    time.sleep(1)
    
    # Check 4: Data attributes
    print("\n4. Checking for indicator codes...")
    code = rows[0].get('data-indicator-code')
    if code:
        print(f"   ✓ Found indicator code: '{code}'")
    else:
        print(f"   ⚠ No indicator code found (not critical)")
    
    time.sleep(1)
    
    print("\n" + "-"*80)
    print("✓ ALL VALIDATION CHECKS PASSED")
    print("-"*80)
    
    Demo.pause()
    
    print("\n🔍 KEY INSIGHT:")
    print("   Validation ensures we catch extraction problems EARLY,")
    print("   before bad data gets into reports or databases.")
    
    Demo.pause()


def demo_complete_scraper():
    """
    DEMO PART 4: Put it all together
    Show the complete resilient scraper in action
    """
    Demo.section("PART 4: The Complete Resilient Scraper")
    
    print("Now let's see the COMPLETE scraper with:")
    print("  ✓ Multiple fallback strategies")
    print("  ✓ Data validation")
    print("  ✓ Comprehensive logging")
    print("  ✓ Error handling\n")
    
    Demo.pause()
    
    class ResilientScraper:
        """Complete resilient scraper implementation"""
        
        def __init__(self, html_content):
            self.soup = BeautifulSoup(html_content, 'html.parser')
            self.data = []
        
        def extract(self):
            """Extract data with fallback strategies"""
            strategies = [
                ('ID #statistics-table', '#statistics-table tbody tr'),
                ('ID #stats-data-grid', '#stats-data-grid tbody tr'),
                ('Data attribute', 'table[data-content="statistics"] tbody tr'),
                ('Table structure', 'table tbody tr'),
            ]
            
            for name, selector in strategies:
                logging.info(f"Trying: {name}")
                rows = self.soup.select(selector)
                
                if rows and len(rows) >= 8:
                    logging.info(f"✓ {name} succeeded! Found {len(rows)} rows")
                    self.data = self._parse(rows)
                    
                    if self._validate():
                        logging.info("✓ Validation passed")
                        return self.data
                    else:
                        logging.warning("✗ Validation failed, trying next strategy")
                else:
                    logging.warning(f"✗ {name} failed")
            
            raise Exception("All strategies failed")
        
        def _parse(self, rows):
            """Parse table rows"""
            data = []
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 4:
                    data.append({
                        'name': cells[0].text.strip(),
                        'value': cells[1].text.strip(),
                        'code': row.get('data-indicator-code', 'UNKNOWN')
                    })
            return data
        
        def _validate(self):
            """Validate extracted data"""
            if len(self.data) < 8:
                return False
            for item in self.data:
                if len(item['name']) < 3:
                    return False
            return True
    
    # Test against all three versions
    html_files = [
        ('data/website_sample_v1.html', 'v1 (Original)'),
        ('data/website_sample_v2.html', 'v2 (Modified IDs)'),
        ('data/website_sample_v3.html', 'v3 (Major Redesign)'),
    ]
    
    for filepath, version in html_files:
        print(f"\n{'─'*80}")
        print(f"Testing: {version}")
        print('─'*80 + "\n")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            html = f.read()
        
        scraper = ResilientScraper(html)
        try:
            scraper.extract()
            print(f"\n✓ Successfully extracted {len(scraper.data)} indicators")
            print(f"  Sample: {scraper.data[0]['name']}")
        except Exception as e:
            print(f"\n✗ Failed: {e}")
        
        time.sleep(2)  # Pause between versions
    
    Demo.pause()
    
    print("\n" + "="*80)
    print("🎉 SUCCESS! The scraper works across ALL THREE HTML versions!")
    print("="*80)
    print("\nThis is the power of resilient scraping:")
    print("  • Automatic adaptation to layout changes")
    print("  • Built-in validation for data quality")
    print("  • Clear logging for debugging")
    print("  • Graceful failure handling")
    
    Demo.pause()


def demo_real_world_tips():
    """
    DEMO PART 5: Real-world production tips
    Share practical advice from production experience
    """
    Demo.section("PART 5: Production Tips and Best Practices")
    
    print("When deploying scrapers in production, remember:\n")
    
    tips = [
        ("Set up monitoring", 
         "Alert when scrapers fail or data looks unusual"),
        
        ("Be polite", 
         "Add delays between requests (time.sleep(1))"),
        
        ("Use caching", 
         "Don't re-scrape data that hasn't changed"),
        
        ("Log everything", 
         "You'll thank yourself when debugging at 2am"),
        
        ("Test with archived HTML", 
         "Keep copies of old page versions for testing"),
        
        ("Have a fallback plan", 
         "What happens if ALL selectors fail?"),
        
        ("Check robots.txt", 
         "Respect the website's scraping policies"),
        
        ("Consider APIs first", 
         "APIs are more stable than scraping"),
    ]
    
    for i, (tip, explanation) in enumerate(tips, 1):
        print(f"{i}. {tip}")
        print(f"   → {explanation}\n")
        time.sleep(1)
    
    Demo.pause()
    
    print("\n🎯 FINAL THOUGHT:")
    print("   Scrapers WILL break. The question is: will they")
    print("   recover automatically, or will you get a call at 2am?")
    print("\n   Build resilience from day one!")
    
    Demo.pause()


def main():
    """Run the complete demonstration"""
    
    print("\n" + "="*80)
    print("  DEMO: Building a Resilient Web Scraper")
    print("  Instructor: [Your Name]")
    print("  DOS Data Analytics Training")
    print("="*80)
    
    Demo.pause("Press Enter to start the demonstration...")
    
    # Run each demo section
    demo_fragile_scraper()
    demo_fallback_strategy()
    demo_validation()
    demo_complete_scraper()
    demo_real_world_tips()
    
    # Final summary
    Demo.section("DEMONSTRATION COMPLETE")
    
    print("What we covered:")
    print("  1. Why scrapers break (fragile selectors)")
    print("  2. How to make them resilient (fallback strategies)")
    print("  3. Why validation matters (data quality)")
    print("  4. Complete working example (all versions)")
    print("  5. Production best practices (real-world tips)")
    
    print("\nNow it's your turn!")
    print("  → Open exercises/exercise1_web_scraping.py")
    print("  → Implement the TODO sections")
    print("  → Test against all three HTML versions")
    
    print("\n" + "="*80)
    print("Questions?")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()