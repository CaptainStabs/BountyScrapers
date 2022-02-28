from quantulum3 import parser

# quants = parser.inline_parse("PEN G BENZATHINE/PROCAINE/100KU INJ")
# print(quants)
# print()
#
# print(parser.inline_parse("LOCM IODINE 300-399MG/ML"))
# quants = parser.parse("LOCM IODINE 300-399MG/ML")
# print(quants)
# print()
desc = "340B BUTORPHAN TART/4MG 10ML INJ"
quants = parser.parse("340B BUTORPHAN TART/4MG 10ML INJ")
# print(parser.inline_parse("340B BUTORPHAN TART/1MG INJ"), "\n")
# print([x.unit for x in quants], "\n")
# print(dir(quants[0]))
# print()

# if "MG/ML"
qs = quants
quant = [x for x in quants if x.unit.entity.name=="mass" or x.unit.entity.name=="concentration" or x.unit.entity.name=="volume"]

if len(quant):
    units = " ".join([(str(q.value) + str(q.unit.symbols[-1])) for q in quant if q.unit.symbols]) + " " + str(desc.split(" ")[-1])
    # s = [q.unit.symbols for q in quant if q.unit.symbols]
    print(units)
        # units = quant[0].unit.symbols
    # if units:
    #     print(str(quant[0].value) + str(units[0]).upper())
print(qs, "\n")
print(dir(qs))
