from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time
import logging
import yaml

# Load configuration from config.yaml
def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

# Setup logging
def setup_logging(log_level, log_file='logs/main.log'):
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# Scrape page using Selenium
def scrape_page(driver, url, page_number, selectors, output_mode, output_file):
    try:
        driver.get(url)
        time.sleep(5)  # Wait for JavaScript to load

        products = driver.find_elements(By.CSS_SELECTOR, selectors['product_box'])
        print(f"Number of products found on page {page_number}: {len(products)}")

        output_lines = []
        for product in products:
            try:
                name = product.find_element(By.CSS_SELECTOR, selectors['product_name']).text
                brand = product.find_element(By.CSS_SELECTOR, selectors['product_brand']).text
                price = product.find_element(By.CSS_SELECTOR, selectors['product_price']).text.strip()
                output_lines.append(f'Brand: {brand}, Name: {name}, Price: {price}')
            except Exception as e:
                logging.error(f"Error extracting product data: {e}")

        # Print to console if needed
        if output_mode in ['console', 'both']:
            for line in output_lines:
                print(line)

        # Write to file if needed
        if output_mode in ['file', 'both']:
            with open(output_file, 'a') as file:
                for line in output_lines:
                    file.write(f"{line}\n")

    except Exception as e:
        logging.error(f"Error while scraping page {page_number}: {e}")

# Main function
def main():
    config = load_config()
    setup_logging(config['logging_level'])

    base_url = config['url']
    selectors = config['selectors']
    output_mode = config['output_mode']
    output_file = config['output_file']
    max_pages = config['max_pages']
    wait_time = config['wait_time']

    # Clear the output file before starting a new run
    if output_mode in ['file', 'both']:
        with open(output_file, 'w') as file:
            file.write("")  # Clear the file content

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    # Scrape the pages
    for page_number in range(1, max_pages + 1):
        page_url = f'{base_url}?page={page_number}'
        logging.info(f"Scraping page {page_number} from URL: {page_url}")
        scrape_page(driver, page_url, page_number, selectors, output_mode, output_file)
        time.sleep(wait_time)

    driver.quit()

# Entry point
if __name__ == '__main__':
    main()
