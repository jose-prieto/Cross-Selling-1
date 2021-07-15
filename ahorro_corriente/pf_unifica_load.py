import pandas as pd
import glob as gb
import csv

class pf_unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera):
        self.nombre_archivo = '\pf_unifica'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        self.df = pd.read_csv(self.ruta, delimiter='|', index_col=False, decimal=",", dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.df = self.df[(self.df[" Tipo Persona "] == "PERSONA NATURAL")]
        self.df[' Monto '] = self.df[' Monto '].astype('float')
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype('int')
        self.df = self.df[(self.df[" Oficina Contable "] < 700) & 
                          (self.df[" Estatus de la Operacion "] != "CANCELADA")]
        
        print("pf_unifica bolívares monto total: ", self.df[' Monto '].sum())
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        self.df = self.df.groupby([' MIS '], as_index=False).agg({' Monto ': sum})
        self.df = self.df.rename(columns={' MIS ': 'mis', ' Monto ': 'monto'})
    
#todo = cc_unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero')
#Bs = todo.df
#Dolar = todo.dfDolar
#Euro = todo.dfEuro