import pandas as pd
import glob as gb

class P2C_Transacciones_load:
    
    #Constructor
    def __init__(self, ruta):
        print("Creando p2c")
        self.nombre_archivo = '\P2C_'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'C,D', header=0, index_col=False, keep_default_na=True)
        self.df['Monto de la operacion'] = self.df['Monto de la operacion'].astype(float)
        self.df = self.df.groupby('RIF', as_index=False)[['Monto de la operacion']].sum()
        self.df = self.recorrerDF(self.df)
    
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"RIF"] = self.quitarCeros(fila["RIF"])
        return df
    
    def to_csv(self, cartera):
        print("Creando cruce cartera y p2c")
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='RIF')
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\p2c.csv', index = False, header=True, sep='|')
        return self.df
    
#p2c = P2C_Transacciones_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero').to_csv()