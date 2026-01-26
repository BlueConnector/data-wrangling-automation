"""
Flask Backend API for Web Scraping Exercise
Provides REST API endpoints for the frontend to execute scraping operations

Run with: python src/backend/app.py
Access at: http://localhost:5000
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sys
import os

# Add parent directory to path to import scraper module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.backend.scraper import ScraperEngine

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)  # Enable CORS for frontend-backend communication

# Initialize scraper engine
scraper_engine = ScraperEngine()


@app.route('/')
def index():
    """Serve the frontend HTML page"""
    return send_from_directory('../frontend', 'index.html')


@app.route('/api/selectors', methods=['GET'])
def get_selectors():
    """
    Get list of available selectors from configuration
    
    Returns:
        JSON: List of selector configurations
    """
    try:
        selectors = scraper_engine.get_selectors()
        return jsonify({
            'success': True,
            'selectors': selectors
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/html-samples', methods=['GET'])
def get_html_samples():
    """
    Get HTML samples for each version
    
    Returns:
        JSON: HTML content for v1, v2, v3
    """
    try:
        samples = scraper_engine.get_html_samples()
        return jsonify({
            'success': True,
            'samples': samples
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/scrape', methods=['POST'])
def scrape():
    """
    Execute scraping with specified selector and version
    
    Request Body:
        {
            "selector": "string - CSS selector to use",
            "version": "string - v1, v2, or v3",
            "selector_name": "string - human-readable name"
        }
    
    Returns:
        JSON: Scraping results including success status and extracted data
    """
    try:
        data = request.get_json()
        
        if not data or 'selector' not in data or 'version' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: selector and version'
            }), 400
        
        selector = data['selector']
        version = data['version']
        selector_name = data.get('selector_name', 'Custom Selector')
        
        # Execute scraping
        result = scraper_engine.scrape(selector, version, selector_name)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'data': []
        }), 500


@app.route('/api/test-selector', methods=['POST'])
def test_selector():
    """
    Test a selector against a specific HTML version
    
    Request Body:
        {
            "selector": "string - CSS selector to test",
            "version": "string - v1, v2, or v3"
        }
    
    Returns:
        JSON: Test results including whether selector found elements
    """
    try:
        data = request.get_json()
        
        if not data or 'selector' not in data or 'version' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required fields: selector and version'
            }), 400
        
        selector = data['selector']
        version = data['version']
        
        # Test selector
        result = scraper_engine.test_selector(selector, version)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/validate', methods=['POST'])
def validate_data():
    """
    Validate scraped data
    
    Request Body:
        {
            "data": [...] - Array of extracted data items
        }
    
    Returns:
        JSON: Validation results
    """
    try:
        data = request.get_json()
        
        if not data or 'data' not in data:
            return jsonify({
                'success': False,
                'error': 'Missing required field: data'
            }), 400
        
        extracted_data = data['data']
        
        # Validate data
        validation_result = scraper_engine.validate_data(extracted_data)
        
        return jsonify(validation_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON: Server status
    """
    return jsonify({
        'status': 'healthy',
        'message': 'Web Scraping Exercise API is running'
    })


if __name__ == '__main__':
    print("="*80)
    print("🚀 Starting Web Scraping Exercise Backend")
    print("="*80)
    print("\nBackend API running at: http://localhost:5000")
    print("Frontend available at: http://localhost:5000")
    print("\nAPI Endpoints:")
    print("  GET  /api/selectors       - Get available selectors")
    print("  GET  /api/html-samples    - Get HTML samples")
    print("  POST /api/scrape          - Execute scraping")
    print("  POST /api/test-selector   - Test a selector")
    print("  POST /api/validate        - Validate data")
    print("  GET  /api/health          - Health check")
    print("\nPress CTRL+C to stop")
    print("="*80 + "\n")
    
    app.run(debug=True, port=5000)