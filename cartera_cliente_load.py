import pandas as pd
import glob as gb
import pyodbc as pdbc
import csv

class cartera_cliente_load:
    
    #Constructor
    def __init__(self, ruta, rutadb, db):
        print("Creando cartera")
        self.rutadb = rutadb
        self.nombre_archivo = '\Cartera_Cliente'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.accdb'):
            self.ruta = file
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.ruta)
        self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM ' + db + ' WHERE "Tipo de Persona" = ?', conn, params=["PJ"])
        self.dfaux = self.df
        self.df = self.recorrerDF(self.df)
        self.df['MisCliente'] = self.df['MisCliente'].astype(str)

    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"CedulaCliente"] = self.quitarCeros(fila["CedulaCliente"])
        return df
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\cartera.csv', index = False, header=True, sep='|', encoding='UTF-8', quoting=csv.QUOTE_NONE)
        
    def to_db(self):
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.rutadb)
        df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM CARTERA', conn)
        df['MisCliente'] = df['MisCliente'].astype(int)
        df['CedulaCliente'] = df['CedulaCliente'].astype(str)
        df['NombreCliente'] = df['NombreCliente'].astype(str)
        df['Segmento Mis'] = df['Segmento Mis'].astype(str)
        df['Unidad De Negocio'] = df['Unidad De Negocio'].astype(str)
        df['Region'] = df['Region'].astype(str)
        df['Tipo_Atencion'] = df['Tipo_Atencion'].astype(str)
        
        self.dfaux['MisCliente'] = self.dfaux['MisCliente'].astype(int)
        self.dfaux['CedulaCliente'] = self.dfaux['CedulaCliente'].astype(str)
        self.dfaux['NombreCliente'] = self.dfaux['NombreCliente'].astype(str)
        self.dfaux['Segmento Mis'] = self.dfaux['Segmento Mis'].astype(str)
        self.dfaux['Unidad De Negocio'] = self.dfaux['Unidad De Negocio'].astype(str)
        self.dfaux['Region'] = self.dfaux['Region'].astype(str)
        self.dfaux['Tipo_Atencion'] = self.dfaux['Tipo_Atencion'].astype(str)
        return pd.concat([self.dfaux,df]).drop_duplicates(keep=False)

#cartera = cartera_cliente_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo', 'Cartera_Clientes_Marzo_2021').to_csv()