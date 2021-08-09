from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import glob as gb
import csv

class tdc_juridica_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando tdc juridica")
        self.fecha = fecha
        self.rutaOrigin = ruta
        self.ruta = ruta
        self.nombre_archivo = '\\Maestro de Tarjetas Clientes'
        ruta_cambiante = self.ruta
        for file in gb.glob(ruta_cambiante + self.nombre_archivo + '*.xlsx'):
            ruta_cambiante = file
        self.df = pd.read_excel(ruta_cambiante, usecols = 'A:O', header=0, sheet_name = "CUENTAS MADRES JURIDICAS", index_col=False, keep_default_na=True, dtype=str)
        self.df = self.df.rename(columns={"Codigo cliente": 'mis'})
        print("TDC Juridico totales: ", len(self.df.index))
        
        ruta_cambiante = self.ruta
        self.nombre_archivo = '\\Maestro de Tarjetas MDP'
        for file in gb.glob(ruta_cambiante + self.nombre_archivo + '*.xlsx'):
            ruta_cambiante = file
        self.dfPersona = pd.read_excel(ruta_cambiante, usecols = 'A:O', header=0, index_col=False, keep_default_na=True, dtype=str)
        self.dfPersona = self.dfPersona.rename(columns={"Codigo cliente": 'mis'})
        print("TDC Personas totales: ", len(self.dfPersona.index))
        
        self.df = pd.concat([self.df, self.dfPersona]).groupby(['mis']).sum().reset_index()
        
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        
        self.df = self.df.groupby(['mis'], as_index=False).agg({'mis': 'first'})
        
        self.df = self.df.assign(fecha = self.fecha)
    
    def get_usable(self):
        df = self.df.assign(uso = 1)
        df = df.rename(columns={'uso': 'TDC Jurídica'})
        
        return df.groupby(['mis'], as_index=False).agg({'TDC Jurídica': 'first'})
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\\tdc_juridico.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
    def insertPg(self, conector):
        print("Insertando tdc")
        for indice_fila, fila in self.df.iterrows():
            try:
                conector.cursor.execute("INSERT INTO TDC (tdc_mis, tdc_fecha) VALUES(%s, %s)", 
                               (fila["mis"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("tdc")
            finally:
                conector.conn.commit()
    
#pf = linea_cir_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero').df