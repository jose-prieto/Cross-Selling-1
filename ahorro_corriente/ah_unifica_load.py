import pandas as pd
import glob as gb
import csv

class ah_unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera):
        self.nombre_archivo = '\\ah_unifica'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        self.df = pd.read_csv(self.ruta, delimiter='|', index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.df[' Monto Contable '] = self.df[' Monto Contable '].astype(float)
        self.df[' Oficina Contable '] = pd.to_numeric(self.df[' Oficina Contable '], errors='coerce')
        self.df = self.df.dropna(subset=[' Oficina Contable '])
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype(int)
        self.df = self.df[(self.df[" Oficina Contable "] <= 699) & 
                          (self.df[" Tipo Persona "] == "PERSONA JURIDICA") & 
                          (self.df[" Categoria "] != "B") & 
                          (self.df[" Categoria "] != "F") & 
                          (self.df[" Categoria "] != "H") & 
                          (self.df[" Categoria "] != "J") & 
                          (self.df[" Categoria "] != "K") & 
                          (self.df[" Categoria "] != "V") &
                          (self.df[" Estatus de la Operacion "] != "C") & 
                          (self.df[" Producto "] != "Ahorro - CUENTA EN DOLARES")]
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        self.dfBs = self.df[(self.df[" Producto "] != "Ahorro - CUENTA EN DOLARES")]
        self.dfBs = self.dfBs.groupby([' MIS '], as_index=False).agg({' Monto Contable ': sum})
        self.dfBs = self.dfBs.rename(columns={' MIS ': 'mis', ' Monto Contable ': 'monto'})
        self.dfDolar = self.df[(self.df[" Producto "] == "Ahorro - CUENTA EN DOLARES")]
        self.dfDolar = self.dfDolar.groupby([' MIS '], as_index=False).agg({' Monto Contable ': sum})
        self.dfDolar = self.dfDolar.rename(columns={' MIS ': 'mis', ' Monto Contable ': 'monto'})
    
    def to_csv(self, cartera):
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\h_unifica_Bs.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\h_unifica_Bs.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#todo = ah_unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#bs = todo.dfBs
#dolar = todo.dfDolar