from dateutil import parser

print(parser.parse('1991-12-26'))

print(str('                    $20,500.00').strip().replace("$", "").replace(",", "").split(".")[0])
