from setuptools import setup

setup(
  name="cell_counter",
  version="1.0.0",
  scripts=["cell_counter_single_v2.py"],
  entry_points = '''
        [console_scripts]
        cell_counter=cell_counter_single_v2:cli
  '''
)
