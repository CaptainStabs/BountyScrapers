from pytest import *
from strings import *

def test_leading_trailing_spaces():
    assert stringPassesLeadingTrailingSpaceCheck("thisisvalid") == True
    assert stringPassesLeadingTrailingSpaceCheck("THISISVALID") == True
    assert stringPassesLeadingTrailingSpaceCheck(" NOTVALID") == False
    assert stringPassesLeadingTrailingSpaceCheck(" NOTVALID ") == False
    assert stringPassesLeadingTrailingSpaceCheck("12345! ") == False

def test_string_uppercase():
    assert stringIsUppercase("MENUITEM") is True
    assert stringIsUppercase("Menuitem") is False
    assert stringIsUppercase("menuitem") is False
    assert stringIsUppercase("menu item") is False
    assert stringIsUppercase("MCDONALD'S") is True
    assert stringIsUppercase("MCDONALD'S issogood") is False
    assert stringIsUppercase("Mcdonald's") is False