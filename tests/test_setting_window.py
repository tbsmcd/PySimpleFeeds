import pytest
from ..setting_window import SettingWindow


def test_validate_styles_are_same_error():
    values = {
        '-DB-': True,
        '-LG-': True,
        '-ROWS-': '1',
        '-LENGTH-': '1',
        '-NAME_0-': 'a', '-LINK_0-': 'a', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    assert 'Choose one of the themes.' in SettingWindow.validate(values)


def test_validate_styles_are_not_bool():
    values = {
        '-DB-': '',
        '-LG-': True,
        '-ROWS-': '1',
        '-LENGTH-': '1',
        '-NAME_0-': 'a', '-LINK_0-': 'a', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    assert 'Choose one of the themes.' in SettingWindow.validate(values)
    values['-DB-'] = True
    values['-LG-'] = ''
    assert 'Choose one of the themes.' in SettingWindow.validate(values)


def test_validate_row_and_length_are_not_numeric_error():
    values = {
        '-DB-': False,
        '-LG-': True,
        '-ROWS-': '1a',
        '-LENGTH-': '0',
        '-NAME_0-': 'a', '-LINK_0-': 'a', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    assert '"Rows" must be a number.' in SettingWindow.validate(values)
    assert '"Length" must be a number.' in SettingWindow.validate(values)


def test_validate_name_is_only_blank_error():
    values = {
        '-DB-': False,
        '-LG-': True,
        '-ROWS-': '1',
        '-LENGTH-': '1',
        '-NAME_0-': '', '-LINK_0-': 'a', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    assert '0: Only one of the name and link should not be blank.' in SettingWindow.validate(values)


def test_validate_link_is_only_blank_error():
    values = {
        '-DB-': False,
        '-LG-': True,
        '-ROWS-': '1',
        '-LENGTH-': '1',
        '-NAME_0-': 'a', '-LINK_0-': '', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    assert '0: Only one of the name and link should not be blank.' in SettingWindow.validate(values)