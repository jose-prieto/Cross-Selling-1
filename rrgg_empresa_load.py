import pandas as pd

class rrgg_empresa_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\rrgg empresa'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + ' 29-01.xls', header=0, index_col=False, keep_default_na=True)
        return df