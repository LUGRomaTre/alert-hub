from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)

Base = declarative_base()


class Channel(Base):
    __tablename__ = 'channels'
    name = Column(String(50), primary_key=True)
    friendly_name = Column(String(100))
    description = Column(Text)
    articles = relationship("Article", back_populates="channel")

    def __repr__(self):
        return '<Channel {0}>'.format(self.name)


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    title = Column(String(255))
    text = Column(Text)
    source_url = Column(String(255))
    permalink = Column(String(255))
    channel_name = Column(String(50), ForeignKey('channels.name'))
    channel = relationship("Channel", back_populates="articles")

    def __repr__(self):
        return '<Article {0}>'.format(self.title)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
