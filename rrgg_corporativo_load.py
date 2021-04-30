import pandas as pd

class rrgg_corporativo_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\rrgg corporativo'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + ' 29-01.xls', header=0, index_col=False, keep_default_na=True)
        return df
    
#corp = rrgg_corporativo_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#rrggCorp = corp.make_DF()