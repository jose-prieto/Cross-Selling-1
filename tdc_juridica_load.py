import pandas as pd
import glob as gb
import csv

class tdc_juridica_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando tdc juridica")
        self.fecha = fecha
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\Maestro de Tarjetas Clientes'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'B', header=0, sheet_name = "TDC ACTIVAS", index_col=False, keep_default_na=True, dtype=str)
        self.df = self.df.rename(columns={"Codigo cliente": 'mis'})
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df = self.df.groupby(['mis'], as_index=False).agg({'mis': 'first'})
    
    def to_csv(self):
        df = self.df.assign(TDC_Jurifica = 1)
        self.df = self.df.assign(fecha = self.fecha)
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\\tdc_juridico.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        return df
    
#pf = linea_cir_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero').df