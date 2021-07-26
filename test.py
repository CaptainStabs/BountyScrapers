import re
test_string = '12\" Spaniko Pizza'
result = re.sub(r'(.*)([0-9]{2})(.{0,1}")(.*)', '\g<2>', test_string)
# if result:
#     cleaned_string = test_string.replace()
print(result)
