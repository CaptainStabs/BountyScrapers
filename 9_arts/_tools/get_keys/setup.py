from setuptools import setup

setup(
  name="get_keys",
  version="1.0.0",
  scripts=["get_keys.py"],
  entry_points = '''
        [console_scripts]
        get_keys=get_keys:cli
  '''
)
