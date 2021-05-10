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
        self.df = self.df[(self.df["CI O RIF"].str.startswith(("J", "R", "G", "F")))]
        self.df = self.df.rename(columns={'MIS': 'mis', 'VIGENTE': 'monto'})
        self.df['monto'] = self.df['monto'].astype(float)
        print("inventario Total: ", self.df['monto'].sum())
        
        self.dfDolar = self.df[(self.df["PRODUCTO AJUSTADO"] == "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        self.dfDolar = self.dfDolar.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("inventario Dolar: ", self.dfDolar['monto'].sum())
        self.dfDolar['monto'] = self.dfDolar['monto'].astype(str)
        self.dfDolar = pd.merge(self.dfDolar, cartera, how='inner', right_on='MisCliente', left_on='mis')
        for i in range(len(self.dfDolar['monto'])):
            self.dfDolar['monto'][i]=self.dfDolar['monto'][i].replace('.',',')
            
        self.dfBs = self.df[(self.df["PRODUCTO AJUSTADO"] != "CRÉDITOS EN CUOTAS MONEDA EXTRANJERA")]
        self.dfBs = self.dfBs.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("inventario Bs: ", self.dfBs['monto'].sum(), "\n")
        self.dfBs['monto'] = self.dfBs['monto'].astype(str)
        self.dfBs = pd.merge(self.dfBs, cartera, how='inner', right_on='MisCliente', left_on='mis')
        for i in range(len(self.dfBs['monto'])):
            self.dfBs['monto'][i]=self.dfBs['monto'][i].replace('.',',')
            
        self.dfMonto = pd.merge(self.dfBs.rename(columns={'monto': 'Crédito Vigente'}), self.dfDolar.rename(columns={'monto': 'Crédito en Moneda Extranjera USD'}), how='outer', right_on='mis', left_on='mis')
        
        self.dfBs = self.dfBs.assign(fecha = fecha)
        self.dfDolar = self.dfDolar.assign(fecha = fecha)
    
    def to_csv(self):
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\credito_dolar.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\credito_vigente.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#todo = ah_unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#bs = todo.dfBs
#dolar = todo.dfDolar