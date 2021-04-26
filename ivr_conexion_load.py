import pandas as pd

class ivr_conexion_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\ivrconexionkiosco_1610.txt'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
            
        df = pd.read_csv(self.ruta + self.nombre_archivo, delimiter='|', dtype=str, encoding='latin-1')
        
        return df