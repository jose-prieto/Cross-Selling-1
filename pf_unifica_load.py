import pandas as pd
import glob as gb

class pf_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\pf_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.txt'):
            filename = file
        self.df = pd.read_csv(filename, delimiter='|', index_col=False, dtype=str, encoding='latin-1')
    
    def make_DF(self):       
        print("Cargando pf_unifica")
        self.df[' Monto '] = self.df[' Monto '].astype(float)
        self.df = self.df[(self.df[" Tipo Persona "] == "PERSONA JURIDICA") & ((self.df[" Estatus de la Operacion "] == "Activo") | (self.df[" Estatus de la Operacion "] == "Inactivo"))]
        self.df = self.df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto ': sum})
        return self.df