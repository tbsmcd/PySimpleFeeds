import PySimpleGUI as sg
import feedparser
import yaml
import webbrowser


class Reader:
    def __init__(self):
        with open('settings.yml') as file:
            self.config = yaml.safe_load(file.read())
        self.entries = {}

    def format_text(self, v):
        default_len = 17
        return '[{0}] '.format(v['site']) + v['title'][:self.config.get('length', default_len)] \
               + ('...' if v['title'][self.config.get('length', default_len):] else '')

    def get_all_entries(self):
        for rss in self.config.get('feeds'):
            i = 0
            entries = []
            for ent in feedparser.parse(rss['link'])['entries']:
                entries.append(
                    {'site': rss['name'], 'key': rss['key'] + str(i), 'link': ent['link'], 'title': ent['title']}
                )
                i += 1
                if i > self.config.get('rows', 6):
                    break
            self.entries[rss['key']] = entries

    def jump_link(self, key: str):
        browser = self.config.get('browser_path')
        if browser is None:
            return
        for site in self.entries.values():
            for entry in site:
                if entry['key'] == key:
                    webbrowser.get(browser).open(entry['link'])

    def show(self):
        sg.theme(self.config.get('theme', 'Dark'))
        self.get_all_entries()
        layout = [[
            sg.Column([[
                sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in site
            ]) for site in self.entries.values()
        ]]
        window = sg.Window('Feeds', layout)
        while True:
            event, values = window.read(timeout=60000)
            if event == sg.WIN_CLOSED:
                break
            if event.startswith('link_'):
                key = event.replace('link_', '')
                self.jump_link(key)
            elif event in sg.TIMEOUT_KEY:
                self.get_all_entries()
                for site in self.entries.values():
                    for entry in site:
                        window['link_' + entry['key']].update(self.format_text(entry))


if __name__ == '__main__':
    ps = Reader()
    ps.show()
