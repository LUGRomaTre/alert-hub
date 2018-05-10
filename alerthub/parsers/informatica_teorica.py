import datetime
import re

import requests
from bs4 import BeautifulSoup

from ..parsers.base import Parser, Article


# noinspection SpellCheckingInspection,PyMethodMayBeStatic
class InformaticaTeoricaParser(Parser):
    def __init__(self):
        self.session = requests.Session()

    @property
    def channel_name(self):
        return 'informatica-teorica'

    def run(self):
        b = self._load_html()
        ul_list = self._load_annunci_ul_list(b)
        articles = [self._get_article_from_ul(ul) for ul in ul_list]
        return articles

    def _load_html(self):
        r = self.session.get('http://www.dia.uniroma3.it/~teorica/')
        return BeautifulSoup(r.text, 'html.parser')

    def _load_annunci_ul_list(self, b):
        inizio_annuncio_pattern = re.compile("^ *INIZIO ANNUNCIO *$")

        aa = b.find_all(text=inizio_annuncio_pattern)
        ul_list = []
        for comment in aa:
            tag = comment
            while tag:
                if tag.name == 'ul':
                    ul_list.append(tag)
                    break
                tag = tag.next_sibling
        return ul_list

    def _get_article_from_ul(self, ul):
        date = self._get_date_from_annuncio(ul.find('b').text)
        td = ul.find('td')
        if td is not None:
            title = td.find('h3').text
            text = self._get_text_from_td(td)
            return Article(text=text, title=title, datetime=date)
        return Article(text=ul)

    def _get_text_from_td(self, td):
        filtered = filter(lambda tag: tag.name != 'h3', td.contents)
        text = ''.join(map(lambda tag: str(tag), filtered))
        return text

    def _get_date_from_annuncio(self, text):
        day, month, year = re.compile('(\d{1,2})/(\d{1,2})/(\d{4})').search(text).group(1, 2, 3)
        return datetime.datetime(int(year), int(month), int(day))
