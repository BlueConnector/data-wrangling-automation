"""
Exercise 2 Solution: Product Data Scraping from E-commerce Sites

This solution demonstrates scraping product data (name, price, SKU) from
e-commerce websites like Fairprice, with features beyond the basic table scraper:

1. Live URL support (https://) using Playwright for JavaScript-rendered content
2. Field-type aware selectors (product_card, product_name, price, sku)
3. Attribute extraction (@href notation for SKU from URLs)
4. Product card iteration (not table rows)
5. Fallback selectors per field type
"""

from playwright.sync_api import sync_playwright
import pandas as pd
import logging
import re
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


class ProductScraper:
    """A web scraper for extracting product data from e-commerce sites"""

    def __init__(self, page, selectors_df):
        """
        Initialize the scraper with a Playwright page and selector configuration

        Args:
            page: Playwright page object (browser page)
            selectors_df: DataFrame containing selector configurations for this URL
        """
        self.page = page
        self.selectors_df = selectors_df
        self.products = []

    def extract_products(self):
        """
        Extract products using field-type aware selectors from configuration

        Returns:
            list: List of dictionaries containing product data (name, price, sku)
        """
        # Step 1: Find all product cards using product_card selectors
        product_elements = self._find_product_cards()

        if not product_elements:
            raise Exception("No product cards found with any selector strategy")

        logging.info(f"Found {len(product_elements)} product cards")

        # Step 2: For each product card, extract name, price, and SKU
        for i, card in enumerate(product_elements):
            try:
                product = self._extract_product_data(card, i)
                if product and product.get('name'):
                    self.products.append(product)
            except Exception as e:
                logging.warning(f"Failed to extract product {i}: {e}")
                continue

        logging.info(f"Successfully extracted {len(self.products)} products")
        return self.products

    def _find_product_cards(self):
        """
        Find all product card elements using fallback selectors

        Returns:
            list: List of Playwright ElementHandle objects
        """
        card_selectors = self.selectors_df[
            (self.selectors_df['field_type'] == 'product_card') &
            (self.selectors_df['enabled'].astype(str).str.lower() == 'true')
        ].sort_values('priority')

        for _, row in card_selectors.iterrows():
            selector = row['selector']
            selector_name = row['selector_name']

            try:
                logging.info(f"Trying product card selector: {selector_name}")

                # Handle @attribute notation (strip it for card finding)
                css_selector = selector.split('@')[0] if '@' in selector else selector

                elements = self.page.query_selector_all(css_selector)

                if elements and len(elements) > 0:
                    logging.info(f"✓ {selector_name} found {len(elements)} cards")
                    return elements
                else:
                    logging.warning(f"✗ {selector_name} found no cards")

            except Exception as e:
                logging.warning(f"✗ {selector_name} failed: {e}")
                continue

        return []

    def _extract_product_data(self, card_element, index):
        """
        Extract name, price, and SKU from a single product card

        Args:
            card_element: Playwright ElementHandle for the product card
            index: Product index for logging

        Returns:
            dict: Product data with name, price, sku fields
        """
        product = {
            'name': None,
            'price': None,
            'sku': None
        }

        # Extract product name
        product['name'] = self._extract_field(card_element, 'product_name')

        # Extract price
        product['price'] = self._extract_field(card_element, 'price')

        # Extract SKU (may come from href attribute)
        product['sku'] = self._extract_field(card_element, 'sku')

        return product

    def _extract_field(self, card_element, field_type):
        """
        Extract a specific field using fallback selectors

        Args:
            card_element: Playwright ElementHandle for the product card
            field_type: Type of field to extract (product_name, price, sku)

        Returns:
            str: Extracted value or None
        """
        # Special case: SKU extraction - try to get href directly first
        if field_type == 'sku':
            try:
                href = card_element.get_attribute('href')
                if href:
                    sku = self._extract_sku_from_url(href)
                    if sku:
                        return sku
            except Exception:
                pass

        field_selectors = self.selectors_df[
            (self.selectors_df['field_type'] == field_type) &
            (self.selectors_df['enabled'].astype(str).str.lower() == 'true')
        ].sort_values('priority')

        for _, row in field_selectors.iterrows():
            selector = row['selector']

            try:
                value = self._extract_with_selector(card_element, selector, field_type)
                if value:
                    return value
            except Exception:
                continue

        return None

    def _extract_with_selector(self, element, selector, field_type):
        """
        Extract data using a selector, supporting @attribute notation
        Uses smart parsing based on field type

        Args:
            element: Playwright ElementHandle to search within
            selector: CSS selector, optionally with @attribute suffix
            field_type: Type of field being extracted

        Returns:
            str: Extracted value
        """
        # Check for @attribute notation (e.g., "a[href*='/product/']@href")
        if '@' in selector:
            selector_part, attr = selector.rsplit('@', 1)

            # For product cards that ARE the link, get attribute directly
            try:
                matches = element.evaluate(f'el => el.matches("{selector_part}")')
            except Exception:
                matches = False

            if matches:
                value = element.get_attribute(attr)
            else:
                # Find nested element and get attribute
                target = element.query_selector(selector_part)
                if not target:
                    return None
                value = target.get_attribute(attr)

            # Special handling for SKU extraction from href
            if attr == 'href' and value and field_type == 'sku':
                return self._extract_sku_from_url(value)

            return value

        # Field-specific text extraction with smart parsing
        if field_type == 'product_name':
            return self._extract_product_name(element, selector)
        elif field_type == 'price':
            return self._extract_price(element, selector)
        else:
            # Generic text extraction
            target = element.query_selector(selector)
            if target:
                return target.text_content().strip()
            return None

    def _extract_product_name(self, element, selector):
        """
        Extract product name with smart parsing to filter out prices, ratings, etc.
        Handles text that may be concatenated without newlines.
        """
        text = element.text_content()
        if not text:
            return None

        # The text is often concatenated like:
        # "Save $0.26$5.95$6.21AdMission Wholemeal Wraps - Protein360g4.3(11)add to cartAdd to cart"
        # We need to extract just the product name part

        # Strategy: Find the product name directly using pattern matching
        # Product names typically: start with brand (capitalized), include product type, end with weight

        # Pattern to find: [Brand Name] [Product Description] [Weight]
        # Where brand starts with capital letter after any price patterns

        # Look for pattern: letter followed by words, then weight
        # This captures: "AdMission Wholemeal Wraps - Protein360g" or "Gardenia Enriched White Bread600g"
        match = re.search(
            r'([A-Z][a-zA-Z]+(?:\s+[a-zA-Z&\-]+)*(?:\s*-\s*[a-zA-Z&\s]+)?)\s*(\d+\s*(?:g|kg|ml|L|pcs|per pack|pack))',
            text,
            re.IGNORECASE
        )

        if match:
            brand_and_product = match.group(1).strip()
            weight = match.group(2).strip()

            # Ensure space before weight
            name = f"{brand_and_product} {weight}"

            # Clean up any bullet certifications that got included
            name = re.sub(r'•.*$', '', name).strip()
            return name

        # Alternative: try to find brand name pattern without weight
        # For products like "AdMission Mini Wraps - Original 8 per pack"
        match = re.search(
            r'([A-Z][a-zA-Z]+(?:\s+[a-zA-Z&\-]+)*(?:\s*-\s*[a-zA-Z&\s]+)?)\s*(\d+\s*per pack)',
            text,
            re.IGNORECASE
        )

        if match:
            name = f"{match.group(1).strip()} {match.group(2).strip()}"
            return name

        # Fallback: find any capitalized brand name followed by description
        match = re.search(r'([A-Z][a-zA-Z]+(?:\s+[a-zA-Z&\-\']+){2,})', text)
        if match:
            name = match.group(1).strip()
            # Try to append weight if found nearby
            weight_match = re.search(r'(\d+\s*(?:g|kg|ml|L))', text)
            if weight_match:
                name = f"{name} {weight_match.group(1)}"
            return name

        # Last resort: return cleaned text up to rating or "add to cart"
        match = re.match(r'^(.*?)(\d+\.\d+\(|add to cart)', text, re.IGNORECASE)
        if match:
            text = match.group(1)

        # Clean up
        text = re.sub(r'^[Ss]ave\s*', '', text)
        text = re.sub(r'\$[\d.]+', '', text)
        text = re.sub(r'•.*$', '', text)
        return text.strip()[:100] if text.strip() else None

    def _extract_price(self, element, selector):
        """
        Extract the actual selling price (not savings or original price)

        Text patterns we see:
        - "$3.20" (simple price)
        - "Save $0.26$5.95$6.21" (savings, sale price, original price)

        We want the SALE price (first price after "Save $X.XX") or the only price
        """
        text = element.text_content()
        if not text:
            return None

        # Find all prices in the text
        all_prices = re.findall(r'\$(\d+\.?\d*)', text)

        if not all_prices:
            return None

        # Check if there's a "Save" pattern
        if 'Save' in text or 'save' in text:
            # Pattern: "Save $0.26$5.95$6.21"
            # prices[0] = savings amount (0.26)
            # prices[1] = sale price (5.95) <- we want this
            # prices[2] = original price (6.21)
            if len(all_prices) >= 2:
                return f"${all_prices[1]}"
            elif len(all_prices) == 1:
                # Only savings shown, no actual price found
                return None
        else:
            # No discount, first price is the actual price
            return f"${all_prices[0]}"

        return None

    def _extract_sku_from_url(self, url):
        """
        Extract SKU/product ID from a product URL

        Examples:
            /product/gardenia-bread-600g-13088637 -> 13088637
            /product/m-protein-wrap-wm360-13251697 -> 13251697
            /product/13251697 -> 13251697

        Args:
            url: Product URL string

        Returns:
            str: Extracted SKU or None
        """
        if not url:
            return None

        # Get the last segment of the URL path
        # e.g., /product/gardenia-bread-600g-13088637 -> gardenia-bread-600g-13088637
        path = url.rstrip('/').split('/')[-1]

        # Remove query parameters if any
        path = path.split('?')[0]

        # Pattern 1: SKU is the last hyphen-separated segment (most common)
        # e.g., "gardenia-bread-600g-13088637" -> "13088637"
        parts = path.split('-')
        for part in reversed(parts):
            # SKU is typically 6-10 digits
            if part.isdigit() and len(part) >= 5:
                return part

        # Pattern 2: Entire path is just the SKU
        if path.isdigit():
            return path

        # Pattern 3: Find any long number sequence at the end
        match = re.search(r'(\d{5,})$', path)
        if match:
            return match.group(1)

        # Pattern 4: Find number sequence anywhere (less reliable)
        match = re.search(r'(\d{6,})', path)
        if match:
            return match.group(1)

        return None

    def validate_products(self):
        """
        Validate that the extracted products meet quality standards

        Returns:
            bool: True if validation passes
        """
        if not self.products:
            logging.error("Validation failed: No products extracted")
            return False

        # Check that we have at least some products
        if len(self.products) < 5:
            logging.warning(f"Only {len(self.products)} products found - may be incomplete")

        # Check that products have names
        products_with_names = sum(1 for p in self.products if p.get('name'))
        if products_with_names < len(self.products) * 0.8:
            logging.error("Validation failed: Too many products missing names")
            return False

        # Check that we got some prices
        products_with_prices = sum(1 for p in self.products if p.get('price'))
        if products_with_prices < len(self.products) * 0.5:
            logging.warning("Many products missing prices - selector may need adjustment")

        logging.info(f"✓ Validation passed: {len(self.products)} products, "
                    f"{products_with_names} with names, {products_with_prices} with prices")
        return True

    def display_results(self):
        """Display the extracted products in a readable format"""
        if not self.products:
            print("No products to display")
            return

        print(f"\n{'='*80}")
        print(f"Extracted {len(self.products)} products:")
        print(f"{'='*80}")

        for i, product in enumerate(self.products[:10], 1):  # Show first 10
            print(f"\n{i}. {product.get('name', 'Unknown')}")
            print(f"   Price: {product.get('price', 'N/A')}")
            print(f"   SKU: {product.get('sku', 'N/A')}")

        if len(self.products) > 10:
            print(f"\n... and {len(self.products) - 10} more products")

        print(f"\n{'='*80}\n")


