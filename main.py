import PySimpleGUI as sg
import feedparser
import yaml
import webbrowser

sg.theme('Black')


class PySimpleRss:
    def __init__(self):
        with open('settings.yml') as file:
            self.config = yaml.safe_load(file.read())
        self.entries = {}
        self.get_all_entries()
        self.layout = [[
            sg.Column([[
                sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in site
            ]) for site in self.entries.values()
        ]]

    @staticmethod
    def format_text(v, length=17):
        return '[{0}] '.format(v['site']) + v['title'][:length] + ('...' if v['title'][length:] else '')

    def get_all_entries(self):
        for rss in self.config['rss']:
            i = 0
            entries = []
            for ent in feedparser.parse(rss['link'])['entries']:
                entries.append(
                    {'site': rss['name'], 'key': rss['key'] + str(i), 'link': ent['link'], 'title': ent['title']}
                )
                i += 1
                if i > 6:
                    break
            self.entries[rss['key']] = entries

    def jump_link(self, key):
        for site in self.entries.values():
            for entry in site:
                if entry['key'] == key:
                    webbrowser.get(self.config['browser']['path']).open(entry['link'])

    def view(self):
        window = sg.Window('NEWS', self.layout)
        while True:
            event, values = window.read(timeout=1000)
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
    ps = PySimpleRss()
    ps.view()
