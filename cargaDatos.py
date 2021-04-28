from pf_unifica_load import pf_unifica_load
from cc_unifica_load import cc_unifica_load
from ah_unifica_load import ah_unifica_load
from rrgg_institucional_load import rrgg_institucional_load
from rrgg_corporativo_load import rrgg_corporativo_load
from P2C_Transacciones_load import P2C_Transacciones_load
from rrgg_empresa_load import rrgg_empresa_load
from maestro_juridicos_load import maestro_juridicos_load
from reporte_pos_load import reporte_pos_load
from ivr_conexion_load import ivr_conexion_load
from rrgg_pyme_load import rrgg_pyme_load
from cartera_cliente_load import cartera_cliente_load

class cargaDatos:
    
    #Atributos
    ruta = r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero'
    
    #Constructor
    def __init__(self):
        pass
        
    def pf_unifica(self):
        pf_unifica = pf_unifica_load(self.ruta)
        return pf_unifica.make_DF()
    
    def cc_unifica(self):
        cc_unifica = cc_unifica_load(self.ruta)
        return cc_unifica.make_DF()
    
    def ah_unifica(self):
        ah_unifica = ah_unifica_load(self.ruta)
        return ah_unifica.make_DF()
    
    def rrgg_institucional(self):
        rrgg_institucional = rrgg_institucional_load(self.ruta)
        return rrgg_institucional.make_DF()
    
    def rrgg_corporativo(self):
        rrgg_corporativo = rrgg_corporativo_load(self.ruta)
        return rrgg_corporativo.make_DF()
    
    def rrgg_empresa(self):
        rrgg_empresa = rrgg_empresa_load(self.ruta)
        return rrgg_empresa.make_DF()
    
    def P2C(self):
        P2C_Transacciones = P2C_Transacciones_load(self.ruta)
        return P2C_Transacciones.make_DF()
    
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
        return ivr_conexion.make_DF()
    
    def rrgg_pyme(self):
        rrgg_pyme = rrgg_pyme_load(self.ruta)
        return rrgg_pyme.make_DF()
    
    def cartera_cliente(self):
        cartera_cliente = cartera_cliente_load(self.ruta)
        return cartera_cliente.make_DF()

cargaDatos = cargaDatos()
#pf_unifica = cargaDatos.pf_unifica()
cc_unifica = cargaDatos.cc_unifica()
ah_unifica = cargaDatos.ah_unifica()
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