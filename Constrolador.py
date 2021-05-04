from cross_selling import cross_selling
from cargaDatos import cargaDatos
from datetime import datetime
from pathlib import Path

class controlador:
    
    def __init__(self, ruta, db, fecha):
        Path(ruta + '\\rchivos csv').mkdir(parents=True, exist_ok=True)
        self.fecha = datetime.strptime(fecha, '%d/%m/%Y')
        self.cargaDatos = cargaDatos(ruta, self.fecha)
        self.cartera = self.cargaDatos.cartera_cliente(db)
        self.crossSelling = cross_selling()
        
    def cruce_unifica_csv(self):
        unifica = self.cargaDatos.unifica()
        return unifica.to_csv()
    
    def cruce_tdv_csv(self):
        tdv = self.cargaDatos.tdv()
        return tdv.to_csv()
    
    def cruce_inventario_csv(self):
        inventario = self.cargaDatos.inventario()
        return inventario.to_csv()
    
    def cruce_cir(self):
        cir = self.cargaDatos.linea_cir()
        return cir.to_csv()
    
    def cruce_tdc_juridica(self):
        tdc = self.cargaDatos.tdc_juridica()
        return tdc.to_csv()
    
    def cruce_puntos_venta(self):
        puntos_venta = self.cargaDatos.puntos_venta()
        return puntos_venta.to_csv()
    
    def cruce_ivr_conexion(self):
        ivr_conexion = self.cargaDatos.ivr_conexion()
        return ivr_conexion.to_csv()
    
    def cruce_p2c(self):
        p2c = self.cargaDatos.p2c()
        return p2c.to_csv()
    
    def cruce_custodia(self):
        custodia = self.cargaDatos.custodia()
        return custodia.to_csv()
    
    def cruce_cash(self):
        cash = self.cargaDatos.cash()
        return cash.to_csv()
    
    def crear_csvs(self):
        """self.cruce_unifica_csv()
        self.cruce_tdv_csv()
        self.cruce_cir()
        self.cruce_tdc_juridica()
        self.cruce_puntos_venta()
        self.cruce_ivr_conexion()
        self.cruce_p2c()
        #Necesitan modificacion
        self.cruce_inventario_csv() #quitar numeros del nombre, el nombre debe empezar por la letra "I"
        self.cruce_custodia() #Completar información de cada columna del archivo nuevo con el archivo Custodia y completando los mis de manera manual"""
        self.cruce_cash() #Completar información de cada columna del archivo nuevo con el archivo cash
        
        
contro = controlador(r'C:\Users\José Prieto\Documents\Bancaribe\Enero', "Cartera_Clientes_Enero_2020", '31/01/2021').crear_csvs()