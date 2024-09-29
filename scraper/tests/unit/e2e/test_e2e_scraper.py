import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from scraper.selenium_scraper import main
import os

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    yield driver
    driver.quit()

def test_e2e_scraper(driver):
    # Run the scraper
    try:
        main()
    except Exception as e:
        pytest.fail(f"End-to-end test failed: {e}")

    # Verify that output.txt is created and contains data
    assert os.path.exists('output.txt'), "Output file was not created."

    with open('output.txt', 'r') as f:
        data = f.read()
        assert len(data) > 0, "Output file is empty, expected scraped data."

    # Additional verification: check if driver navigates correctly
    driver.get('https://www.houseoffraser.co.uk/men/hoodies-and-sweatshirts')
    assert "House of Fraser" in driver.title, "Browser did not navigate to the correct URL."
