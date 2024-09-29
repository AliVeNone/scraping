import unittest
from bs4 import BeautifulSoup
from scraper.scraper import extract_product_data

class TestScraper(unittest.TestCase):
    def test_extract_product_data(self):
        # Sample HTML content to simulate a product element
        product_html = '''
        <div class="s-productthumbbox">
            <span class="productdescriptionname">Hoodie Name</span>
            <span class="productdescriptionbrand">Brand Name</span>
            <span class="CurrencySizeLarge curprice">£29.99</span>
        </div>
        '''
        product_soup = BeautifulSoup(product_html, 'html.parser')
        
        try:
            extract_product_data(product_soup)  # Should print out the product info
        except Exception as e:
            self.fail(f"extract_product_data raised an exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
