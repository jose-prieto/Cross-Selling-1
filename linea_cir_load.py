import pandas as pd
import glob as gb

class linea_cir_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando lineas CIR")
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\REPORTES DE CIR'
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'G,J,T,X', header=0, sheet_name = "CONSOLIDADO", index_col=False, skiprows=11, keep_default_na=True, dtype=str)
        self.df = self.df[(self.df["ESTATUS"] == "VIGENTE")]
        self.df = self.df.rename(columns={self.df.columns[0]: 'estatus', self.df.columns[1]: 'mis', self.df.columns[2]: 'montoBs', self.df.columns[3]: 'montoDolar'})
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df['montoBs'] = self.df['montoBs'].astype(float)
        self.df['montoDolar'] = self.df['montoDolar'].astype(float)
        self.dfBs = self.df.groupby(['mis'], as_index=False).agg({'montoBs': sum})
        self.dfBs = self.dfBs.rename(columns={'montoBs': 'monto'})
        self.dfBs = self.dfBs.assign(fecha = fecha)
        self.dfBs['monto'] = self.dfBs['monto'].astype(str)
        for i in range(len(self.dfBs['monto'])):
            self.dfBs['monto'][i]=self.dfBs['monto'][i].replace('.',',')
            
        self.dfDolar = self.df.groupby(['mis'], as_index=False).agg({'montoDolar': sum})
        self.dfDolar = self.dfBs.rename(columns={'montoDolar': 'monto'})
        self.dfDolar = self.dfDolar.assign(fecha = fecha)
        self.dfDolar['monto'] = self.dfDolar['monto'].astype(str)
        for i in range(len(self.dfDolar['monto'])):
            self.dfDolar['monto'][i]=self.dfDolar['monto'][i].replace('.',',')
    
    def to_csv(self):
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\lineaBs.csv', index = False, header=True, sep='|')
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\lineaDolar.csv', index = False, header=True, sep='|')
    
#pf = linea_cir_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero').df