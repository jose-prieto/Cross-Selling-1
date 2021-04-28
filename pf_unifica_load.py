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
        
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.txt'):
            filename = file
            
        df = pd.read_csv(filename, delimiter='|', dtype=str, encoding='latin-1')
        
        return df