def load_complex_selectors(config_file='data/complex_selectors.csv'):
    """
    Load selector configuration from the complex selectors CSV file

    Args:
        config_file (str): Path to the complex selectors CSV file

    Returns:
        DataFrame: Selector configuration with field_type column
    """
    try:
        selectors_df = pd.read_csv(config_file)

        # Validate required columns (includes field_type)
        required_columns = ['url', 'selector_name', 'selector', 'priority', 'enabled', 'field_type']
        missing_columns = [col for col in required_columns if col not in selectors_df.columns]

        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")

        print(f"✓ Loaded {len(selectors_df)} selector configurations from {config_file}")

        # Show summary by field type
        field_counts = selectors_df.groupby('field_type').size()
        print(f"\n📊 Selectors by field type:")
        for field_type, count in field_counts.items():
            print(f"   • {field_type}: {count} selectors")

        return selectors_df

    except FileNotFoundError:
        print(f"✗ Error: Configuration file not found: {config_file}")
        return None
    except Exception as e:
        print(f"✗ Error loading configuration: {str(e)}")
        return None


def scrape_products(url, selectors_df, headless=True, wait_time=3):
    """
    Scrape products from a live URL using Playwright

    Args:
        url: URL to scrape (supports https://)
        selectors_df: DataFrame with selectors for this URL
        headless: Run browser in headless mode
        wait_time: Seconds to wait for page to load

    Returns:
        list: Extracted products
    """
    print(f"\n{'='*80}")
    print(f"Scraping: {url}")
    print(f"{'='*80}")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)

        # Create context with realistic viewport and user agent
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )

        page = context.new_page()

        try:
            # Navigate to URL
            logging.info(f"Navigating to {url}")
            page.goto(url, wait_until='domcontentloaded', timeout=60000)

            # Wait for content to load (JavaScript-heavy sites need more time)
            logging.info(f"Waiting {wait_time}s for dynamic content...")
            time.sleep(wait_time)

            # Try to wait for product elements to appear
            try:
                page.wait_for_selector('a[href*="/product/"]', timeout=10000)
                logging.info("Product elements detected")
            except Exception:
                logging.warning("Product selector wait timed out, continuing anyway...")

            # Scroll to load lazy-loaded content
            logging.info("Scrolling to load more products...")
            page.evaluate('window.scrollTo(0, document.body.scrollHeight / 2)')
            time.sleep(1)

            # Get selectors for this URL
            url_selectors = selectors_df[selectors_df['url'] == url]

            if url_selectors.empty:
                raise Exception(f"No selectors configured for {url}")

            logging.info(f"Using {len(url_selectors)} selectors for this URL")

            # Create scraper and extract products
            scraper = ProductScraper(page, url_selectors)
            products = scraper.extract_products()

            # Validate and display
            scraper.validate_products()
            scraper.display_results()

            return products

        except Exception as e:
            logging.error(f"Scraping failed: {e}")
            raise
        finally:
            context.close()
            browser.close()


