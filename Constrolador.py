from cargaDatos import cargaDatos
from cross_selling import cross_selling
from pathlib import Path

class controlador:
    
    def __init__(self, ruta, db):
        Path(ruta + '\\rchivos csv').mkdir(parents=True, exist_ok=True)
        self.cargaDatos = cargaDatos(ruta)
        self.cartera = self.cargaDatos.cartera_cliente(db)
        self.crossSelling = cross_selling()
        
    def cruce_unifica_csv(self):
        unifica = self.cargaDatos.unifica(self.cartera)
        return unifica.to_csv()
    
    def cruce_tdv_csv(self):
        tdv = self.cargaDatos.tdv(self.cartera)
        return tdv.to_csv()
    
    def cruce_inventario_csv(self):
        inventario = self.cargaDatos.inventario(self.cartera)
        return inventario.to_csv()
    
    def cruce_pf_unifica(self):
        pf = self.cargaDatos.pf_unifica()
        return pf.to_csv(self.cartera)
    
    def cruce_p2c(self):
        p2c = self.cargaDatos.p2c()
        return p2c.to_csv(self.cartera)
    
    def cruce_ivr_conexion(self):
        ivr_conexion = self.cargaDatos.ivr_conexion()
        return ivr_conexion.to_csv(self.cartera)
    
    def crear_csvs(self):
        self.cruce_inventario_csv()
        #self.cruce_unifica_csv()
        #self.cruce_tdv_csv()
        #self.cruce_p2c()
        #self.cruce_ivr_conexion()
        
contro = controlador(r'C:\Users\José Prieto\Documents\Bancaribe\Enero', "Cartera_Clientes_Enero_2020").crear_csvs()