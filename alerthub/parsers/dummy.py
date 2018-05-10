from ..parsers.base import Parser, Article


class DummyParser(Parser):
    @property
    def channel_name(self):
        return 'dummy-channel'

    def run(self):
        return Article('CIAO!'), Article('Davvero?')
