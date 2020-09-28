import shutil
import os
import PySimpleGUI as sg
import feedparser
import yaml
import webbrowser
import setting_window


class MainWindow:
    def __init__(self):
        self.__get_config()
        self.__entries = {}

    def __get_config(self):
        if os.path.isfile('settings.yml') is False:
            shutil.copyfile('settings.yml.default', 'settings.yml')
        with open('settings.yml') as file:
            self.__config = yaml.safe_load(file.read())

    def __format_text(self, v):
        default_len = 17
        return v['title'][:self.__config.get('length', default_len)] \
            + ('...' if v['title'][self.__config.get('length', default_len):] else '')

    def __get_all_entries(self):
        for rss in self.__config.get('feeds'):
            entries = []
            feed = feedparser.parse(rss['link'])
            if feed.status == 200:
                num_of_ent = len(feed['entries'])
                for i in range(self.__config.get('rows', 6)):
                    if i < num_of_ent:
                        ent = feed['entries'][i]
                        link, title = ent['link'], ent['title']
                    else:
                        link, title = '', ''
                    entries.append(
                        {'site': rss['name'], 'key': rss['name'] + str(i), 'link': link, 'title': title}
                    )
            else:
                for i in range(self.__config.get('rows', 6)):
                    if i == 0:
                        title = "HTTP_STATUS: {0}".format(feed.status)
                    else:
                        title = ''
                    entries.append(
                        {'site': rss['name'], 'key': rss['name'] + str(i), 'link': '', 'title': title}
                    )
            self.__entries[rss['name']] = entries

    def __jump_link(self, key: str):
        browser = self.__config.get('browser_path')
        if browser is None:
            return
        for site in self.__entries.values():
            for entry in site:
                if entry['key'] == key:
                    webbrowser.get(browser).open(entry['link'])

    def open(self):
        sg.theme(self.__config.get('theme', 'DarkBlack'))
        self.__get_all_entries()
        layout = [[
            sg.Frame(site[0]['site'], [
                [sg.T(self.__format_text(v), enable_events=True, key='link_' + v['key'])] for v in site
            ], border_width=0) for site in self.__entries.values()
        ], [sg.B('Setting')]]
        window = sg.Window('Feeds', layout)
        while True:
            event, values = window.read(timeout=60000)
            if event == sg.WIN_CLOSED:
                break
            elif event == 'Setting':
                sw = setting_window.SettingWindow()
                sw.open()
                window.close()
                ps = MainWindow()
                ps.open()

            elif event.startswith('link_'):
                key = event.replace('link_', '')
                self.__jump_link(key)
            elif event in sg.TIMEOUT_KEY:
                self.__get_all_entries()
                for site in self.__entries.values():
                    for entry in site:
                        window['link_' + entry['key']].update(self.__format_text(entry))
        window.close()
        # self.open()


if __name__ == '__main__':
    ps = MainWindow()
    ps.open()
