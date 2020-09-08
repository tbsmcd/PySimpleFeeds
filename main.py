import PySimpleGUI as sg
import feedparser
import webbrowser

sg.theme('Black')
chrome_path = 'open -a /Applications/Google\ Chrome.app %s'


class PySimpleRss:
    def __init__(self):
        self.nhk, self.asa, self.mai, self.hat = [], [], [], []
        self.get_all_entries()
        self.layout = [[
            sg.Column([[sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in self.nhk]),
            sg.VSeparator(),
            sg.Column([[sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in self.asa]),
            sg.VSeparator(),
            sg.Column([[sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in self.mai]),
            sg.VSeparator(),
            sg.Column([[sg.T(self.format_text(v), enable_events=True, key='link_' + v['key'])] for v in self.hat]),
        ]]

    @staticmethod
    def format_text(v, length=17):
        return '[{0}] '.format(v['site']) + v['title'][:length] + ('...' if v['title'][length:] else '')

    def get_all_entries(self):
        def get_entries_list(key, rss):
            i = 0
            entries = []
            for ent in feedparser.parse(rss)['entries']:
                entries.append({'site': key, 'key': key + str(i), 'link': ent['link'], 'title': ent['title']})
                i += 1
                if i > 6:
                    break
            return entries
        self.nhk = get_entries_list('nhk', 'https://www.nhk.or.jp/rss/news/cat0.xml')
        self.asa = get_entries_list('asa', 'http://www.asahi.com/rss/asahi/newsheadlines.rdf')
        self.mai = get_entries_list('mai', 'https://mainichi.jp/rss/etc/mainichi-flash.rss')
        self.hat = get_entries_list('hat', 'https://b.hatena.ne.jp/entrylist.rss')

    def jump_link(self, key):
        entries = self.nhk + self.asa + self.mai + self.hat
        key_links = {val['key']: val['link'] for val in entries}
        webbrowser.get(chrome_path).open(key_links[key])

    def view(self):
        window = sg.Window('NEWS', self.layout)
        while True:
            event, values = window.read(timeout=10000)
            if event == sg.WIN_CLOSED:
                break
            if event.startswith('link_'):
                key = event.replace('link_', '')
                self.jump_link(key)
            elif event in sg.TIMEOUT_KEY:
                self.get_all_entries()
                entries = self.nhk + self.asa + self.mai + self.hat
                for v in entries:
                    window['link_' + v['key']].update(self.format_text(v))


if __name__ == '__main__':
    ps = PySimpleRss()
    ps.view()
