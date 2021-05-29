import pandas as pd
import glob as gb
import pyodbc as pdbc
import csv

class cartera_cliente_load:
    
    #Constructor
    def __init__(self, ruta, rutadb, db, fecha):
        print("Creando cartera")
        self.rutadb = rutadb
        #self.nombre_archivo = '\Cartera_Cliente'
        self.nombre_archivo = '\Cartera_'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.accdb'):
            self.ruta = file
        self.conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.ruta)
        #self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "MIS Grupo", "Grupo Economico", "Cod Of", "Segmento", "Unidad De Negocio", "Región", "Nombre completo" FROM ' + db + ' WHERE "Título" = ?', self.conn, params=["Asesor de Negocios Comerciales"])
        self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "Segmento Mis", "Unidad De Negocio", "Region", "Nombre del Responsable" FROM ' + db + ' WHERE "TipoResp" = ?', self.conn, params=["Asesor de Negocios Comerciales"])
        self.df['CedulaCliente'] = self.df['CedulaCliente'].str.strip()
        self.df = self.recorrerDF(self.df)
        self.df['MisCliente'] = self.df['MisCliente'].astype(str)
        
        self.df = self.df.assign(fecha = fecha)

    def quitarCeros(self, rifCliente):
        if not rifCliente:
            return rifCliente
        aux = rifCliente[1:]
        while (len(aux) < 9):
            aux = '0' + aux
        return rifCliente[0] + aux
    
    def recorrerDF(self, df):
        for indice_fila, fila in df.iterrows():
            df.at[indice_fila,"CedulaCliente"] = self.quitarCeros(fila["CedulaCliente"])
        return df
    
    def to_csv(self):
        self.df.to_csv(self.rutaOrigin + '\\rchivos csv\cartera.csv', index = False, header=True, sep='|', encoding='UTF-8', quoting=csv.QUOTE_NONE)
    
    def insertDf(self):
        conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.rutadb)
        cursor = conn.cursor()
        try:
            for indice_fila, fila in self.df.iterrows():
                try:
                    cursor.execute("INSERT INTO CARTERA ([mis], [rif], [nombre], [segmento], [unidad], [region], [tipo_atencion]) VALUES(?,?,?,?,?,?,?)", 
                                   fila["MisCliente"], 
                                   fila["CedulaCliente"], 
                                   fila["NombreCliente"], 
                                   fila["Segmento Mis"], 
                                   fila["Unidad De Negocio"], 
                                   fila["Region"], 
                                   fila["Tipo_Atencion"],
                                   fila["Nombre del Responsable"])
                except KeyError as llave:
                    print(type(llave))
                    print(llave.args)
                    print(llave)
                    print("Llave primaria")
                except Exception as excep:
                    print(type(excep))
                    print(excep.args)
                    print(excep)
                finally:
                    conn.commit()
        except KeyError as llave:
            print(type(llave))
            print(llave.args)
            print(llave)
        finally:
            conn.close()
            

#cartera = cartera_cliente_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo', 'Cartera_Clientes_Marzo_2021').to_csv()