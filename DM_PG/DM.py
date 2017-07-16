import logging
import psycopg2.extras

"""contiene solo le Query SQL, tutte le comunicazioni con la base di dati sono qui. """


class DM():
    __server = "localhost"
    __database = "instrumarket"
    __user = "postgres"
    __pw = ""
    __connection = None
    __nIstanze = 0

    @classmethod
    def __open(cls, host=None, database=None, user=None, pw=None):
        if host is not None:
            cls.__server = host
        if database is not None:
            cls.__database = database
        if user is not None:
            cls.__user = user
            cls.__pw = pw
        if cls.__connection is None:
            try:
                cls.__connection = psycopg2.connect(\
                host=cls.__server, database=cls.__database, \
                user=cls.__user, password=cls.__pw )
                logging.info("connection to Database created")
            except psycopg2.OperationalError as err:
                logging.error("Error connecting to PostgreSQL DBMS \
                at %s. \nDetails: %s.", cls.__server, err)
                exit()

    @classmethod
    def __close(cls):
        if cls.__nIstanze == 0 and cls.__connection is not None:
            cls.__connection.close()
            logging.info("connection closed.")
            cls.__connection = None

    @classmethod
    def __cursor(cls):
        """ Ritorna un cursore che restituisce dict invece di tuple \
        per ciascuna riga di una select."""
        return cls.__connection.cursor( \
        cursor_factory=psycopg2.extras.DictCursor )

    def __init__(self):
        type(self).__open()
        type(self).__nIstanze += 1

    def close(self):
        """chiude in modo esplicito la connessione, se non ci sono \
        altre istanze attive"""
        self.__del__()

    def __del__(self):
        type(self).__nIstanze -= 1
        type(self)._close()

    def __enter__(self): # per il with
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


#################### Verifica credenziali sulla base di dati ################################################

# ritorna la password se trova username nella tabella cliente altrimenti niente.
    def getPassword(self, username):
        with type(self).__cursor() as cur:
            cur.execute('SELECT password \
            From Cliente \
            Where username ILIKE %s', (username,))
            pwd = cur.fetchone()
            return pwd



#################### Parte del codice per Ricerca-Strumento per Categoria, Modello o Nome. ##################

# Funzioni per Strumenti Professionali


## ritorna una lista di strumenti Professionali ove la categoria è uguale a categ
    def getStrumentiProPerCat(self, categ):
        with type(self).__cursor() as cur:
            cur.execute('SELECT SP.id, SP.prezzo_proposto, SP.prezzo, SP.usato, SP.modello, SP.categoria, F.path \
            From StrumentoProfessionale SP \
            JOIN FotoStrumentiProfessionali F On SP.id = F.strumentop \
            WHERE categoria ILIKE %s ', (categ,))
            return list(cur)


## ritorna una lista di strumenti Professionali ove l'id dello strumento è uguale a Nome.
    def getStrumentiProPerNome(self, nome):
        with type(self).__cursor() as cur:
            cur.execute('SELECT SP.id, SP.prezzo_proposto, SP.prezzo, SP.usato, SP.modello, SP.categoria, F.path \
            From StrumentoProfessionale sp \
            Join FotoStrumentiProfessionali F On SP.id = F.strumentop \
            WHERE id ILIKE %s', (nome,))
            return list(cur)

## ritorna una lista di strumenti Professionali ove il modello dello strumento è uguale a modello
    def getStrumentiProPerModello(self, modello):
        with type(self).__cursor() as cur:
            cur.execute('SELECT SP.id, SP.prezzo_proposto, SP.prezzo, SP.usato, SP.modello, SP.categoria, F.path \
            From StrumentoProfessionale sp \
            Join FotoStrumentiProfessionali F On SP.id = F.strumentop \
            WHERE modello ILIKE %s', (modello,))
            return list(cur)



# Funzioni per Strumenti Per Scuole Musicali


## ritorna una lista di strumenti per scuole Musicali ove la categoria è uguale a categ
    def getStrumentiPsmPerCat(self, categ):
        with type(self).__cursor() as cur:
            cur.execute('SELECT sps.id, sps.sconto_applicato, sps.prezzo, sps.modello, sps.categoria, f.path \
            From StrumentoPsm sps \
            Join FotoStrumentiPsm F on sps.id = f.strumento_psm \
            WHERE categoria ILIKE %s ', (categ,))
            return list(cur)


## ritorna una lista di strumenti per scuole musicali ove l'id dello strumento è uguale a Nome.




            #pass






## ritorna una lista di strumenti per scuole musicali ove il modello dello strumento è uguale a mod
    def getStrumentiPsmPerModello(self, mod):
        with type(self).__cursor() as cur:
            cur.execute('SELECT sps.id, sps.sconto_applicato, sps.prezzo, sps.modello, sps.categoria, f.path \
            From StrumentoPsm sps \
            Join FotoStrumentiPsm F on sps.id = f.strumento_psm \
            WHERE modello ILIKE %s ', (mod,))
            return list(cur)











############################ Parte del codice per il Visualizza-Catalogo ##############################



# ritorna una lista di strumenti Professionali, allegando anche la foto se c'è dello strumento.
    def getStrumentiPro(self):
        with type(self).__cursor() as cur:
            cur.execute('SELECT sp.*, f.path \
            From StrumentoProfessionale sp \
            Join FotoStrumentiProfessionali f on sp.id = f.strumentop')
            return list(cur)





#ritorns una lista di strumenti per scuole musicali, allegando anche la foto se c'è dello strumento.
    def getStrumentiPsm(self):
        with type(self).__cursor() as cur:
            cur.execute('SELECT psm.*, f.path \
            From StrumentoPsm psm \
            Join FotoStrumentiPsm f on psm.id = f.strumento_psm')
            return list(cur)
