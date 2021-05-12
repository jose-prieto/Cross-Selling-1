import pandas as pd
import glob as gb
import csv

class inventario_ajustado_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        input("Quitar los números del archivo de inventario ajustado (Debe empezar en 'I')\n")
        print("Creando inventario ajustado")
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\INVENTARIO AJUSTADO'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'A:AJ', header=0, index_col=False, keep_default_na=True, sheet_name="INVENTARIO_DEL_DÍA", dtype=str)
        self.df['CI O RIF'] = self.df['CI O RIF'].str.strip()
        self.df = self.df[(self.df["CI O RIF"].str.startswith(("J", "R", "G", "F")))]
        self.df = self.df.rename(columns={'MIS': 'mis', 'VIGENTE': 'monto'})
        self.df['monto'] = self.df['monto'].astype(float)
        print("inventario Total: ", self.df['monto'].sum())
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        
        self.dfDolar = self.df[(self.df["PRODUCTO AJUSTADO"] == "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        self.dfBs = self.df[(self.df["PRODUCTO AJUSTADO"] != "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        
        self.df = self.df.assign(fecha = fecha)
        
    def get_monto(self):
        dfDolar = self.dfDolar.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("inventario Dolar: ", dfDolar['monto'].sum())
        dfDolar['monto'] = dfDolar['monto'].astype(str)
        for i in range(len(dfDolar['monto'])):
            dfDolar['monto'][i]=dfDolar['monto'][i].replace('.',',')
            
        dfBs = self.dfBs.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("inventario Bs: ", dfBs['monto'].sum(), "\n")
        dfBs['monto'] = dfBs['monto'].astype(str)
        for i in range(len(dfBs['monto'])):
            dfBs['monto'][i]=dfBs['monto'][i].replace('.',',')
            
        return pd.merge(dfBs.rename(columns={'monto': 'Crédito Vigente'}), dfDolar.rename(columns={'monto': 'Crédito en Moneda Extranjera USD'}), how='outer', right_on='mis', left_on='mis')
    
    def get_usable(self):
        dfDolar = self.dfDolar.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfDolar = dfDolar.assign(uso = 1)
        dfDolar = dfDolar.rename(columns={'uso': 'Crédito en Moneda Extranjera USD'})
        dfDolar = dfDolar.groupby(['mis'], as_index=False).agg({'Crédito en Moneda Extranjera USD': 'first'})
        
        dfBs = self.dfBs.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfBs = dfBs.assign(uso = 1)
        dfBs = dfBs.rename(columns={'uso': 'Crédito Vigente'})
        dfBs = dfBs.groupby(['mis'], as_index=False).agg({'Crédito Vigente': 'first'})
        
        return pd.merge(dfBs, dfDolar, how='outer', right_on='mis', left_on='mis')
    
    def to_csv(self):
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\credito_dolar.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\credito_vigente.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#todo = ah_unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#bs = todo.dfBs
#dolar = todo.dfDolar