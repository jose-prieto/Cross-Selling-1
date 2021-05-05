from cross_selling import cross_selling
from cargaDatos import cargaDatos
from pathlib import Path
import pandas as pd

class controlador:
    
    def __init__(self, ruta, rutadb, db, fecha):
        self.ruta = ruta + '\\rchivos csv'
        Path(self.ruta).mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta, rutadb, fecha)
        self.cartera = self.cargaDatos.cartera_cliente(db)
        self.crossSelling = cross_selling()
    
    def cruce_inventario_csv(self):
        inventario = self.cargaDatos.inventario()
        return inventario.to_csv()
    
    def cruce_cir_csv(self):
        cir = self.cargaDatos.linea_cir()
        return cir.to_csv()
    
    def cruce_tdc_juridica_csv(self):
        tdc = self.cargaDatos.tdc_juridica()
        return tdc.to_csv()
    
    def cruce_puntos_venta_csv(self):
        puntos_venta = self.cargaDatos.puntos_venta()
        return puntos_venta.to_csv()
    
    def cruce_ivr_conexion_csv(self):
        ivr_conexion = self.cargaDatos.ivr_conexion()
        return ivr_conexion.to_csv()
    
    def cruce_p2c_csv(self):
        p2c = self.cargaDatos.p2c()
        return p2c.to_csv()
    
    def cruce_custodia_csv(self):
        custodia = self.cargaDatos.custodia()
        return custodia.to_csv()
    
    def cruce_cash_csv(self):
        cash = self.cargaDatos.cash()
        return cash.to_csv()
    
    def crear_csvs(self):
        carteraMonto = pd.merge(self.cargaDatos.unifica().dfMonto, self.cargaDatos.tdv().dfMonto, how='outer', left_on='mis', right_on='mis')
        carteraMonto = pd.merge(carteraMonto, self.cargaDatos.linea_cir().dfMonto, how='outer', left_on='mis', right_on='mis')
        """self.cruce_puntos_venta_csv()
        self.cruce_ivr_conexion_csv()
        self.cruce_p2c_csv()
        #Necesitan modificacion
        input("Quitar los números del archivo de inventario ajustado (Debe empezar en 'I')\n")
        self.cruce_inventario_csv() #quitar numeros del nombre, el nombre debe empezar por la letra "I"
        self.cruce_custodia_csv() #Completar información de cada columna del archivo nuevo con el archivo Custodia y completando los mis de manera manual
        self.cruce_cash_csv() #Completar información de cada columna del archivo nuevo con el archivo cash"""
        
        """carteraProducto['Convenio 20 / Convenio 1'] = pd.loc[carteraMonto['Convenio 20 / Convenio 1'].notnull(), 'Convenio 20 / Convenio 1'] = 1
        carteraProducto['Cuenta en Euros'] = pd.loc[carteraMonto['Cuenta en Euros'].notnull(), 'Cuenta en Euros'] = 1
        carteraProducto['Línea/CIR Monto Vigente aprobado (Bs.)'] = pd.loc[carteraMonto['Línea/CIR Monto Vigente aprobado (Bs.)'].notnull(), 'Línea/CIR Monto Vigente aprobado (Bs.)'] = 1
        carteraProducto['Línea/CIR Monto Vigente aprobado (USD)'] = pd.loc[carteraMonto['Línea/CIR Monto Vigente aprobado (USD)'].notnull(), 'Línea/CIR Monto Vigente aprobado (USD)'] = 1"""
        
        writer = pd.ExcelWriter(self.ruta + '\Cross-Selling-Enero-2021.xlsx')
        pd.merge(self.cartera, carteraMonto, how='inner', left_on='MisCliente', right_on='mis').to_excel(writer, sheet_name="Montos por Producto Cliente", index=False, startrow=8)
        carteraProducto = carteraMonto
        carteraProducto['Corriente/Ahorro'] = carteraProducto.loc[pd.notna(carteraProducto['Corriente/Ahorro']), 'Corriente/Ahorro'] = 1
        carteraProducto['TDV'] = carteraProducto.loc[pd.notna(carteraProducto['TDV']) , 'TDV'] = 1
        carteraProducto['Cuenta en Euros'] = carteraProducto.loc[pd.notna(carteraProducto['Cuenta en Euros']), 'Cuenta en Euros'] = 1
        carteraProducto['Línea/CIR Monto Vigente aprobado (Bs.)'] = carteraProducto.loc[pd.notna(carteraProducto['Línea/CIR Monto Vigente aprobado (Bs.)']), 'Línea/CIR Monto Vigente aprobado (Bs.)'] = 1
        carteraProducto['Línea/CIR Monto Vigente aprobado (USD)'] = carteraProducto.loc[pd.notna(carteraProducto['Línea/CIR Monto Vigente aprobado (USD)']), 'Línea/CIR Monto Vigente aprobado (USD)'] = 1
        carteraProducto['Convenio 20 / Convenio 1'] = carteraProducto.loc[pd.notna(carteraProducto['Convenio 20 / Convenio 1']), 'Convenio 20 / Convenio 1'] = 1
        pd.merge(self.cartera, carteraProducto, how='inner', left_on='MisCliente', right_on='mis').to_excel(writer, sheet_name="CS Cliente", index=False, startrow=8)
        writer.save()
        
    def insert_db(self):
        return self.cartera.to_db()
        
contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').crear_csvs()
#contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()