from typing import Type

from .model import Article, Channel, session_scope
from .parsers import Parser


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


class Crawler:
    def __init__(self):
        self.parsers: [Type[Parser]] = []

    def start(self):
        with session_scope() as session:
            for P in self.parsers:
                parser = P()
                channel_name = parser.channel_name

                articles = parser.run()
                my_channel = get_or_create(session, Channel, name=channel_name)

                db_objects = []
                for article in articles:
                    a = Article(text=article.text,
                                datetime=article.datetime,
                                title=article.title,
                                channel_name=channel_name)
                    db_objects.append(a)

                session.add_all(db_objects)

    def register_parser(self, parser: Type[Parser]):
        self.parsers.append(parser)
