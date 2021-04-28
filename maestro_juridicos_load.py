import pandas as pd

class maestro_juridicos_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\Maestro de Tarjetas Clientes Juridicos'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_TDC_ACTIVAS(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + ' Enero 2021.xlsx', sheet_name="TDC ACTIVAS", header=0, index_col=False, keep_default_na=True)
        return df
    
    def make_CUENTAS_MADRES_JURIDICAS(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + ' Enero 2021.xlsx', sheet_name="CUENTAS MADRES JURIDICAS", header=0, index_col=False, keep_default_na=True)
        return df