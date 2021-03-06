from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import csv

class intervencion_tdc_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        self.crear_excel(ruta)
        self.ruta = ruta
        input("Vacíe la información necesaria en el archivo de excel llamado 'intervencion_tdc_llenar.xlsx' recién creado en la ruta:\n\n" + ruta + "\n\nluego presione Enter")
        print("Creando intervencion tdc\n")
        self.df = pd.read_excel(self.ruta + '\intervencion_tdc_llenar.xlsx', usecols = 'A,B', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.df['montoVenta'] = self.df['montoVenta'].astype(float)
        self.df['rif'] = self.df['rif'].str.strip()
        
        print("Intervención tdc venta: ", self.df['montoVenta'].sum(), "\n")
        
        self.df = self.recorrerDF(self.df)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df = self.df.rename(columns={'MisCliente': 'mis', 'montoVenta': 'monto'})
        self.df = self.df.groupby(['mis'], as_index=False).agg({'monto': sum})
        self.df = self.df[(self.df["monto"] > 0)]
            
        self.df = self.df.assign(fecha = fecha)
        
    def get_monto(self):
        df = self.df.groupby(['mis'], as_index=False).agg({'monto': sum})
        df['monto'] = df['monto'].astype(str)
        for i in range(len(df['monto'])):
            df['monto'][i]=df['monto'][i].replace('.',',')
            
        return df.rename(columns={'monto': 'Intervención TDC Venta'})
        
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'Intervención TDC Venta'})
        
        return df.groupby(['mis'], as_index=False).agg({'Intervención TDC Venta': 'first'})

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
        writer = pd.ExcelWriter(ruta + '\intervencion_tdc_llenar.xlsx')
        df = pd.DataFrame(columns = ['rif', 'montoVenta'])
        df.to_excel(writer, index=False)
        writer.save()
    
    def to_csv(self):
        self.df.to_csv(self.ruta + '\\rchivos csv\intervencion_tdc.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    def insertPg(self, conector):
        print("Insertando intervención tdc")
        for indice_fila, fila in self.df.iterrows():
            try:
                conector.cursor.execute("INSERT INTO INTERVENCION_TDC (int_mis, int_monto, int_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("intervencion tdc")
            finally:
                conector.conn.commit()