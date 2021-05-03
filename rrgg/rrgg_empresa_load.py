import pandas as pd
import glob as gb

class rrgg_empresa_load:
    
    #Constructor
    def __init__(self, ruta, cartera):
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\rrgg empresa'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xls'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'A,G,H', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.df = self.df[(self.df["Producto Ajustado"] == "TDV")]
        self.df = self.df.rename(columns={'Mis': 'mis', 'Monto': 'monto'})
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df['monto'] = self.df['monto'].astype(float)
        self.df = self.df.groupby(['mis'], as_index=False).agg({'monto': sum})
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\rrgg_empresa.csv', index = False, header=True, sep='|')

#rrgg_empresa = rrgg_empresa_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').df