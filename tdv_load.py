import pandas as pd
from rrgg.rrgg_corporativo_load import rrgg_corporativo_load
from rrgg.rrgg_empresa_load import rrgg_empresa_load
from rrgg.rrgg_institucional_load import rrgg_institucional_load
from rrgg.rrgg_pyme_load import rrgg_pyme_load

class tdv_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando TDV")
        self.ruta = ruta
        self.corporativo = rrgg_corporativo_load(self.ruta, cartera)
        self.empresa = rrgg_empresa_load(self.ruta, cartera)
        self.institucional = rrgg_institucional_load(self.ruta, cartera)
        self.pyme = rrgg_pyme_load(self.ruta, cartera)
        self.df = pd.concat([self.corporativo.df, self.empresa.df, self.institucional.df, self.pyme.df]).groupby(['mis']).sum().reset_index()
        self.df = self.df.assign(fecha = fecha)
    
    def to_csv(self):
        self.df.to_csv(self.ruta + '\\rchivos csv\\tdv.csv', index = False, header=True, sep='|')