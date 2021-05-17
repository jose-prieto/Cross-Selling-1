from cargaDatos import cargaDatos
from pathlib import Path
import pandas as pd

class controlador:
    
    def __init__(self, ruta, rutadb, db, fecha):
        self.ruta = ruta + '\\rchivos csv'
        Path(self.ruta).mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta, rutadb, fecha, db)
        
        self.unifica = self.cargaDatos.unifica()
        self.tdv = self.cargaDatos.tdv()
        self.mesa_cambio = self.cargaDatos.mesa_cambio()
        self.exportacion = self.cargaDatos.exportacion()
        self.intervencion_tdc = self.cargaDatos.intervencion_tdc()
        self.custodia = self.cargaDatos.custodia()
        self.inventario = self.cargaDatos.inventario()
        self.linea_cir = self.cargaDatos.linea_cir()
        self.tdc_juridica = self.cargaDatos.tdc_juridica()
        self.cash = self.cargaDatos.cash()
        self.puntos_venta = self.cargaDatos.puntos_venta()
        self.ivr_conexion = self.cargaDatos.ivr_conexion()
        self.p2c = self.cargaDatos.p2c()
        
        cartera = pd.merge(self.cargaDatos.cartera.df, self.crear_cartera_montos(), how='inner', left_on='MisCliente', right_on='mis')
        self.cargaDatos.cartera.df = cartera.groupby(['MisCliente'], as_index=False).agg({'fecha': 'first', 
                                                                                          'CedulaCliente': 'first', 
                                                                                          'NombreCliente': 'first',
                                                                                          'Segmento Mis': 'first',
                                                                                          'Unidad De Negocio': 'first',
                                                                                          'Region': 'first',
                                                                                          'Nombre del Responsable': 'first'})
    
    def crear_cartera_montos(self):
        carteraMonto = self.unifica.get_monto()
        carteraMonto = pd.merge(carteraMonto, self.tdv.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.mesa_cambio.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.exportacion.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_tdc.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.custodia.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.inventario.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.linea_cir.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cash.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.puntos_venta.get_monto(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2c.get_monto(), how='outer', left_on='mis', right_on='mis')
        return carteraMonto
    
    def crear_cartera_clientes(self):
        carteraMonto = self.unifica.get_usable()
        carteraMonto = pd.merge(carteraMonto, self.tdv.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.mesa_cambio.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.exportacion.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.intervencion_tdc.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.custodia.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.inventario.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.linea_cir.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.tdc_juridica.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cash.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.puntos_venta.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.ivr_conexion.get_usable(), how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.p2c.get_usable(), how='outer', left_on='mis', right_on='mis')
        return carteraMonto
        
    def crear_excel(self):
        print("Creando excel")
        clientes = pd.merge(self.cargaDatos.cartera.df, self.crear_cartera_clientes(), how='inner', left_on='MisCliente', right_on='mis').fillna(0)
        montos = pd.merge(self.cargaDatos.cartera.df, self.crear_cartera_montos(), how='inner', left_on='MisCliente', right_on='mis').fillna(0)
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021-Corporativa.xlsx')
        clientes[(clientes["Segmento Mis"] == "CP-CORPORATIVO")].to_excel(writer, sheet_name="CS Clientes", index=False, startrow=8, freeze_panes=(9,5))
        montos[(montos["Segmento Mis"] == "CP-CORPORATIVO")].to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,5))
        writer.save()
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021-Institucional.xlsx')
        clientes[(clientes["Segmento Mis"] == "CI-INSTITUCIONAL")].to_excel(writer, sheet_name="CS Clientes", index=False, startrow=8, freeze_panes=(9,5))
        montos[(montos["Segmento Mis"] == "CI-INSTITUCIONAL")].to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,5))
        writer.save()
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021-Empresa.xlsx')
        clientes[(clientes["Segmento Mis"] == "CS-EMPRESA")].to_excel(writer, sheet_name="CS Clientes", index=False, startrow=8, freeze_panes=(9,5))
        montos[(montos["Segmento Mis"] == "CS-EMPRESA")].to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,5))
        writer.save()
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021-Pyme.xlsx')
        clientes[(clientes["Segmento Mis"] == "CR-PYME")].to_excel(writer, sheet_name="CS Clientes", index=False, startrow=8, freeze_panes=(9,5))
        montos[(montos["Segmento Mis"] == "CR-PYME")].to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8, freeze_panes=(9,5))
        writer.save()
        
        
    def crear_csv(self):
        self.cargaDatos.unifica().dfMonto
        
    def insert_db(self):
        self.cargaDatos.cartera.insertDf()
        self.unifica.insertDf()
        self.custodia.insertDf()
        
    #Dirección en pc de archivos fuente, dirección de base de datos destino, nombre de la tabla dentro de la cartera clientes y fecha a asignar a cada registro.
contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Insumos Cross Selling\Enero', r'C:\Users\José Prieto\Documents\Bancaribe\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021')
df = contro.cargaDatos.cartera.df
contro.crear_excel()

#contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()