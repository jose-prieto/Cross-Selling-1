import pandas as pd
import csv

class ivr_conexion_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\ivrconexionkiosco_1610.txt'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_csv(self.ruta + self.nombre_archivo, delimiter='|', dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"cedula"] = self.quitarCeros(fila["cedula"])
        return df
    
    def make_DF(self):
        print("Creando ivr conexion")
        self.df = self.df[self.df["cedula"].str.startswith(("J", "R", "G", "F"))]
        self.df = self.recorrerDF(self.df)
        return self.df
    
#aux = ivr_conexion_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#ivr = aux.make_DF()