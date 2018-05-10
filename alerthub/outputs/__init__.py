from .rss import RSSOutput
from ..model import session_scope, Article


class SimpleOutput:
    def print(self):
        with session_scope() as session:
            # .options(joinedload(Article.channel))
            for a in session.query(Article).all():
                print(a.channel_name + ': ' + a.text)
