import pandas as pd
import csv

class ah_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\ah_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_csv(self.ruta + self.nombre_archivo + '2901.txt', delimiter='|', index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
    
    def make_DF(self):
        print("Creando ah_unifica")
        self.df[' Monto Contable '] = self.df[' Monto Contable '].astype(float)
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype(int)
        self.df = self.df[(self.df[" Oficina Contable "] <= 699) & (self.df[" Tipo Persona "] == "PERSONA JURIDICA") & 
                          (self.df[" Categoria "] != "B") & (self.df[" Categoria "] != "F") & (self.df[" Categoria "] != "H") & (self.df[" Categoria "] != "J") & (self.df[" Categoria "] != "K") & (self.df[" Categoria "] != "V") &
                          (self.df[" Producto "] != "Ahorro - CUENTA EN DOLARES")]
        self.df = self.df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto Contable ': sum})
        return self.df
    
#d = ah_unifica_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#ah = d.make_DF()