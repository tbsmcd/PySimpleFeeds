import PySimpleGUI as sg
import feedparser
import yaml
import webbrowser


class MainWindow:
    def __init__(self):
        with open('settings.yml') as file:
            self.__config = yaml.safe_load(file.read())
        self.__entries = {}

    def __format_text(self, v):
        default_len = 17
        return '[{0}] '.format(v['site']) + v['title'][:self.__config.get('length', default_len)] \
               + ('...' if v['title'][self.__config.get('length', default_len):] else '')

    def __get_all_entries(self):
        for rss in self.__config.get('feeds'):
            i = 0
            entries = []
            for ent in feedparser.parse(rss['link'])['entries']:
                entries.append(
                    {'site': rss['name'], 'key': rss['key'] + str(i), 'link': ent['link'], 'title': ent['title']}
                )
                i += 1
                if i > self.__config.get('rows', 6):
                    break
            self.__entries[rss['key']] = entries

    def __jump_link(self, key: str):
        browser = self.__config.get('browser_path')
        if browser is None:
            return
        for site in self.__entries.values():
            for entry in site:
                if entry['key'] == key:
                    webbrowser.get(browser).open(entry['link'])

    def show(self):
        sg.theme(self.__config.get('theme', 'Dark'))
        self.__get_all_entries()
        layout = [[
            sg.Column([[
                sg.T(self.__format_text(v), enable_events=True, key='link_' + v['key'])] for v in site
            ]) for site in self.__entries.values()
        ], [sg.B('Setting')]]
        window = sg.Window('Feeds', layout)
        while True:
            event, values = window.read(timeout=60000)
            if event == sg.WIN_CLOSED:
                break
            if event.startswith('link_'):
                key = event.replace('link_', '')
                self.__jump_link(key)
            elif event in sg.TIMEOUT_KEY:
                self.__get_all_entries()
                for site in self.__entries.values():
                    for entry in site:
                        window['link_' + entry['key']].update(self.__format_text(entry))
        window.close()


if __name__ == '__main__':
    ps = MainWindow()
    ps.show()
