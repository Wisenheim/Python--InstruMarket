import logging
from flask import Flask, request
from flask.templating import render_template
from Model import Model



logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)
app.model = Model.Model()



# definisco la funzione index() che mi ritorna la pagina Home di InstruMarket
@app.route('/')
def index():
    return render_template('index.html')



# definisco la funzione login() che mi ritorna la pagina del login.
@app.route('/login')
def login():
	return render_template('login.html')



# definisco la funzione verificaCredenziali() che verifica se le Credenziali sono validi, in tal caso mi porta alla pagina home
# altrimenti mi da l'errore dell'invalidità di Credenziali
@app.route('/verificaCredenziali', methods=['GET','POST'])
def verificaCredenziali():
	username =request.form['username']
	password =request.form['password']

	if app.model.verificaUser( username, password ):
		print("Benvenuto " + username)
		return render_template('index.html', )
	else:
		return render_template('login.html', error="Credenziali non valide")


# definisco la funzione catalogo() che mi ritorna la pagina catalogo che contiene gli strumenti disponibili.
@app.route('/catalogo')
def catalogo():

    catalogoPro = app.model.getCatalogoPro()
    catalogoPsm = app.model.getCatalogoPsm()
    return render_template('catalogo.html', catalogoPro=catalogoPro, catalogoPsm=catalogoPsm)


# definisco la funzione strumenti() che mi ritorna
# una pagina con la lista di strumenti sia professionali che PSM considerando la ricerca scelta.
@app.route('/strumenti', methods=['POST','GET'])
def strumenti():
    if request.method == 'POST':
        categ = request.form['categ']
        metods = request.form['metods']
    else:
        categ = request.args['categ']
        metods = request.args['metods']

    strumentiPro = app.model.getStrumentiPro(categ, metods)
    strumentiPsm = app.model.getStrumentiPsm(categ, metods)
    if len(list(strumentiPro)) == 0 and len(list(strumentiPsm)) == 0:
        print('é vuota purtroppo xD')
        vuota=True
    else:
        vuota=False
    return render_template('strumenti.html', strumentiPro=strumentiPro, strumentiPsm=strumentiPsm, vuota=vuota)


if __name__ == '__main__':
    app.run(debug=False)
