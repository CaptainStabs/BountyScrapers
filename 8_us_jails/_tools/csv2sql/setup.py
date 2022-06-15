from setuptools import setup

setup(
  name="csv2sql",
  version="1.0.0",
  scripts=["csv_to_sql.py"],
  entry_points = '''
        [console_scripts]
        csv2sql=csv_to_sql:cli
  '''
)
