from pf_unifica_load import pf_unifica_load
from unifica_load import unifica_load
from tdv_load import tdv_load
from inventario_ajustado_load import inventario_ajustado_load
from P2C_Transacciones_load import P2C_Transacciones_load
from maestro_juridicos_load import maestro_juridicos_load
from reporte_pos_load import reporte_pos_load
from ivr_conexion_load import ivr_conexion_load
from cartera_cliente_load import cartera_cliente_load

class cargaDatos:
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def unifica(self, cartera):
        return unifica_load(self.ruta, cartera)
    
    def tdv(self, cartera):
        return tdv_load(self.ruta, cartera)
    
    def inventario(self, cartera):
        return inventario_ajustado_load(self.ruta, cartera)
        
    def pf_unifica(self):
        pf_unifica = pf_unifica_load(self.ruta)
        return pf_unifica
    
    def p2c(self):
        P2C_Transacciones = P2C_Transacciones_load(self.ruta)
        return P2C_Transacciones
    
    def TDC_ACTIVAS(self):
        tdc_activas = maestro_juridicos_load(self.ruta)
        return tdc_activas.make_TDC_ACTIVAS()
    
    def MADRES_JURIDICAS(self):
        madres_juridicas = maestro_juridicos_load(self.ruta)
        return madres_juridicas.make_TDC_ACTIVAS()
    
    def reporte_pos(self):
        reporte_pos = reporte_pos_load(self.ruta)
        return reporte_pos.make_DF()
    
    def ivr_conexion(self):
        ivr_conexion = ivr_conexion_load(self.ruta)
        return ivr_conexion
    
    def cartera_cliente(self, db):
        cartera_cliente = cartera_cliente_load(self.ruta, db)
        return cartera_cliente.to_csv()

#cargaDatos = cargaDatos()
#pf_unifica = cargaDatos.pf_unifica()
#cc_unifica = cargaDatos.cc_unifica()
#ah_unifica = cargaDatos.ah_unifica()
#rrgg_institucional = cargaDatos.rrgg_institucional()
#rrgg_corporativo = cargaDatos.rrgg_corporativo()
#rrgg_empresa = cargaDatos.rrgg_empresa()
#p2c = cargaDatos.P2C()
#rrgg_empresa = cargaDatos.rrgg_empresa()
#tdc_activas = cargaDatos.TDC_ACTIVAS()
#tdc_madres = cargaDatos.MADRES_JURIDICAS()
#reporte_pos = cargaDatos.reporte_pos()
#ivr_conexion = cargaDatos.ivr_conexion()
#rrgg_pyme = cargaDatos.rrgg_pyme()
#df = cargaDatos.cartera_cliente()