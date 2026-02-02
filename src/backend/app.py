"""
Demo API for Exercise 1: Selector Strategy Testing

This API provides endpoints to test different CSS selectors against
sample HTML files, demonstrating how web scraping strategies work.

Endpoints:
- /api/demo/selectors - Get all selectors from CSV
- /api/demo/test-selector - Test a specific selector
- /api/demo/test-all - Test all selectors
- /api/demo/playwright - Compare BeautifulSoup vs Playwright
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from bs4 import BeautifulSoup
import logging
import time

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Path to data directory
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))

class SelectorDemo:
    """Demo class for testing CSS selectors against HTML samples"""

    def __init__(self):
        self.selectors_df = None
        self.html_samples = {}
        self.data_path = DATA_DIR

    def load_selectors(self):
        """Load selector configuration from CSV"""
        selectors_path = os.path.join(DATA_DIR, 'selectors.csv')
        try:
            self.selectors_df = pd.read_csv(selectors_path)
            logger.info(f"Loaded {len(self.selectors_df)} selectors from {selectors_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to load selectors from {selectors_path}: {e}")
            self.selectors_df = None
            return False

    def load_html_samples(self):
        """Load HTML sample files"""
        samples = {}
        versions = ['v1', 'v2', 'v3']

        for version in versions:
            filename = f'{version}.html'
            filepath = os.path.join(self.data_path, 'website_samples', filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    samples[version] = f.read()
                logger.info(f"Loaded HTML sample: {version}")
            except Exception as e:
                logger.error(f"Failed to load {version}: {e}")
                samples[version] = None

        self.html_samples = samples
        return samples

    def test_selector(self, selector, version, selector_name="Test Selector"):
        """
        Test a CSS selector against a specific HTML version

        Args:
            selector (str): CSS selector to test
            version (str): HTML version to test against (v1, v2, v3)
            selector_name (str): Human-readable name for the selector

        Returns:
            dict: Test results
        """
        try:
            # Get HTML content for version
            html_content = self.html_samples.get(version)
            if not html_content:
                return {
                    'success': False,
                    'error': f'HTML sample for version {version} not found',
                    'selector': selector,
                    'selector_name': selector_name,
                    'version': version,
                    'data': []
                }

            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')

            # Try to find elements with selector
            rows = soup.select(selector)

            if not rows or len(rows) == 0:
                return {
                    'success': False,
                    'message': f'Selector found no elements',
                    'selector': selector,
                    'selector_name': selector_name,
                    'version': version,
                    'rows_found': 0,
                    'data': []
                }

            # Extract data from rows
            data = self._parse_table_rows(rows)

            return {
                'success': True,
                'message': f'Successfully found {len(rows)} rows, extracted {len(data)} data points',
                'selector': selector,
                'selector_name': selector_name,
                'version': version,
                'rows_found': len(rows),
                'data': data
            }

        except Exception as e:
            logger.error(f"Selector test error: {e}")
            return {
                'success': False,
                'error': str(e),
                'selector': selector,
                'selector_name': selector_name,
                'version': version,
                'data': []
            }

    def _parse_table_rows(self, rows):
        """Parse table rows into structured data"""
        data = []

        for row in rows:
            # Skip header rows
            if row.find('th'):
                continue

            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:
                try:
                    indicator = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    change = cells[2].get_text(strip=True)

                    data.append({
                        'indicator': indicator,
                        'value': value,
                        'change': change
                    })
                except (IndexError, AttributeError) as e:
                    logger.warning(f"Failed to parse row: {e}")
                    continue

        return data

# Global demo instance
demo = SelectorDemo()

@app.route('/', methods=['GET'])
def hello_world():
    return "Scraper backend server is running!"

@app.route('/api/demo/selectors', methods=['GET'])
def get_selectors():
    """Get all selectors from CSV"""
    logger.info("API call: get_selectors")
    if demo.selectors_df is None:
        logger.info("Loading selectors...")
        demo.load_selectors()

    if demo.selectors_df is None:
        logger.error("selectors_df is None")
        return jsonify({'error': 'Failed to load selectors'}), 500

    logger.info(f"Converting {len(demo.selectors_df)} selectors to dict")
    # Convert to list of dicts for JSON response
    selectors = demo.selectors_df.to_dict('records')
    logger.info(f"Returning {len(selectors)} selectors")
    return jsonify({'selectors': selectors})

@app.route('/api/demo/test-selector', methods=['POST'])
def test_selector():
    """Test a specific selector against a version"""
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    selector = data.get('selector')
    version = data.get('version')
    selector_name = data.get('selector_name', 'Test Selector')

    if not selector or not version:
        return jsonify({'error': 'Selector and version are required'}), 400

    # Load HTML samples if not loaded
    if not demo.html_samples:
        demo.load_html_samples()

    result = demo.test_selector(selector, version, selector_name)
    return jsonify(result)

@app.route('/api/demo/test-all', methods=['GET'])
def test_all_selectors():
    """Test all selectors and return results"""
    if not demo.selectors_df:
        demo.load_selectors()

    if not demo.html_samples:
        demo.load_html_samples()

    if demo.selectors_df is None:
        return jsonify({'error': 'Failed to load selectors'}), 500

    results = []

    # Group selectors by URL/version
    for _, row in demo.selectors_df.iterrows():
        url = row['url']
        version = url.split('_')[-1].replace('.html', '')  # Extract v1, v2, v3

        result = demo.test_selector(
            row['selector'],
            version,
            row['selector_name']
        )

        # Add additional metadata
        result.update({
            'priority': row['priority'],
            'enabled': row['enabled'],
            'comment': row.get('comment', ''),
            'url': url
        })

        results.append(result)

    return jsonify({'results': results})

@app.route('/api/demo/selector-fallback', methods=['POST'])
def selector_fallback_demo():
    """
    Demonstrate selector fallback strategy for a specific version

    Shows step-by-step how selectors are tried in priority order
    until one succeeds, demonstrating resilience to HTML changes.

    Tests the SAME set of selectors across all versions to show
    which ones break and which ones survive redesigns.
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    version = data.get('version', 'v1')

    # Load selectors and HTML if needed
    if demo.selectors_df is None:
        demo.load_selectors()

    if not demo.html_samples:
        demo.load_html_samples()

    # Define a consistent set of selectors to test across ALL versions
    # This shows which selectors break and which survive redesigns
    universal_selectors = [
        {
            'priority': 1,
            'selector_name': 'ID selector (v1)',
            'selector': '#statistics-table tbody tr',
            'comment': 'Original ID from v1 - very specific, breaks on redesign'
        },
        {
            'priority': 2,
            'selector_name': 'ID selector (v2)',
            'selector': '#stats-data-grid tbody tr',
            'comment': 'New ID from v2 redesign - also breaks when changed'
        },
        {
            'priority': 3,
            'selector_name': 'Class selector (v1)',
            'selector': 'table.data-table tbody tr',
            'comment': 'Original class name - changes with redesigns'
        },
        {
            'priority': 4,
            'selector_name': 'Class selector (v2)',
            'selector': 'table.stats-grid-view tbody tr',
            'comment': 'Updated class name - only works on v2'
        },
        {
            'priority': 5,
            'selector_name': 'Data attribute',
            'selector': 'table[data-content="statistics"] tbody tr',
            'comment': 'Semantic attribute - most stable, added in v3'
        },
        {
            'priority': 6,
            'selector_name': 'ARIA role (grid)',
            'selector': 'table[role="grid"] tbody tr',
            'comment': 'Accessibility attribute - works on v1 and v2'
        },
        {
            'priority': 7,
            'selector_name': 'ARIA role (table)',
            'selector': 'table[role="table"] tbody tr',
            'comment': 'Accessibility attribute - works on v3'
        },
        {
            'priority': 8,
            'selector_name': 'Generic table',
            'selector': 'table tbody tr',
            'comment': 'Last resort - matches any table (may get wrong one)'
        }
    ]

    # Test each selector in priority order
    attempts = []
    first_success = None

    for selector_config in universal_selectors:
        result = demo.test_selector(
            selector_config['selector'],
            version,
            selector_config['selector_name']
        )

        attempt = {
            'priority': selector_config['priority'],
            'selector_name': selector_config['selector_name'],
            'selector': selector_config['selector'],
            'comment': selector_config['comment'],
            'success': result['success'],
            'rows_found': result.get('rows_found', 0),
            'data_sample': result.get('data', [])[:2]  # First 2 rows only
        }

        attempts.append(attempt)

        # Track first success
        if result['success'] and first_success is None:
            first_success = attempt

    # Count successes and failures
    successes = len([a for a in attempts if a['success']])
    failures = len([a for a in attempts if not a['success']])

    return jsonify({
        'version': version,
        'total_selectors': len(attempts),
        'successes': successes,
        'failures': failures,
        'attempts': attempts,
        'first_success': first_success,
        'explanation': {
            'strategy': 'Test multiple selectors in priority order until one succeeds',
            'why_it_works': 'Different selectors target different HTML attributes. When a site redesigns, some break but others survive, ensuring the scraper keeps working.'
        }
    })

