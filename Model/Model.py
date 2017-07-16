from DM_PG import DM

class Model(object):
    """Fornisce tutti i metodi per acquisire i dati da pubblicare. \
    li chiede al dataMapper, appena li riceve li manda al controller."""

    def __init__(self):
        self.dataMapper = DM.DM()




    def verificaUser(self, username, password):
        pwd = self.dataMapper.getPassword(username)
        if pwd is None or password != pwd['password']:
            return False
        else:
            return True

# ritorna un catalogo di soli strumenti professionali usando la funzione getStrumentiPro() del dataMapper.
    def getCatalogoPro(self):
        return self.dataMapper.getStrumentiPro()

# ritorna un catalogo di soli strumenti per scuole musicali psm usando la funzione getStrumentiPsm() del dataMapper.
    def getCatalogoPsm(self):
        return self.dataMapper.getStrumentiPsm()


# qui chiamo le funzioni del DataMapper che mi ritornano una lista di strumenti professionali o per categoria o per modello
    def getStrumentiPro(self, categ, metods):
        if metods == "categoria":
            return self.dataMapper.getStrumentiProPerCat(categ)
        elif metods == "modello":
            return self.dataMapper.getStrumentiProPerModello(categ)

# qui chiamo le funzioni del DataMapper che mi ritornano una lista di strumenti per Scuole Musicali o per categoria o per modello
    def getStrumentiPsm(self, categ, metods):
        if metods == "categoria":
            return self.dataMapper.getStrumentiPsmPerCat(categ)
        elif metods == "modello":
            return self.dataMapper.getStrumentiPsmPerModello(categ)

    def __del__(self):
        self.dataMapper.close()
