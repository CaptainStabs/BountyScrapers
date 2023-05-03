from setuptools import setup

setup(
  name="importer",
  version="1.0.0",
  scripts=["importer_script.py"],
  entry_points = '''
        [console_scripts]
        importer=importer_script:cli
  '''
)