@app.route('/api/demo/playwright', methods=['POST'])
def playwright_demo():
    """
    Compare BeautifulSoup vs Playwright scraping approaches

    This endpoint demonstrates:
    1. BeautifulSoup (static HTML parsing)
    2. Playwright (browser automation)
    3. Performance comparison
    4. When to use each approach
    """
    data = request.get_json()

    if not data:
        return jsonify({'error': 'No data provided'}), 400

    version = data.get('version', 'v1')
    selector = data.get('selector', 'table[data-content="statistics"] tbody tr')

    # Load HTML samples if not loaded
    if not demo.html_samples:
        demo.load_html_samples()

    html_content = demo.html_samples.get(version)
    if not html_content:
        return jsonify({'error': f'HTML sample for version {version} not found'}), 404

    try:
        # METHOD 1: BeautifulSoup (traditional approach)
        start_time = time.time()
        soup_bs = BeautifulSoup(html_content, 'html.parser')
        rows_bs = soup_bs.select(selector)
        data_bs = demo._parse_table_rows(rows_bs)
        bs_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        # METHOD 2: Playwright (browser automation)
        # Note: For this demo, we'll simulate Playwright by showing what it would do
        # In a real scenario, Playwright would launch a browser and execute JavaScript
        start_time = time.time()

        try:
            from playwright.sync_api import sync_playwright

            # Create a temporary HTML file for Playwright to load
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
                f.write(html_content)
                temp_path = f.name

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                page = browser.new_page()
                page.goto(f'file://{temp_path}')

                # Get content after JavaScript execution (if any)
                content_pw = page.content()
                browser.close()

            # Clean up temp file
            os.unlink(temp_path)

            # Parse with BeautifulSoup (same as before, but now with JS-executed content)
            soup_pw = BeautifulSoup(content_pw, 'html.parser')
            rows_pw = soup_pw.select(selector)
            data_pw = demo._parse_table_rows(rows_pw)
            pw_time = (time.time() - start_time) * 1000

            playwright_available = True

        except ImportError:
            # Playwright not installed - show comparison without it
            data_pw = data_bs  # Same data since no JavaScript in our samples
            pw_time = bs_time * 1.5  # Simulate typical Playwright overhead
            playwright_available = False

        # Compare results
        comparison = {
            'version': version,
            'selector': selector,
            'playwright_available': playwright_available,
            'beautifulsoup': {
                'method': 'BeautifulSoup',
                'description': 'Static HTML parsing - fast and simple',
                'execution_time_ms': round(bs_time, 2),
                'rows_found': len(rows_bs),
                'data_extracted': len(data_bs),
                'data': data_bs[:3],  # First 3 rows for preview
                'pros': [
                    'Very fast',
                    'Low memory usage',
                    'Simple to use',
                    'No browser required'
                ],
                'cons': [
                    'Cannot handle JavaScript',
                    'No interaction with page',
                    'Only sees initial HTML'
                ]
            },
            'playwright': {
                'method': 'Playwright',
                'description': 'Browser automation - handles JavaScript and dynamic content',
                'execution_time_ms': round(pw_time, 2),
                'rows_found': len(rows_pw) if playwright_available else len(rows_bs),
                'data_extracted': len(data_pw),
                'data': data_pw[:3],  # First 3 rows for preview
                'pros': [
                    'Handles JavaScript',
                    'Can interact with page',
                    'Sees rendered content',
                    'Supports modern web apps'
                ],
                'cons': [
                    'Slower',
                    'Higher memory usage',
                    'More complex setup',
                    'Requires browser'
                ]
            },
            'recommendation': {
                'for_static_sites': 'Use BeautifulSoup - it\'s faster and simpler',
                'for_dynamic_sites': 'Use Playwright - it can execute JavaScript',
                'for_this_demo': 'BeautifulSoup works fine since our samples are static HTML'
            }
        }

        return jsonify(comparison)

    except Exception as e:
        logger.error(f"Playwright demo error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Load data on startup (don't fail if loading fails)
    demo.load_selectors()
    demo.load_html_samples()

    print(f"Starting Flask server on port 8080...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Selectors loaded: {demo.selectors_df is not None}")
    print(f"HTML samples loaded: {len(demo.html_samples)} versions")

    app.run(host='0.0.0.0', debug=True, port=8080)