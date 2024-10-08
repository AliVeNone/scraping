import os
import httpx
import time
import logging
import yaml
from bs4 import BeautifulSoup

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

# Extract product data
def extract_product_data(product, selectors):
    try:
        name = product.find('span', class_=selectors['product_name']).text
        brand = product.find('span', class_=selectors['product_brand']).text
        price = product.find('span', class_=selectors['product_price']).text.strip()
        return f'Brand: {brand}, Name: {name}, Price: {price}'
    except Exception as e:
        logging.error(f"Error extracting product data: {e}")
        return None

# Scrape a specific page
def scrape_page(url, page_number, selectors, output_mode, output_file):
    try:
        response = httpx.get(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses

        # Debug: Print the HTML response to verify content
        print(f"Response HTML for page {page_number}:\n", response.text)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all products on the page
        products = soup.find_all('div', class_=selectors['product_box'])
        print(f"Number of products found on page {page_number}: {len(products)}")

        # Collect product data
        output_lines = []
        for product in products:
            product_data = extract_product_data(product, selectors)
            if product_data:
                output_lines.append(product_data)

        # Print to console if needed
        if output_mode in ['console', 'both']:
            for line in output_lines:
                print(line)

        # Write to file if needed
        if output_mode in ['file', 'both']:
            with open(output_file, 'a') as file:
                for line in output_lines:
                    file.write(f"{line}\n")

    except httpx.HTTPError as e:
        logging.error(f"HTTP error while accessing page {page_number}: {e}")

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

    # Scrape the pages
    for page_number in range(1, max_pages + 1):
        page_url = f'{base_url}?page={page_number}'
        logging.info(f"Scraping page {page_number} from URL: {page_url}")
        scrape_page(page_url, page_number, selectors, output_mode, output_file)
        time.sleep(wait_time)

# Entry point
if __name__ == '__main__':
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    main()
