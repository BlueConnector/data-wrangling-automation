"""
Demo API for Exercise 1: Selector Strategy Testing

This API provides endpoints to test different CSS selectors against
sample HTML files, demonstrating how web scraping strategies work.
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os
from bs4 import BeautifulSoup
import logging

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
    if not demo.selectors_df:
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

if __name__ == '__main__':
    # Load data on startup (don't fail if loading fails)
    demo.load_selectors()
    demo.load_html_samples()

    print(f"Starting Flask server on port 8080...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Selectors loaded: {demo.selectors_df is not None}")
    print(f"HTML samples loaded: {len(demo.html_samples)} versions")

    app.run(host='0.0.0.0', debug=True, port=8080)