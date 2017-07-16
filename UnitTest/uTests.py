import sys, os
lib_path = os.path.abspath(os.path.join('..', 'WebSite'))
sys.path.append(lib_path)
import unittest
import controller



class FlaskTestCase(unittest.TestCase):
    def test_login(self):
        tester = controller.app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)



# verifichiamo se login accetta soli le Credenziali valide
    def test_login_corretto(self):
        tester = controller.app.test_client(self)
        response = tester.get('/verificaCredenziali',
        data=dict(username="mina", password="0909"),
        follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)


# verifichiamo se login non accetta le Credenziali non valide
    def test_pagina_login_scorretto(self):
        tester = controller.app.test_client(self)
        response = tester.get('/verificaCredenziali',
        data=dict(username="unknown", password="Errore"),
        follow_redirects=True
        )
        self.assertIn(b'Credenziali non valide', response.data)



# verifico se la pagina strumenti ritorna la risposta giusta per la ricerca scelta.
    def test_ricercaStrumenti(self):
        tester = controller.app.test_client(self)
        response = tester.post('/strumenti',
        data=dict(metods="modello" , categ="X010"),
        follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
#/!\: l'errore che mi dava in test_ricercaStrumenti è perché usavo testet.get che è una HTTP GET, invece serviva il HTTP POST



# verifichiamo se la pagina catalogo si carica, testando se il file di html contiene un id di uno strumento professionale
# caricato dalla base di dati - XX00000000-
    def test_pagina_catalogo_carica(self):
        tester = controller.app.test_client(self)
        response = tester.get('/catalogo', )
        self.assertTrue(b'XX00000000' in response.data)










if __name__ == '__main__':
    unittest.main()