def test_product_scraper():
    """
    Test the product scraper against configured URLs
    """
    # Load complex selectors
    selectors_df = load_complex_selectors('data/complex_selectors.csv')

    if selectors_df is None:
        print("Cannot proceed without selector configuration")
        return

    # Get unique URLs
    urls = selectors_df['url'].unique()
    print(f"\n✓ Found {len(urls)} URLs to scrape")

    results = []

    for url in urls:
        try:
            products = scrape_products(url, selectors_df, headless=True)
            results.append({
                'url': url,
                'status': 'SUCCESS',
                'count': len(products)
            })
        except Exception as e:
            logging.error(f"Failed to scrape {url}: {e}")
            results.append({
                'url': url,
                'status': f'FAILED: {str(e)}',
                'count': 0
            })

    # Summary
    print("\n" + "="*80)
    print("SCRAPING SUMMARY")
    print("="*80)
    for result in results:
        status_symbol = "✓" if result['status'] == 'SUCCESS' else "✗"
        print(f"{status_symbol} {result['url']}")
        print(f"   Status: {result['status']}")
        if result['count'] > 0:
            print(f"   Products: {result['count']}")
    print("="*80)


def demonstrate_differences():
    """
    Show the key differences between this scraper and the basic table scraper
    """
    print("\n" + "="*80)
    print("PRODUCT SCRAPER vs TABLE SCRAPER")
    print("="*80)

    print("""
┌─────────────────────┬────────────────────────┬────────────────────────┐
│ Feature             │ Table Scraper (Ex 1)   │ Product Scraper (Ex 2) │
├─────────────────────┼────────────────────────┼────────────────────────┤
│ Data Source         │ Local HTML files       │ Live URLs (https://)   │
│ HTML Structure      │ Table rows (<tr>)      │ Product cards (<div>)  │
│ Output Fields       │ indicator, value,      │ name, price, sku       │
│                     │ change, period         │                        │
│ Selector File       │ selectors.csv          │ complex_selectors.csv  │
│ Field Type Column   │ No                     │ Yes (field_type)       │
│ Attribute Extract   │ No                     │ Yes (@href notation)   │
│ JavaScript Support  │ Limited                │ Full (Playwright)      │
│ Use Case            │ Government statistics  │ E-commerce products    │
└─────────────────────┴────────────────────────┴────────────────────────┘

OUTPUT FORMAT COMPARISON:

Table Scraper Output:
{
    "indicator": "Gross Domestic Product",
    "value": "542,300M",
    "change": "+0.78",
    "period": "Oct 2024",
    "code": "GDP"
}

Product Scraper Output:
{
    "name": "Gardenia Enriched White Bread 600g",
    "price": "$2.50",
    "sku": "13088637"
}
    """)
    print("="*80 + "\n")


if __name__ == "__main__":
    print("="*80)
    print("Exercise 2 Solution: Product Data Scraping")
    print("="*80)
    print("\nThis solution demonstrates scraping product data from e-commerce sites.")
    print("Selectors are loaded from data/complex_selectors.csv")
    print("Supports live URLs, field types, and attribute extraction!\n")

    # Show differences from basic scraper
    demonstrate_differences()

    # Run the scraper
    test_product_scraper()

    print("\n" + "="*80)
    print("Exercise Complete!")
    print("="*80)
    print("\nKey Features Demonstrated:")
    print("1. Live URL scraping with Playwright")
    print("2. Field-type aware selectors (product_card, name, price, sku)")
    print("3. Attribute extraction (@href for SKU)")
    print("4. Product card iteration (not table rows)")
    print("5. Separate config file (complex_selectors.csv)")
