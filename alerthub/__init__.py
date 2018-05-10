from . import parsers
from .crawler import Crawler
from .outputs import SimpleOutput, RSSOutput

crawler = Crawler()
# crawler.register_parser(DummyParser)
crawler.register_parser(parsers.InformaticaTeoricaParser)
crawler.start()
# make_test_data()


SimpleOutput().print()
RSSOutput().run()
