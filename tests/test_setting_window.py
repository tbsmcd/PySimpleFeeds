import pytest
from ..setting_window import SettingWindow


def provide_values(params={}):
    values = {
        '-DB-': True,
        '-LG-': False,
        '-ROWS-': '1',
        '-LENGTH-': '1',
        '-NAME_0-': 'a', '-LINK_0-': 'a', '-NAME_1-': 'a', '-LINK_1-': 'a', '-NAME_2-': 'a', '-LINK_2-': 'a',
        '-NAME_3-': 'a', '-LINK_3-': 'a', '-NAME_4-': 'a', '-LINK_4-': 'a', '-NAME_5-': 'a', '-LINK_5-': 'a',
    }
    values.update(params)
    return values


def test_validate_with_collect_values_success():
    values = provide_values()
    assert len(SettingWindow.validate(values)) == 0


def test_validate_styles_are_same_error():
    values = provide_values({'-LG-': True})
    assert 'Choose one of the themes.' in SettingWindow.validate(values)


def test_validate_styles_are_not_bool_error():
    values = provide_values({'-DB-': ''})
    assert 'Choose one of the themes.' in SettingWindow.validate(values)
    values['-DB-'] = True
    values['-LG-'] = ''
    assert 'Choose one of the themes.' in SettingWindow.validate(values)


def test_validate_row_and_length_are_not_numeric_error():
    values = provide_values({'-ROWS-': '1a', '-LENGTH-': 'ss'})
    assert '"Rows" must be a number.' in SettingWindow.validate(values)
    assert '"Length" must be a number.' in SettingWindow.validate(values)


def test_validate_name_is_only_blank_error():
    values = provide_values({'-NAME_0-': ''})
    assert '0: Only one of the name and link should not be blank.' in SettingWindow.validate(values)


def test_validate_link_is_only_blank_error():
    values = provide_values({'-LINK_0-': ''})
    assert '0: Only one of the name and link should not be blank.' in SettingWindow.validate(values)