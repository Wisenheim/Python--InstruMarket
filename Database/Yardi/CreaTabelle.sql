
CREATE DOMAIN LivelloStrumento AS VARCHAR(12)
	CHECK( VALUE IN( 'principante', 'intermedio', 'avanzato' ) );

CREATE DOMAIN Consegna AS VARCHAR(10)
	CHECK( VALUE IN( 'normale', 'rapida', 'tracciata' ));

CREATE DOMAIN Pagamento AS VARCHAR(16)
	CHECK( VALUE IN( 'bonifico', 'alla consegna', 'paypal', 'carta di credito' ) );


CREATE TABLE if not exists Cliente
(
	cf 		CHAR(16) PRIMARY KEY,
	username        VARCHAR(20),
	password	VARCHAR(20),
	nome		VARCHAR(20)   NOT NULL,
	cognome		VARCHAR(20)   NOT NULL,	
	email           VARCHAR(30)   NOT NULL,
	via		VARCHAR(20)   NOT NULL,
	citta		VARCHAR(30)   NOT NULL,
	CAP		INTEGER       NOT NULL,
	provincia 	VARCHAR(20)   NOT NULL,
	telefono	INTEGER       NOT NULL,
	registrato	BOOLEAN,
	cellulare	INTEGER
	
);

CREATE TABLE if not exists Tsm
(
	cf CHAR(16) PRIMARY KEY
				REFERENCES Cliente( cf )
					ON DELETE CASCADE
					ON UPDATE CASCADE
);

CREATE TABLE if not exists MusicistiProfessionisti 
(
	cf CHAR(16) PRIMARY KEY
				REFERENCES Cliente( cf )
					ON DELETE CASCADE
					ON UPDATE CASCADE
);

CREATE TABLE if not exists StrumentoPSM
(	id				CHAR(10)    PRIMARY KEY,
	sconto_applicato 		NUMERIC( 4, 2 )  NOT NULL,
	numero_pezzi_per_sconto 	INTEGER          NOT NULL,
	prezzo				NUMERIC(8,2)     NOT NULL,
	peso				NUMERIC( 5, 2 )  NOT NULL,
	descrizione			VARCHAR(60)      NOT NULL,
	data_presenza_sul_sito		DATE             NOT NULL,
	livello_consigliato		LivelloStrumento NOT NULL,
	modello                         VARCHAR(20)      NOT NULL,
	categoria                       VARCHAR(20)      NOT NULL
);

CREATE TABLE if not exists StrumentoProfessionale
(
	id				CHAR(10) PRIMARY KEY,
	venditore			CHAR(16) 
						REFERENCES MusicistiProfessionisti( cf )
							ON DELETE	CASCADE
							ON UPDATE	CASCADE,
	data_presenza_sul_sito 		DATE 		NOT NULL,
	usato				BOOLEAN,
	prezzo_proposto			NUMERIC(8,2) 	NOT NULL,
	descrizione			VARCHAR( 60 ),
	prezzo				NUMERIC(8,2) 	NOT NULL,
	sconto_praticabile		NUMERIC(4,2 ),
	peso				NUMERIC( 5, 2 ),
	ip_venditore			CHAR(16),
	data_messa_in_vendita		DATE		NOT NULL,
	modello                         VARCHAR(20)     NOT NULL,
	categoria                       VARCHAR(20)     NOT NULL

);


CREATE TABLE if not exists Strumento
(
	id				CHAR(10) PRIMARY KEY,
	data_presenza_sul_sito 		DATE 		NOT NULL,
	descrizione			VARCHAR( 60 ),
	prezzo				NUMERIC(8,2) 	NOT NULL,
	peso				NUMERIC( 5, 2 ),
	modello                         VARCHAR(20)     NOT NULL,
	categoria                       VARCHAR(20)     NOT NULL

);




CREATE TABLE if not exists FotoStrumentiProfessionali
(
	path 		VARCHAR( 100 ) NOT NULL,
	strumentoP	CHAR(10) NOT NULL
				REFERENCES StrumentoProfessionale( id )
					ON DELETE CASCADE
					ON UPDATE CASCADE,
        PRIMARY KEY (path, strumentoP)
);

CREATE TABLE if not exists FotoStrumentiPSM
(
	path		VARCHAR(100) NOT NULL,
	strumento_psm	CHAR(10) NOT NULL
				REFERENCES StrumentoPSM( id )
					ON DELETE CASCADE
					ON UPDATE CASCADE,
        PRIMARY KEY (path, strumento_psm)
);


CREATE TABLE if not exists FotoStrumenti
(
	path		VARCHAR(100) NOT NULL,
	strumento	CHAR(10) NOT NULL
				REFERENCES Strumento( id )
					ON DELETE CASCADE
					ON UPDATE CASCADE,
        PRIMARY KEY (path, strumento)
);


