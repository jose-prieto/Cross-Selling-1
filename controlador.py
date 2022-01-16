from dbConnector import dbConnector
from cargaDatos import cargaDatos
from psycopg2 import Error
from pathlib import Path
import pandas as pd

class controlador:
    
    def __init__(self, ruta, fecha):
        self.ruta = ruta + '\\rchivos csv'
        Path(self.ruta).mkdir(parents=True, exist_ok=True)
        
        self.ruta = ruta
        self.db = "Base_Clientes"
        self.fecha = fecha
        
        self.cargaDatos = ""
        self.unifica = ""
        self.tdv = ""
        self.mesa_cambio = ""
        self.exportacion = ""
        self.intervencion_tdc = ""
        self.intervencion_euro = ""
        self.custodia = ""
        self.inventario = ""
        self.linea_cir = ""
        self.tdc_juridica = ""
        self.cash = ""
        self.puntos_venta = ""
        self.ivr_conexion = ""
        self.p2c = ""
        self.p2p = ""
        self.fideicomiso = ""
        
        self.recargar_datos()
        
    def recargar_datos(self):
        self.cargaDatos = cargaDatos(self.ruta, self.fecha, self.db)
        
        self.unifica = self.cargaDatos.unifica()
        self.tdv = self.cargaDatos.tdv()
        self.mesa_cambio = self.cargaDatos.mesa_cambio()
        self.exportacion = self.cargaDatos.exportacion()
        self.intervencion_tdc = self.cargaDatos.intervencion_tdc()
        self.intervencion_euro = self.cargaDatos.intervencion_euro()
        self.custodia = self.cargaDatos.custodia()
        self.inventario = self.cargaDatos.inventario()
        self.originacion = self.cargaDatos.originacion()
        self.linea_cir = self.cargaDatos.linea_cir()
        self.tdc_juridica = self.cargaDatos.tdc_juridica()
        self.cash = self.cargaDatos.cash()
        self.puntos_venta = self.cargaDatos.puntos_venta()
        self.ivr_conexion = self.cargaDatos.ivr_conexion()
        self.p2c = self.cargaDatos.p2c()
        self.p2p = self.cargaDatos.p2p()
        self.fideicomiso = self.cargaDatos.fideicomiso()
        
        self.cargaDatos.cartera.df = self.cargaDatos.cartera.df.groupby(['MisCliente'], as_index=False).agg({'fecha': 'first', 
                                                                                          'CedulaCliente': 'first', 
                                                                                          'NombreCliente': 'first',
                                                                                          'MIS Grupo': 'first',
                                                                                          'Grupo Economico': 'first',
                                                                                          'Segmento': 'first',
                                                                                          'Unidad De Negocio': 'first',
                                                                                          'Cod Of': 'first',
                                                                                          'Región': 'first',
                                                                                          'Código de BC': 'first',
                                                                                          'Nombre completo': 'first',
                                                                                          'Título': 'first',
                                                                                          'Tipo de Atención': 'first',
                                                                                          'Estatus Cliente': 'first'})
        
        self.cargaDatos.cartera.df = self.cargaDatos.cartera.df.rename(columns={'MisCliente': 'MIS', 
                                                                                'fecha': 'Mes', 
                                                                                'Cod Of': 'CARTERA',
                                                                                'MIS Grupo': 'MIS GRUPO',
                                                                                'Grupo Economico': 'GRUPO',
                                                                                'NombreCliente': 'NOMBRE DEL CLIENTE', 
                                                                                'Unidad De Negocio': 'OFICINA', 
                                                                                'Región': 'VICEPRESIDENCIA', 
                                                                                'Nombre completo': 'RESPONSABLE', 
                                                                                'Código de BC': 'MIS Responsable',
                                                                                'Título': 'Título Responsable'})
    
    def crear_cartera_montos(self):
        carteraMonto = self.unifica.get_monto()
        carteraMonto = pd.merge(carteraMonto, self.tdv.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.mesa_cambio.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.exportacion.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_tdc.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_euro.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.custodia.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.inventario.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.originacion.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.linea_cir.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cash.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.puntos_venta.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2c.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2p.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.fideicomiso.get_monto(), how='outer', left_on='mis', right_on='mis')
        return carteraMonto
    
    def crear_cartera_clientes(self):
        carteraMonto = self.unifica.get_usable()
        carteraMonto = pd.merge(carteraMonto, self.tdv.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.mesa_cambio.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.exportacion.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_tdc.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_euro.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.custodia.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.inventario.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.originacion.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.linea_cir.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.tdc_juridica.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cash.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.puntos_venta.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.ivr_conexion.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2c.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2p.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.fideicomiso.get_usable(), how='outer', left_on='mis', right_on='mis')
        return carteraMonto
        
    def crear_excel(self, df, segmento):
        print("Creando excel")
        clientes = pd.merge(df, self.crear_cartera_clientes(), how='inner', left_on='MIS', right_on='mis').fillna(0)
        montos = pd.merge(df, self.crear_cartera_montos(), how='inner', left_on='MIS', right_on='mis').fillna(0)
        print("montos luego: ",len(clientes.index))
        print("usables luego: ",len(montos.index))
        
        writer = pd.ExcelWriter(self.ruta + '\\rchivos csv\Cross-Selling-' + segmento + '-Noviembre-2021.xlsx')
        clientes.to_excel(writer, sheet_name="CS Clientes", index=False)
        montos.to_excel(writer, sheet_name="Montos por Producto Cliente", index=False)
        writer.save()
        
    def crear_csv(self, df):
        self.cargaDatos.cartera.to_csv(df)
        self.unifica.to_csv(df)
        self.tdv.to_csv(df)
        self.mesa_cambio.to_csv(df)
        self.exportacion.to_csv(df)
        self.intervencion_tdc.to_csv(df)
        self.intervencion_euro.to_csv(df)
        self.custodia.to_csv(df)
        self.inventario.to_csv(df)
        self.originacion.to_csv(df)
        self.linea_cir.to_csv(df)
        self.tdc_juridica.to_csv(df)
        self.cash.to_csv(df)
        self.puntos_venta.to_csv(df)
        self.ivr_conexion.to_csv(df)
        self.p2c.to_csv(df)
        self.p2p.to_csv(df)
        self.fideicomiso.to_csv(df)
        
    def insertPg(self, df, db):
        try:
            conector = dbConnector(db)
            conector.pgConn()
            self.cargaDatos.cartera.insertPg(conector,df)
            self.unifica.insertPg(conector)
            self.tdv.insertPg(conector)
            self.mesa_cambio.insertPg(conector)
            self.exportacion.insertPg(conector)
            self.intervencion_tdc.insertPg(conector)
            self.intervencion_euro.insertPg(conector)
            self.custodia.insertPg(conector)
            self.inventario.insertPg(conector)
            self.originacion.insertPg(conector)
            self.linea_cir.insertPg(conector)
            self.tdc_juridica.insertPg(conector)
            self.cash.insertPg(conector)
            self.puntos_venta.insertPg(conector)
            self.ivr_conexion.insertPg(conector)
            self.p2c.insertPg(conector)
            self.p2p.insertPg(conector)
            self.fideicomiso.insertPg(conector)
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (conector.conn):
                conector.conn.commit()
                conector.conn.close()
        
    def controlador(self):
        while True:
            opcion = input("1: Ejecutivo\n2: Todos menos ejecutivo y comercial\n3: Comercial\n4: Corporativo\n5: Empresa\n6: Institucional\n7: Personas y banca premium\n8: Pyme\n9: Microempresario popular\n10: Recargar data\n\n0: Salir\n")
            if(opcion == "1"):
                self.insertPg(self.cargaDatos.cartera.df, "EJECUTIVO")
            elif(opcion == "2"):
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Título Responsable"] == "Asesor de Negocios Comerciales")]
                    self.insertPg(df, "COMERCIAL")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "CORPORATIVO")]
                    self.insertPg(df, "CORPORATIVO")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "EMPRESA")]
                    self.insertPg(df, "EMPRESA")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "INSTITUCIONAL")]
                    self.insertPg(df, "INSTITUCIONAL")
                elif(opcion == "2"):
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Título Responsable"] == "Asesor de Negocios Comerciales")]
                    self.crear_excel(df, "Comercial")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "CORPORATIVO")]
                    self.crear_excel(df, "Corporativo")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "EMPRESA")]
                    self.crear_excel(df, "Empresa")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "INSTITUCIONAL")]
                    self.crear_excel(df, "Institucional")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "PYME")]
                    self.crear_excel(df, "Pyme")
                    df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "MICROEMPRESARIO POPULAR")]
                    self.crear_excel(df, "Microempresario Popular")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "3"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Título Responsable"] == "Asesor de Negocios Comerciales")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "COMERCIAL")
                elif(opcion == "2"):
                    self.crear_excel(df, "Comercial")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "4"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "CORPORATIVO")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "CORPORATIVO")
                elif(opcion == "2"):
                    self.crear_excel(df, "Corporativo")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "5"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "EMPRESA")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "EMPRESA")
                elif(opcion == "2"):
                    self.crear_excel(df, "Empresa")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "6"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "INSTITUCIONAL")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "INSTITUCIONAL")
                elif(opcion == "2"):
                    self.crear_excel(df, "Institucional")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "7"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "PERSONAS") & 
                                                (self.cargaDatos.cartera.df["Segmento"] == "BANCA PREMIUM")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "PERSONAS")
                elif(opcion == "2"):
                    self.crear_excel(df, "Personas")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "8"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "PYME")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "PYME")
                elif(opcion == "2"):
                    self.crear_excel(df, "Pyme")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "9"):
                df = self.cargaDatos.cartera.df[(self.cargaDatos.cartera.df["Segmento"] == "MICROEMPRESARIO POPULAR")]
                opcion = input("1: Insertar en db\n2: Crear Excel y .CSV\n")
                if(opcion == "1"):
                    self.insertPg(df, "MICROEMPRESARIO POPULAR")
                elif(opcion == "2"):
                    self.crear_excel(df, "Microempresario Popular")
                    #self.crear_csv(df)
                else:
                    break
            elif(opcion == "10"):
                self.recargar_datos()
            elif(opcion == "0"):
                print("Cerrando app.")
                break
            else:
                print("Opción incorrecta.")
        
    #Dirección en pc de archivos fuente, dirección de base de datos destino, nombre de la tabla dentro de la cartera clientes y fecha a asignar a cada registro.
controlador(r'C:\Users\bc221066\Documents\José Prieto\Cross Selling\Insumos\2021\Diciembre', '30/12/2021').controlador()

#contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()