"""Base scraper class with common functionality"""
class BaseScraper:
    def __init__(self, url):
        self.url = url
        self.data = None

    def fetch(self):
        """Fetch HTML content"""
        pass

    def parse(self):
        """Parse HTML - to be implemented by subclasses"""
        raise NotImplementedError

    def validate(self):
        """Validate scraped data"""
        pass
        """
        Load HTML samples for each version
        
        Returns:
            dict: HTML content for each version
        """
        samples = {}
        
        versions = {
            'v1': 'website_sample_v1.html',
            'v2': 'website_sample_v2.html',
            'v3': 'website_sample_v3.html'
        }
        
        for version, filename in versions.items():
            filepath = os.path.join(self.data_path, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    samples[version] = f.read()
                logger.info(f"Loaded HTML sample: {version}")
            except Exception as e:
                logger.error(f"Error loading {version}: {str(e)}")
                samples[version] = None
        
        return samples
    
    def scrape(self, selector, version, selector_name="Custom Selector"):
        """
        Execute scraping with specified selector
        
        Args:
            selector (str): CSS selector to use
            version (str): Version to scrape (v1, v2, v3)
            selector_name (str): Human-readable name for logging
            
        Returns:
            dict: Scraping results
        """
        try:
            # Load HTML for specified version
            html_content = self._load_html(version)
            
            if not html_content:
                return {
                    'success': False,
                    'error': f'Could not load HTML for {version}',
                    'data': []
                }
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Try to find elements with selector
            rows = soup.select(selector)
            
            if not rows or len(rows) == 0:
                return {
                    'success': False,
                    'message': f'Selector "{selector}" found no elements in {version}',
                    'selector_name': selector_name,
                    'rows_found': 0,
                    'data': []
                }
            
            # Extract data from rows
            data = self._parse_rows(rows)
            
            # Validate data
            validation = self._validate_data(data)
            
            return {
                'success': validation['valid'],
                'message': f'Successfully extracted {len(data)} indicators' if validation['valid'] else 'Data validation failed',
                'selector_name': selector_name,
                'selector': selector,
                'version': version,
                'rows_found': len(rows),
                'data': data,
                'validation': validation
            }
            
        except Exception as e:
            logger.error(f"Scraping error: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'data': []
            }
    
    def test_selector(self, selector, version):
        """
        Test if a selector finds elements without extracting data
        
        Args:
            selector (str): CSS selector to test
            version (str): Version to test against
            
        Returns:
            dict: Test results
        """
        try:
            html_content = self._load_html(version)
            
            if not html_content:
                return {
                    'success': False,
                    'found': False,
                    'count': 0,
                    'error': f'Could not load HTML for {version}'
                }
            
            soup = BeautifulSoup(html_content, 'html.parser')
            elements = soup.select(selector)
            
            return {
                'success': True,
                'found': len(elements) > 0,
                'count': len(elements),
                'selector': selector,
                'version': version
            }
            
        except Exception as e:
            logger.error(f"Test selector error: {str(e)}")
            return {
                'success': False,
                'found': False,
                'count': 0,
                'error': str(e)
            }
    
    def validate_data(self, data):
        """
        Validate extracted data
        
        Args:
            data (list): Extracted data to validate
            
        Returns:
            dict: Validation results
        """
        return self._validate_data(data)
    
    def _load_html(self, version):
        """
        Load HTML file for specified version
        
        Args:
            version (str): v1, v2, or v3
            
        Returns:
            str: HTML content or None
        """
        filename_map = {
            'v1': 'website_sample_v1.html',
            'v2': 'website_sample_v2.html',
            'v3': 'website_sample_v3.html'
        }
        
        if version not in filename_map:
            logger.error(f"Invalid version: {version}")
            return None
        
        filepath = os.path.join(self.data_path, filename_map[version])
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            logger.error(f"Error loading HTML: {str(e)}")
            return None
    
    def _parse_rows(self, rows):
        """
        Parse table rows into structured data
        
        Args:
            rows: BeautifulSoup ResultSet of table rows
            
        Returns:
            list: Extracted data
        """
        data = []
        
        for row in rows:
            try:
                cells = row.find_all('td')
                
                if len(cells) >= 4:
                    indicator = {
                        'name': cells[0].get_text(strip=True),
                        'value': cells[1].get_text(strip=True),
                        'change': cells[2].get_text(strip=True),
                        'period': cells[3].get_text(strip=True),
                        'code': row.get('data-indicator-code', 'UNKNOWN')
                    }
                    
                    # Only add if we got meaningful data
                    if indicator['name'] and indicator['value']:
                        data.append(indicator)
                        
            except Exception as e:
                logger.warning(f"Error parsing row: {str(e)}")
                continue
        
        return data
    
    def _validate_data(self, data):
        """
        Validate extracted data meets quality standards
        
        Args:
            data (list): Data to validate
            
        Returns:
            dict: Validation results with detailed checks
        """
        checks = {
            'has_data': len(data) > 0,
            'has_minimum_rows': len(data) >= 8,
            'all_fields_present': True,
            'valid_names': True
        }
        
        issues = []
        
        # Check 1: Has data
        if not checks['has_data']:
            issues.append('No data extracted')
        
        # Check 2: Minimum rows
        if not checks['has_minimum_rows']:
            issues.append(f'Expected at least 8 rows, got {len(data)}')
        
        # Check 3: All fields present
        required_fields = ['name', 'value', 'change', 'period']
        for i, item in enumerate(data):
            for field in required_fields:
                if field not in item or not item[field]:
                    checks['all_fields_present'] = False
                    issues.append(f'Row {i} missing field: {field}')
                    break
        
        # Check 4: Valid names
        for item in data:
            if len(item.get('name', '')) < 3:
                checks['valid_names'] = False
                issues.append(f'Invalid name: {item.get("name", "empty")}')
                break
        
        # Overall validation
        all_valid = all(checks.values())
        
        return {
            'valid': all_valid,
            'checks': checks,
            'issues': issues,
            'row_count': len(data),
            'message': 'All validation checks passed' if all_valid else f'{len(issues)} validation issues found'
        }