import pandas as pd

class reporte_pos_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\Reporte POS'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + ' Enero 2021.xlsx', header=0, index_col=False, keep_default_na=True)
        return df