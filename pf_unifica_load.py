import pandas as pd
import glob as gb

class pf_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\pf_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):       
        print("Cargando pf_unifica")
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.txt'):
            filename = file
            
        df = pd.read_csv(filename, delimiter='|', index_col=False, dtype=str, encoding='latin-1')
        df[' Monto Contable '] = df[' Monto Contable '].astype(float)
        df = df[(df[" Tipo Persona "] == "PERSONA JURIDICA") & ((df[" Estatus de la Operacion "] == "Activo") | (df[" Estatus de la Operacion "] == "Inactivo"))]
        df = df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto Contable ': sum})
        return df