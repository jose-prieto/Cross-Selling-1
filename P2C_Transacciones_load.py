import pandas as pd
import glob as gb
import csv

class P2C_Transacciones_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando p2c")
        self.nombre_archivo = '\P2C_'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'C,D', header=0, index_col=False, keep_default_na=True)
        self.df['Monto de la operacion'] = self.df['Monto de la operacion'].astype(float)
        self.df = self.df.rename(columns={'RIF': 'rif', 'Monto de la operacion': 'monto'})
        self.df = self.recorrerDF(self.df)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df = self.df.groupby(['rif'], as_index=False).agg({'monto': sum})
        self.df = self.df.assign(fecha = fecha)
        self.df['monto'] = self.df['monto'].astype(str)
        for i in range(len(self.df['monto'])):
            self.df['monto'][i]=self.df['monto'][i].replace('.',',')
    
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"rif"] = self.quitarCeros(fila["rif"])
        return df
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\p2c.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#p2c = P2C_Transacciones_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').to_csv()