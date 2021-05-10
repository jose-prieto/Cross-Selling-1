from cargaDatos import cargaDatos
from pathlib import Path
import pandas as pd

class controlador:
    
    def __init__(self, ruta, rutadb, db, fecha):
        self.ruta = ruta + '\\rchivos csv'
        Path(self.ruta).mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta, rutadb, fecha, db)
        
        self.unifica = self.cargaDatos.unifica()
        """self.tdv = self.cargaDatos.tdv()
        self.mesa_cambio = self.cargaDatos.mesa_cambio()
        self.exportacion = self.cargaDatos.exportacion()
        self.intervencion_tdc = self.cargaDatos.intervencion_tdc()"""
        self.custodia = self.cargaDatos.custodia()
        """self.inventario = self.cargaDatos.inventario()
        self.linea_cir = self.cargaDatos.linea_cir()
        self.tdc_juridica = self.cargaDatos.tdc_juridica()
        self.cash = self.cargaDatos.cash()
        self.puntos_venta = self.cargaDatos.puntos_venta()
        self.ivr_conexion = self.cargaDatos.ivr_conexion()
        self.p2c = self.cargaDatos.p2c()"""
        
        self.cargaDatos.cartera.df = pd.merge(self.cargaDatos.cartera.df, self.crear_cartera(), how='inner', left_on='MisCliente', right_on='mis')
    
    def crear_cartera(self):
        carteraMonto = self.unifica.get_monto()
        #carteraMonto = pd.merge(carteraMonto, self.tdv.dfMonto, how='outer', left_on='mis', right_on='mis')
        #carteraMonto = pd.merge(carteraMonto, self.mesa_cambio.dfMonto, how='outer', left_on='mis', right_on='mis')
        #carteraMonto = pd.merge(carteraMonto, self.exportacion.dfMonto, how='outer', left_on='mis', right_on='mis')
        #carteraMonto = pd.merge(carteraMonto, self.intervencion_tdc.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.custodia.get_monto(), how='outer', left_on='mis', right_on='mis')
        """carteraMonto = pd.merge(carteraMonto, self.inventario.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.linea_cir.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.tdc_juridica.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cash.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.puntos_venta.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.ivr_conexion.dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2c.dfMonto, how='outer', left_on='mis', right_on='mis')"""
        return carteraMonto
        
    def crear_excel(self):
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021.xlsx')
        self.cargaDatos.cartera.df.to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,8))
        writer.save()
        
        
    def crear_csv(self):
        self.cargaDatos.unifica().dfMonto
        
    def insert_db(self):
        self.cargaDatos.cartera.insertDf()
        self.unifica.insertDf()
        self.custodia.insertDf()
        
    #Dirección en pc de archivos fuente, dirección de base de datos destino, nombre de la tabla dentro de la cartera clientes y fecha a asignar a cada registro.
contro = controlador(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo', r'C:\Users\José Prieto\Documents\Bancaribe\Cross Selling', "Cartera_Clientes_Marzo_2021", '26/03/2021')
df = contro.cargaDatos.cartera.df
contro.insert_db()

#contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()