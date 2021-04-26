import pandas as pd

class P2C_Transacciones_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\P2C_Transaccion'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        df = pd.read_excel(self.ruta + self.nombre_archivo + 'es enero.xlsx', header=0, index_col=False, keep_default_na=True)
        return df
    
hola = P2C_Transacciones_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').make_DF()