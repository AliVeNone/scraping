from setuptools import setup, find_packages

setup(
    name='Baigiamasis',
    version='0.1.0',
    description='A web scraper project for scraping dynamic and static pages',
    author='Alina Venckute',
    author_email='alina@gmail.com',
    packages=find_packages(),  # Automatically find and include all packages
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        'httpx',
        'beautifulsoup4',
        'selenium',
        'webdriver-manager',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'run_scraper=scraper.scraper:main',
            'run_selenium_scraper=scraper.selenium_scraper:main',
        ],
    },
)
