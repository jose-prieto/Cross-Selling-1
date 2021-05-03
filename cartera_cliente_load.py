import pandas as pd
import glob as gb
import pyodbc as pdbc

class cartera_cliente_load:
    
    #Constructor
    def __init__(self, ruta, db):
        print("Creando cartera")
        self.nombre_archivo = '\Cartera_Cliente'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.accdb'):
            self.ruta = file
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.ruta)
        self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Tipo_Atencion" FROM ' + db + ' WHERE "Tipo de Persona" = ?', conn, params=["PJ"])
        self.df = self.recorrerDF(self.df)

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
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\cartera.csv', index = False, header=True, sep='|')
        return self.df

#cartera = cartera_cliente_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo', 'Cartera_Clientes_Marzo_2021').to_csv()