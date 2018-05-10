# Alert Hub
Un **aggregatore di notizie/avvisi** che usa varie sorgenti come i siti dei  professori, le varie mailing list, feed RSS, ecc...

Il progetto è scritto in **Python 3**. 

## Stato del progetto
### Canali supportati

  - *informatica-teorica*
  
### Output supportati

  - *SimpleOutput*: output testuale sullo stdout
  - *RSSOutput*: server web - RSS
  
## Avvio

Creare una [virtualenv](https://docs.python.org/3/tutorial/venv.html) se desiderato (consigliato).

Installare le dipendenze richieste:
 
    $ pip install -r requirements.txt

Avviare il file **main.py**:
    
    $ python3 main.py
    
## Contribuire
Attualmente nel file `alerthub/init.py` si possono avviare manualmente i vari moduli dell'applicazione.

Creare un fork del repo e una volta terminate le modifiche creare una **Pull request**.

### Come creare un Parser
Le classi `Parser` hanno lo scopo di prendere avvisi dai vari siti (come quelli dei professori). 

 - Usare come modello il file `alerthub/parsers/informatica_teorica.py`
 - Esportare il nuovo Parser creato dentro il file `alerthub/parsers/__init__.py`
 - Importarla in `alerthub/__init__.py` e registrare il Parser appena esportato:
 
 ```python
crawler.register_parser(parsers.NuovoParser)
```

Nella pratica si tratta di estendere la classe astratta `Parser` e di registrarla presso l'oggetto `Crawler` che
potrà così eseguirla. Bisogna implementare i metodi `channel_name` e `run`. 

`channel-name` ritorna il nome del canale dove salvare i dati (scegliere un "nome-significativo");
`run` si occupa di fare il parsing del sito desiderato e ritornare una `iterable` di oggetti `Article`. 

L'oggetto `Article` supporta i seguenti campi:

 - text (required)
 - title
 - datetime