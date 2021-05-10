import pandas as pd
import csv

class mesa_cambio_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        self.crear_excel(ruta)
        self.ruta = ruta
        input("Vacíe la información necesaria en el archivo de excel llamado 'mesa_cambio_llenar.xlsx' recién creado en la ruta:\n\n" + ruta + "\n\nluego presione Enter")
        print("Creando mesa de cambio\n")
        self.df = pd.read_excel(self.ruta + '\mesa_cambio_llenar.xlsx', usecols = 'A:C', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.df['montoCompra'] = self.df['montoCompra'].astype(float)
        self.df['montoVenta'] = self.df['montoVenta'].astype(float)
        print("Mesa de cabio compra monto: ", self.df['montoCompra'].sum())
        print("Mesa de cabio venta monto: ", self.df['montoVenta'].sum())
        
        self.df = self.recorrerDF(self.df)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df = self.df.rename(columns={'MisCliente': 'mis'})
        self.df = self.df.groupby(['mis'], as_index=False).agg({'montoCompra': sum, 'montoVenta':sum})
            
        self.df = self.df.assign(fecha = fecha)
        
    def get_monto(self):
        dfCompra = self.df.groupby(['mis'], as_index=False).agg({'montoCompra': sum})
        dfCompra = dfCompra.rename(columns={'montoCompra': 'monto'})
        
        dfVenta = self.df.groupby(['mis'], as_index=False).agg({'montoVenta': sum})
        dfVenta = dfVenta.rename(columns={'montoVenta': 'monto'})
        
        dfCompra['monto'] = dfCompra['monto'].astype(str)
        for i in range(len(dfCompra['monto'])):
            dfCompra['monto'][i]=dfCompra['monto'][i].replace('.',',')
            
        dfVenta['monto'] = dfVenta['monto'].astype(str)
        for i in range(len(dfVenta['monto'])):
            dfVenta['monto'][i]=dfVenta['monto'][i].replace('.',',')
            
        return pd.merge(dfCompra.rename(columns={'monto': 'Mesa de Cambio Compra (USD)'}), dfVenta.rename(columns={'monto': 'Mesa de Cambio Venta (USD)'}), how='outer', right_on='mis', left_on='mis')
        
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'Mesa de Cambio (USD)'})
        
        return df.groupby(['mis'], as_index=False).agg({'Mesa de Cambio (USD)': 'first'})

    def quitarCeros(self, rifCliente):
        aux = rifCliente
        while (rifCliente[0] == " "):
            aux = rifCliente[1:]
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"rif"] = self.quitarCeros(fila["rif"])
        return df
        
    def crear_excel(self, ruta):
        writer = pd.ExcelWriter(ruta + '\mesa_cambio_llenar.xlsx')
        df = pd.DataFrame(columns = ['rif', 'montoCompra', 'montoVenta'])
        df.to_excel(writer, index=False)
        writer.save()
    
    def to_csv(self):
        self.dfCompra.to_csv(self.ruta + '\\rchivos csv\custodiaDolar.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfVenta.to_csv(self.ruta + '\\rchivos csv\custodiaEuro.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)