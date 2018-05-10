from http.server import BaseHTTPRequestHandler, HTTPServer
from xml.etree.ElementTree import Element, ElementTree, SubElement

from sqlalchemy.orm import joinedload

from ..model import session_scope, Channel


class RSSOutput:
    def run(self):
        httpd = HTTPServer(('127.0.0.1', 8080), HTTPRequestHandler)
        httpd.serve_forever()


class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('ico'):
            self._send_404()
            return

        top = Element('rss', {'version': '2.0'})

        with session_scope() as session:
            channel_name = self.path.strip('/')
            my_channel = session.query(Channel) \
                .filter(Channel.name == channel_name) \
                .options(joinedload(Channel.articles)) \
                .first()

            if my_channel is None:
                return self._send_404('Channel "%s" not found' % channel_name)

            channel_el = SubElement(top, 'channel')
            title_el = SubElement(channel_el, 'title')
            title_el.text = my_channel.name

            for my_article in my_channel.articles:
                item_el = SubElement(channel_el, 'item')
                title_el = SubElement(item_el, 'title')
                title_el.text = my_article.title
                pub_date_el = SubElement(item_el, 'pubDate')
                pub_date_el.text = my_article.datetime.isoformat()

                description = SubElement(item_el, 'description')
                description.text = my_article.text

            self._send_rss(ElementTree(top))

    def _send_rss(self, rss):
        self.send_response(200)
        self.send_header('Content-type', 'application/rss+xml')
        self.end_headers()
        rss.write(self.wfile, encoding='utf-8', xml_declaration=True)

    def _send_404(self, message='404 Not Found'):
        self.send_response(404)
        self.end_headers()
        self.wfile.write(message.encode())
