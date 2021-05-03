import pandas as pd
import glob as gb
import csv

class ivr_conexion_load:
    
    #Constructor
    def __init__(self, ruta):
        print("Creando ivr conexion")
        self.nombre_archivo = '\ivr'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        self.df = pd.read_csv(self.ruta, delimiter='|', dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.df = self.df[self.df["cedula"].str.startswith(("J", "R", "G", "F"))]
        self.df = self.recorrerDF(self.df)
        
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"cedula"] = self.quitarCeros(fila["cedula"])
        return df
    
    def to_csv(self, cartera):
        print("Creando cruce cartera e ivr")
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='cedula')
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\ivrconexion.csv', index = False, header=True, sep='|')
        return self.df
    
#ivr = ivr_conexion_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').to_csv()