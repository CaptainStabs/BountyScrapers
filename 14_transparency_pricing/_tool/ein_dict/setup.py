from setuptools import setup

setup(
  name="ein_dict",
  version="1.0.0",
  scripts=["ein_dict_maker.py"],
  entry_points = '''
        [console_scripts]
        ein_dict=ein_dict_maker:cli
  '''
)
