from setuptools import setup

setup(
  name="address_scraper",
  version="1.0.0",
  scripts=["address_scraping.py"],
  entry_points = '''
        [console_scripts]
        address_scraper=address_scraping:cli
  '''
)
