from setuptools import setup

setup(
  name="index_sorter",
  version="1.0.0",
  scripts=["index_sorter_cli.py"],
  entry_points = '''
        [console_scripts]
        index_sorter=index_sorter_cli:cli
  '''
)
