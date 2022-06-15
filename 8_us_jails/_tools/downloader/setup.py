from setuptools import setup

setup(
  name="downloader",
  version="1.0.0",
  scripts=["downloader.py"],
  entry_points = '''
        [console_scripts]
        downloader=downloader:cli
  '''
)
