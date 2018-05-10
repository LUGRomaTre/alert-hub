from datetime import datetime

from .model import session_scope, Channel, Article


def make_test_data():
    with session_scope() as session:
        my_channel = Channel(name='dia-dibb-teorica')
        my_article = Article(title='Verbalizzazione degli esiti della valutazione in itinere',
                             text="Gli studenti che intendano avvalersi del risultato conseguito nella valutazione in itinere devono"
                                  " obbligatoriamente: (1) Prenotarsi all'esame per l'appello di febbraio. (2) Presentarsi in uno "
                                  "dei seguenti orari di verbalizzazione: - martedi' 20 febbraio ore 13:00 - ufficio del docente;"
                                  " - venerdi' 23 febbraio ore 17:00 - ufficio del docente. Gli studenti che si presenteranno"
                                  " all'esame scritto dell'appello di febbraio rifiuteranno implicitamente il voto della "
                                  "valutazione in itinere.", channel_name=my_channel.name, datetime=datetime.now())
        my_article2 = Article(text='Roba', channel_name=my_channel.name)
        session.add_all((my_channel, my_article, my_article2))
