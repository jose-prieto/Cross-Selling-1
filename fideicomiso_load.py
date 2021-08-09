from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import glob as gb
import csv

class fideicomiso_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando fideicomiso")
        self.fecha = fecha
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\REPORTE DE CAPITALES '
        for file in gb.glob(self.ruta + self.nombre_archivo + '*.xlsx'):
            self.ruta = file
        self.df = pd.read_excel(self.ruta, usecols = 'B,C,E', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.df = self.df.rename(columns={self.df.columns[0]: 'letra', self.df.columns[1]: 'rif', self.df.columns[2]: 'monto'})
        self.df["rif"] = self.df["letra"] + self.df["rif"]
        self.df['monto'] = self.df['monto'].astype(float)
        self.df = self.df[(self.df["monto"] > 0)]
        self.df = self.recorrerDF(self.df)
        
        print("Total fideicomiso: ", self.df['monto'].sum(), "\n")
        
        self.df = pd.merge(self.df, cartera, how='inner', right_on='CedulaCliente', left_on='rif')
        self.df = self.df.rename(columns={'MisCliente': 'mis'})
        self.df = self.df.groupby(['mis'], as_index=False).agg({'monto': sum})
        
        self.df = self.df.assign(fecha = self.fecha)

    def quitarCeros(self, rifCliente):
        if not rifCliente:
            return rifCliente
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"rif"] = self.quitarCeros(fila["rif"])
        return df
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'Fideicomiso'})
        df = df.groupby(['mis'], as_index=False).agg({'Fideicomiso': sum})
        
        return df
        
    def get_monto(self):
        df = self.df
        df['monto'] = df['monto'].astype(str)
        for i in range(len(df['monto'])):
            df['monto'][i]=df['monto'][i].replace('.',',')
            
        df = df.rename(columns={'monto': 'Fideicomiso'})
        
        return df.groupby(['mis'], as_index=False).agg({'Fideicomiso': 'first'})
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\\fideicomiso.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    def insertPg(self, conector):
        print("Insertando fideicomiso")
        for indice_fila, fila in self.df.iterrows():
            try:
                conector.cursor.execute("INSERT INTO FIDEICOMISO (fid_mis, fid_monto, fid_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                                fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("fideicomiso")
            finally:
                conector.conn.commit()
    
#pf = linea_cir_load(r'C:\Users\José Prieto\Documents\Bancaribe\Enero', "29/01/2021").df