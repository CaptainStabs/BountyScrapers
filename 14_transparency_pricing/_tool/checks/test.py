from frictionless import validate
import yaml

report = validate('rate.schema.yaml')

print(report)