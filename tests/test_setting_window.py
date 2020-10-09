import os
import pytest
from ..setting_window import SettingWindow


def provide_values(params={}):
    values = {
        '-DB-': True,
        '-LG-': False,
        '-ROWS-': '6',
        '-LENGTH-': '20',
        '-NAME_0-': 'a', '-LINK_0-': 'https://a', '-NAME_1-': 'b', '-LINK_1-': 'https://b',
        '-NAME_2-': 'c', '-LINK_2-': 'https://c', '-NAME_3-': 'd', '-LINK_3-': 'https://d',
        '-NAME_4-': 'e', '-LINK_4-': 'https://e', '-NAME_5-': 'f', '-LINK_5-': 'https://f',
    }
    values.update(params)
    return values


# validate()
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


# save()
def test_save_with_collect_style_success(tmpdir):
    tmpfile = tmpdir.join('settings.yml')
    values = provide_values()
    SettingWindow.save(values, tmpfile)
    with tmpfile.open('r') as f:
        yml = f.readlines()
    assert yml[0].strip() == 'feeds:'
    assert yml[1].strip() == '- link: https://a'
    assert yml[2].strip() == 'name: a'
    assert yml[13].strip() == 'length: 20'
    assert yml[14].strip() == 'rows: 6'
    assert yml[15].strip() == 'theme: DarkBlack'
    os.remove(tmpfile)