CREATE TABLE if not exists AcquistoTSM
(
        tsm				CHAR(16) NOT NULL
						REFERENCES TSM( cf )
							ON DELETE NO ACTION
							ON UPDATE CASCADE,
        data				DATE,
	ip_cliente			CHAR(16),
	ora				TIME NOT NULL,
	prezzo_praticato		NUMERIC( 8,2 ) NOT NULL, 
	modalita_consegna		Consegna NOT NULL,
	modalita_pagamento		Pagamento,

	PRIMARY KEY( tsm, data )
);

CREATE TABLE if not exists OggettoVenditaTSM
(
	tsm 		CHAR(16) NOT NULL,
	data_acquisto		DATE,
	strumento		CHAR(10) NOT NULL
					REFERENCES StrumentoPSM( id )
						ON DELETE NO ACTION
						ON UPDATE CASCADE,
	quantita		INTEGER NOT NULL,
	
	PRIMARY KEY( tsm, data_acquisto, strumento ),
	FOREIGN KEY( tsm, data_Acquisto ) 
		REFERENCES AcquistoTSM( tsm, data )
			ON DELETE NO ACTION
			ON UPDATE CASCADE
);

CREATE TABLE if not exists AcquistoPrivato
(
        cliente			CHAR(16) NOT NULL REFERENCES Cliente(cf),
	data			DATE NOT NULL,
	ip_cliente 		CHAR(16) NOT NULL,
	ora			TIME NOT NULL,
	prezzo_praticato	NUMERIC( 8, 2 ) NOT NULL,
	modalita_consegna	Consegna,
	modalita_pagamento	Pagamento,

	PRIMARY KEY( cliente, data )
);

CREATE TABLE if not exists OggettoVendita
(
	cliente	        CHAR(16) NOT NULL,
	data_acquisto	DATE     NOT NULL,
	strumento	CHAR(10) NOT NULL
				REFERENCES StrumentoProfessionale( id)
					ON DELETE NO ACTION
					ON UPDATE CASCADE,
	quantita	INTEGER NOT NULL,

	PRIMARY KEY( cliente, data_acquisto, strumento ),
	FOREIGN KEY( cliente, data_Acquisto ) 
		REFERENCES AcquistoPrivato( cliente, data )
			ON DELETE NO ACTION
			ON UPDATE CASCADE
);




CREATE TABLE IF NOT EXISTS OffertaPro
(
        id              VARCHAR(10) NOT NULL,
        strumentoPro    CHAR(10) NOT NULL constraint FkeyOffrPro REFERENCES StrumentoProfessionale(id)
                                                                        ON DELETE NO ACTION
                                                                        ON UPDATE CASCADE,
        descrizione     VARCHAR NOT NULL,
        scadenza        DATE NOT NULL,
        dataPartenza    DATE NOT NULL,
        prezzo          NUMERIC(8,2) NOT NULL,
        
        PRIMARY KEY (id, strumentoPro)

);


CREATE TABLE IF NOT EXISTS ScontoPro
(
        id              VARCHAR(10) NOT NULL,
        strumentoPro    CHAR(10) NOT NULL constraint FkeyScontPro REFERENCES StrumentoProfessionale(id)
                                                                        ON DELETE NO ACTION
                                                                        ON UPDATE CASCADE,
        descrizione     VARCHAR NOT NULL,
        scadenza        DATE NOT NULL,
        dataPartenza    DATE NOT NULL,
        prezzo          NUMERIC(8,2) NOT NULL,
        prezzoScontato  NUMERIC(8,2) NOT NULL,
        PRIMARY KEY (id, strumentoPro)

);






CREATE TABLE IF NOT EXISTS OffertaPSM
(
        id              VARCHAR(10) NOT NULL,
        strumentoPSM    CHAR(10) NOT NULL constraint FkeyOffrPsm REFERENCES StrumentoPSM(id)
                                                                        ON DELETE NO ACTION
                                                                        ON UPDATE CASCADE,
        descrizione     VARCHAR NOT NULL,
        scadenza        DATE NOT NULL,
        dataPartenza    DATE NOT NULL,
        prezzo          NUMERIC(8,2) NOT NULL,
        
        PRIMARY KEY (id, strumentoPSM)

);





CREATE TABLE IF NOT EXISTS ScontoPSM
(
        id              VARCHAR(10) NOT NULL,
        strumentoPSM    CHAR(10) NOT NULL constraint FkeyScontPsm REFERENCES StrumentoPSM(id)
                                                                        ON DELETE NO ACTION
                                                                        ON UPDATE CASCADE,
        descrizione     VARCHAR NOT NULL,
        scadenza        DATE NOT NULL,
        dataPartenza    DATE NOT NULL,
        prezzo          NUMERIC(8,2) NOT NULL,
        prezzoScontato  NUMERIC(8,2) NOT NULL,
        PRIMARY KEY (id, strumentoPSM)

);
