import pytest
from selenium.common.exceptions import NoSuchElementException
from scraper.selenium_scraper import scrape_page

def test_scrape_page(chrome_driver):
    # Navigate to the sample page for testing
    chrome_driver.get('https://www.houseoffraser.co.uk/men/hoodies-and-sweatshirts')
    
    # Testing the page scrape functionality
    try:
        scrape_page(chrome_driver, chrome_driver.current_url, 1, {
            'product_box': 'div.s-productthumbbox',
            'product_name': 'span.productdescriptionname',
            'product_brand': 'span.productdescriptionbrand',
            'product_price': 'span.CurrencySizeLarge.curprice',
        }, 'console', 'output.txt')
    except NoSuchElementException:
        pytest.fail("scrape_page raised NoSuchElementException unexpectedly")

