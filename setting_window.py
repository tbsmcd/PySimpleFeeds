import PySimpleGUI as sg
import yaml
import re


class SettingWindow:
    LABEL_LEN = 14

    def __init__(self):
        with open('settings.yml') as file:
            self.__config = yaml.safe_load(file.read())

    @staticmethod
    def validate(values):
        messages = []
        if not (values['-DB-'] != values['-LG-'] and type(values['-DB-']) == bool and type(values['-LG-']) == bool):
            messages.append('Choose one of the themes.')
        if not re.search(r'^[1-9][0-9]*$', values['-ROWS-']):
            messages.append('"Rows" must be a number.')
        if not re.search(r'^[1-9][0-9]*$', values['-LENGTH-']):
            messages.append('"Length" must be a number.')
        for i in range(6):
            name, link = values['-NAME_{0}-'.format(i)].strip(), values['-LINK_{0}-'.format(i)].strip()
            if name != link and (name == '' or link == ''):
                messages.append('{0}: Only one of the name and link should not be blank'.format(i))
        return messages

    @staticmethod
    def save(values):
        settings = dict()
        settings['theme'] = 'DarkBlack' if values['-DB-'] is True else 'LightGrey2'
        settings['rows'] = int(values['-ROWS-'])
        settings['length'] = int(values['-LENGTH-'])
        settings['feeds'] = []
        for i in range(6):
            if values['-NAME_{0}-'.format(i)].strip() != '':
                settings['feeds'].append({
                    'name': values['-NAME_{0}-'.format(i)].strip(),
                    'link': values['-LINK_{0}-'.format(i)].strip()
                })
        with open('settings.yml', 'w') as file:
            yaml.dump(settings, file, encoding='utf-8', allow_unicode=True)
        return

    def open(self):
        style = [
            [sg.T('Theme', size=(self.LABEL_LEN, 1), justification='right'),
             sg.Radio('DarkBlack', default=self.__config.get('theme') == 'DarkBlack', group_id='-THEME-', key='-DB-'),
             sg.Radio('LightGrey2', default=self.__config.get('theme') == 'LightGrey2', group_id='-THEME-', key='-LG-')],
            [sg.T('Number of Rows', size=(self.LABEL_LEN, 1), justification='right'),
             sg.Input(self.__config.get('rows', ''), key='-ROWS-', size=(12, 2))],
            [sg.T('Headline Length', size=(self.LABEL_LEN, 1), justification='right'),
             sg.Input(self.__config.get('length', ''), key='-LENGTH-', size=(12, 2))]
        ]
        feeds = self.__config.get('feeds')
        sites = []
        for i in range(6):
            name, link = (feeds[i]['name'], feeds[i]['link']) if len(feeds) > i else ('', '')
            sites.append(
                [
                    sg.T('Name'.format(i), size=(self.LABEL_LEN, 1), justification='right'),
                    sg.Input(name, key='-NAME_{0}-'.format(i), size=(12, 2)),
                    sg.T('Url', size=(self.LABEL_LEN, 1), justification='right'),
                    sg.Input(link, key='-LINK_{0}-'.format(i), size=(50, 2))
                ]
            )
        layout = [
            [sg.Frame('Style', style, border_width=0)],
            [sg.Frame('Sites', sites, border_width=0)],
            [sg.Submit('Save'), sg.Cancel()]
        ]
        window = sg.Window('Settings', layout)
        while True:
            event, values = window.read()
            # In the author's environment, the string is mixed in with "\x10".
            values = {k: v.replace('\x10', '') if type(v) == str else v for k, v in values.items()}
            if event in (sg.WIN_CLOSED, 'Cancel'):
                break
            if event == 'Save':
                messages = SettingWindow.validate(values)
                if len(messages) == 0:
                    # save
                    SettingWindow.save(values)
                    break
                else:
                    message = '\n'.join(messages)
                    sg.Popup(message, title='Error')
                    break

        window.close()
