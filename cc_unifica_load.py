import pandas as pd
import glob as gb

class cc_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\cc_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
            
        df = pd.read_csv(self.ruta + self.nombre_archivo + '2901.txt', delimiter='|', dtype=str, encoding='latin-1')
        
        return df