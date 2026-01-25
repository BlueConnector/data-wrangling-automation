/**
 * API Client - Handles all communication with Python Flask backend
 * Clean separation between frontend and backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

class ScraperAPI {
    /**
     * Check backend health status
     */
    static async checkHealth() {
        try {
            const response = await fetch(`${API_BASE_URL}/health`);
            const data = await response.json();
            return { success: true, data };
        } catch (error) {
            console.error('Health check failed:', error);
            return { success: false, error: error.message };
        }
    }

    /**
     * Get list of available selectors from configuration
     */
    static async getSelectors() {
        try {
            const response = await fetch(`${API_BASE_URL}/selectors`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch selectors');
            }
            
            return data;
        } catch (error) {
            console.error('Error fetching selectors:', error);
            return { success: false, error: error.message, selectors: [] };
        }
    }

    /**
     * Get HTML samples for each version
     */
    static async getHTMLSamples() {
        try {
            const response = await fetch(`${API_BASE_URL}/html-samples`);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to fetch HTML samples');
            }
            
            return data;
        } catch (error) {
            console.error('Error fetching HTML samples:', error);
            return { success: false, error: error.message, samples: {} };
        }
    }

    /**
     * Execute scraping with specified selector and version
     * 
     * @param {string} selector - CSS selector to use
     * @param {string} version - Version to scrape (v1, v2, v3)
     * @param {string} selectorName - Human-readable selector name
     */
    static async scrape(selector, version, selectorName) {
        try {
            const response = await fetch(`${API_BASE_URL}/scrape`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selector: selector,
                    version: version,
                    selector_name: selectorName
                })
            });
            
            const data = await response.json();
            
            if (!response.ok && response.status !== 500) {
                throw new Error(data.error || 'Scraping failed');
            }
            
            return data;
        } catch (error) {
            console.error('Scraping error:', error);
            return {
                success: false,
                error: error.message,
                data: []
            };
        }
    }

    /**
     * Test a selector without extracting full data
     * 
     * @param {string} selector - CSS selector to test
     * @param {string} version - Version to test against
     */
    static async testSelector(selector, version) {
        try {
            const response = await fetch(`${API_BASE_URL}/test-selector`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    selector: selector,
                    version: version
                })
            });
            
            const data = await response.json();
            
            if (!response.ok && response.status !== 500) {
                throw new Error(data.error || 'Test failed');
            }
            
            return data;
        } catch (error) {
            console.error('Test selector error:', error);
            return {
                success: false,
                found: false,
                count: 0,
                error: error.message
            };
        }
    }

    /**
     * Validate extracted data
     * 
     * @param {Array} data - Extracted data to validate
     */
    static async validateData(data) {
        try {
            const response = await fetch(`${API_BASE_URL}/validate`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    data: data
                })
            });
            
            const result = await response.json();
            
            if (!response.ok) {
                throw new Error(result.error || 'Validation failed');
            }
            
            return result;
        } catch (error) {
            console.error('Validation error:', error);
            return {
                success: false,
                error: error.message
            };
        }
    }
}

/**
 * Update API status indicator in UI
 */
async function updateAPIStatus() {
    const statusIndicator = document.getElementById('statusIndicator');
    const statusText = document.getElementById('statusText');
    
    const health = await ScraperAPI.checkHealth();
    
    if (health.success) {
        statusIndicator.className = 'status-indicator status-healthy';
        statusText.textContent = 'Backend connected';
    } else {
        statusIndicator.className = 'status-indicator status-error';
        statusText.textContent = 'Backend offline';
    }
}

// Check API status on load and periodically
updateAPIStatus();
setInterval(updateAPIStatus, 30000); // Check every 30 seconds