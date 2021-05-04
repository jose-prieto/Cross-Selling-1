from cross_selling import cross_selling
from cargaDatos import cargaDatos
from pathlib import Path

class controlador:
    
    def __init__(self, ruta, rutadb, db, fecha):
        Path(ruta + '\\rchivos csv').mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta, rutadb, fecha)
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
        self.cartera.to_csv()
        self.cruce_unifica_csv()
        self.cruce_tdv_csv()
        self.cruce_cir_csv()
        self.cruce_tdc_juridica_csv()
        self.cruce_puntos_venta_csv()
        self.cruce_ivr_conexion_csv()
        self.cruce_p2c_csv()
        #Necesitan modificacion
        input("Quitar los números del archivo de inventario ajustado (Debe empezar en 'I')\n")
        self.cruce_inventario_csv() #quitar numeros del nombre, el nombre debe empezar por la letra "I"
        self.cruce_custodia_csv() #Completar información de cada columna del archivo nuevo con el archivo Custodia y completando los mis de manera manual
        self.cruce_cash_csv() #Completar información de cada columna del archivo nuevo con el archivo cash
        
    def insert_db(self):
        return self.cartera.to_db()
        
#orden: ruta de carpeta con archivos fuente, ruta de base de datos a donde se almacenará la data, nombre de la tabla en la base de datos cartera y fecha en formato DD/MM/YYYY
contro = controlador(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero', r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Cross Selling', "Cartera_Clientes_Enero_2020", '29/01/2021').insert_db()