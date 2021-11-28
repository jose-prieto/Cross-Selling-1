import pyodbc as pdbc
import pandas as pd
import numpy as np
import glob as gb
import csv

class cartera_cliente_load:
    
    #Constructor
    def __init__(self, ruta, db, fecha):
        print("Creando cartera")
        self.nombre_archivo = '\Base'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.accdb'):
            self.ruta = file
        self.df = ""
        
        """try:
            self.conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.ruta)
            self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "NombreCliente", "MIS Grupo", "Grupo Economico", "Cod Of", "Segmento", "Unidad De Negocio", "Región", "Código de BC", "Nombre completo", "Título", "Tipo de Atención" FROM ' + db + ' WHERE "Estatus Cliente" <> ?', self.conn, params=["Cancelado"])
        except Exception as err:
            print(err)
            input("Error presione contrl + C")
        finally:
            self.conn.close()"""
            
        try:
            self.conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + self.ruta)
            opcion = input("1: Todos los activos menos personas y banca premium\n2: Personas y Banca premium y .CSV\n")
            if (opcion == "1"):
                self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "Estatus Cliente", "NombreCliente", "MIS Grupo", "Grupo Economico", "Cod Of", "Segmento", "Unidad De Negocio", "Región", "Código de BC", "Nombre completo", "Título", "Tipo de Atención" FROM ' + db + ' WHERE ("Segmento" = ? OR "Segmento" = ? OR "Segmento" = ? OR "Segmento" = ? OR "Segmento" = ? OR "Título" = ?) AND "Estatus Cliente" = ?', self.conn, params=["CORPORATIVO", "EMPRESA", "INSTITUCIONAL", "PYME", "MICROEMPRESARIO POPULAR", "Asesor de Negocios Comerciales", "Activo"])
            elif (opcion == "2"):
                self.df = pd.read_sql('SELECT "MisCliente", "CedulaCliente", "Estatus Cliente", "NombreCliente", "MIS Grupo", "Grupo Economico", "Cod Of", "Segmento", "Unidad De Negocio", "Región", "Código de BC", "Nombre completo", "Título", "Tipo de Atención" FROM ' + db + ' WHERE "Estatus Cliente" = ?', self.conn, params=["Activo"])
            else:
                print("Opción equivocada.")
        except Exception as err:
            print(err)
            input("Error presione contrl + C")
        finally:
            self.conn.close()
        
        self.df['Cod Of'] = np.where((self.df['Nombre completo'] == 'ADAN BORGES, ETTSAIDA ELIANA') | (self.df['Nombre completo'] == 'FUENTES PEREZ, JAVIER ANTONIO') | (self.df['Nombre completo'] == 'WENDY, VELIZ'), 'No Gestionable', self.df['Cod Of'])
        
        self.df['CedulaCliente'] = self.df['CedulaCliente'].str.strip()
        self.df['MIS Grupo'] = np.where(self.df['MIS Grupo'] == 'No Tiene', 0, self.df['MIS Grupo'])
        self.df['MIS Grupo'] = np.where(self.df['MIS Grupo'] == '', 0, self.df['MIS Grupo'])
        self.df['Código de BC'] = self.df['Código de BC'].str.replace('bc','')
        self.df['Grupo Economico'] = np.where(self.df['Grupo Economico'] == 'No Tiene', self.df['NombreCliente'], self.df['Grupo Economico'])
        self.df['Grupo Economico'] = np.where(self.df['Grupo Economico'] == '', self.df['NombreCliente'], self.df['Grupo Economico'])
        self.df['Grupo Economico'] = np.where(self.df['Grupo Economico'] == 0, self.df['NombreCliente'], self.df['Grupo Economico'])
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
    
    def to_csv(self, df):
        clienteDf = df.groupby(['MIS'], as_index=False).agg({'Mes': 'first', 
                                                                    'CedulaCliente': 'first', 
                                                                    'NOMBRE DEL CLIENTE': 'first',
                                                                    'MIS GRUPO': 'first',
                                                                    'GRUPO': 'first',
                                                                    'Segmento': 'first',
                                                                    'OFICINA': 'first',
                                                                    'CARTERA': 'first',
                                                                    'VICEPRESIDENCIA': 'first',
                                                                    'MIS Responsable': 'first',
                                                                    'RESPONSABLE': 'first',
                                                                    'Título Responsable': 'first',
                                                                    'Tipo de Atención': 'first'})
        clienteDf.to_csv(self.rutaOrigin + '\\rchivos csv\clientes.csv', index = False, header=True, sep='|', encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
            
    def insertPg(self, conector, df):
        print("Insertando clientes")
        for indice_fila, fila in df.iterrows():
            try:
                conector.cursor.execute("INSERT INTO CLIENTE (mis, cedula, nombre, mis_grupo, grupo, fecha, segmento, oficina, cartera, vicepresidencia, responsable, mis_responsable, titulo, tipo_atencion) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                               (fila["MIS"], 
                               fila["CedulaCliente"], 
                               fila["NOMBRE DEL CLIENTE"], 
                               fila["MIS GRUPO"], 
                               fila["GRUPO"],
                               fila["Mes"], 
                               fila["Segmento"], 
                               fila["OFICINA"], 
                               fila["CARTERA"], 
                               fila["VICEPRESIDENCIA"], 
                               fila["RESPONSABLE"],
                               fila["MIS Responsable"],
                               fila["Título Responsable"], 
                               fila["Tipo de Atención"], 
                               ))
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("cartera")
                input("Empieza cartera2")
            finally:
                conector.conn.commit()
            
#cartera = cartera_cliente_load(r'C:\Users\bc221066\Documents\José Prieto\Cross Selling\Enero', 'fesfefs', 'Base_Clientes', '29/01/2021').to_csv()