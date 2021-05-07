import pandas as pd
import csv

class exportacion_dolar_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        self.crear_excel(ruta)
        self.ruta = ruta
        input("Vacíe la información necesaria en el archivo de excel llamado 'exportacion_dolar.xlsx' recién creado en la ruta:\n\n" + ruta + "\n\nluego presione Enter")
        print("Creando exportación dolar\n")
        self.df = pd.read_excel(self.ruta + '\exportacion_dolar.xlsx', usecols = 'A:C', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.recorrerDF(self.df)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df['montoCompra'] = self.df['montoCompra'].astype(float)
        self.df['montoVenta'] = self.df['montoVenta'].astype(float)
        self.dfCompra = self.df.groupby(['MisCliente'], as_index=False).agg({'montoCompra': sum})
        self.dfCompra = self.dfCompra.rename(columns={'montoCompra': 'monto', 'MisCliente': 'mis'})
        self.dfCompra['monto'] = self.dfCompra['monto'].astype(str)
        for i in range(len(self.dfCompra['monto'])):
            self.dfCompra['monto'][i]=self.dfCompra['monto'][i].replace('.',',')
        self.dfVenta = self.df.groupby(['MisCliente'], as_index=False).agg({'montoVenta': sum})
        self.dfVenta = self.dfVenta.rename(columns={'montoVenta': 'monto', 'MisCliente': 'mis'})
        self.dfVenta['monto'] = self.dfVenta['monto'].astype(str)
        for i in range(len(self.dfVenta['monto'])):
            self.dfVenta['monto'][i]=self.dfVenta['monto'][i].replace('.',',')
            
        self.dfMonto = pd.merge(self.dfCompra.rename(columns={'monto': 'Intervención 20% Exportación Compra (USD)'}), self.dfVenta.rename(columns={'monto': 'Intervención 20% Exportación Venta (USD)'}), how='outer', right_on='mis', left_on='mis')
            
        self.dfVenta = self.dfVenta.assign(fecha = fecha)
        self.dfCompra = self.dfCompra.assign(fecha = fecha)

    def quitarCeros(self, rifCliente):
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"rif"] = self.quitarCeros(fila["rif"])
        return df
        
    def crear_excel(self, ruta):
        writer = pd.ExcelWriter(ruta + '\exportacion_dolar.xlsx')
        df = pd.DataFrame(columns = ['rif', 'montoCompra', 'montoVenta'])
        df.to_excel(writer, index=False)
        writer.save()
    
    def to_csv(self):
        self.dfCompra.to_csv(self.ruta + '\\rchivos csv\custodiaDolar.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfVenta.to_csv(self.ruta + '\\rchivos csv\custodiaEuro.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)