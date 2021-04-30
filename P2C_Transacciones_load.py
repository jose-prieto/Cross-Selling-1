import pandas as pd

class P2C_Transacciones_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\P2C_Transaccion'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_excel(self.ruta + self.nombre_archivo + 'es enero.xlsx', usecols = 'C,D', header=0, index_col=False, keep_default_na=True)
    
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"RIF"] = self.quitarCeros(fila["RIF"])
        return df
    
    def make_DF(self):
        print("Creando p2c")
        self.df['Monto de la operacion'] = self.df['Monto de la operacion'].astype(float)
        self.df = self.df.groupby('RIF', as_index=False)[['Monto de la operacion']].sum()
        self.df = self.recorrerDF(self.df)
        return self.df
    
#p = P2C_Transacciones_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#p2c = p.make_DF()