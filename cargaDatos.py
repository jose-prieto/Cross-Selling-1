from pf_unifica_load import pf_unifica_load
from cc_unifica_load import cc_unifica_load
from ah_unifica_load import ah_unifica_load
from rrgg_institucional_load import rrgg_institucional_load
from rrgg_corporativo_load import rrgg_corporativo_load
from P2C_Transacciones_load import P2C_Transacciones_load

class cargaDatos:
    
    #Atributos
    ruta = r'C:\Users\José Prieto\Documents\Bancaribe\Enero'
    
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
    
    def P2C(self):
        P2C_Transacciones = P2C_Transacciones_load(self.ruta)
        return P2C_Transacciones.make_DF()

cargaDatos = cargaDatos()
#pf_unifica = cargaDatos.pf_unifica()
#cc_unifica = cargaDatos.cc_unifica()
#ah_unifica = cargaDatos.ah_unifica()
#rrgg_institucional = cargaDatos.rrgg_institucional()
#rrgg_corporativo = cargaDatos.rrgg_corporativo()
p2c = cargaDatos.P2C()