from static import *

def stringPassesLeadingTrailingSpaceCheck(s):
    if s == "":
        return False
    stripped = s.strip()
    return stripped == s

def stringIsUppercase(s):
    return s.upper() == s

def validateString(colName, value):
    formatted = value.strip().upper()
    for char in invalid_chars:
        formatted = formatted.replace(char, " ").replace("  ", " ")
    if formatted != value:
        print(f'UPDATE menu_items SET {colName!r} = {formatted!r} WHERE restaurant_name = {value!r}')
        print(f'DELETE FROM menu_items WHERE {colName!r} = {value!r}')
