import pandas as pd

class P2C_Transacciones_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\P2C_Transaccion'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (aux[0] == '0'):
            aux = aux[1:]
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"RIF"] = self.quitarCeros(fila["RIF"])
        return df
    
    def make_DF(self):
        print("Creando p2c")
        df = pd.read_excel(self.ruta + self.nombre_archivo + 'es enero.xlsx', usecols = 'C,D', header=0, index_col=False, keep_default_na=True)
        df['Monto de la operacion'] = df['Monto de la operacion'].astype(float)
        df = df.groupby('RIF', as_index=False)[['Monto de la operacion']].sum()
        df = self.recorrerDF(df)
        return df
    
#p = P2C_Transacciones_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#p2c = p.make_DF()