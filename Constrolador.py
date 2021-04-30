import pandas as pd
from cargaDatos import cargaDatos
from cross_selling import cross_selling

class controlador:
    
    def __init__(self):
        self.cargaDatos = cargaDatos()
        self.cartera = self.cargaDatos.cartera_cliente()
        self.crossSelling = cross_selling()
        self.objetCartera = ''
        self.direccion = r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\archivos csv'
        
    def cruce_cc_unifica(self):
        cc_unifica = self.cargaDatos.cc_unifica()
        cc_unifica.make_DF()
        print("Creando cruce cartera y ccUnifica")
        cc_unifica.df = pd.merge(cc_unifica.df, self.cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        cc_unifica.df.to_csv(self.direccion + "\cc_unifica.csv", index = False, header=True, sep='|')
        return cc_unifica.df
    
    def cruce_ah_unifica(self):
        ah_unifica = self.cargaDatos.ah_unifica()
        ah_unifica.make_DF()
        print("Creando cruce cartera y ahUnifica")
        ah_unifica.df = pd.merge(ah_unifica.df, self.cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        ah_unifica.df.to_csv(self.direccion + "\ch_unifica.csv", index = False, header=True, sep='|')
        return ah_unifica.df
    
    def cruce_pf_unifica(self):
        pf = self.cargaDatos.pf_unifica()
        pf.make_DF()
        print("Creando cruce cartera y pfUnifica")
        pf.df = pd.merge(pf.df, self.cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        pf.df.to_csv(self.direccion + "\pf_unifica.csv", index = False, header=True, sep='|')
        return pf.df
    
    def cruce_p2c(self):
        p2c = self.cargaDatos.p2c()
        p2c.make_DF()
        print("Creando cruce cartera y p2c")
        p2c.df = pd.merge(p2c.df, self.cartera, how='inner', right_on='CedulaCliente', left_on='RIF')
        p2c.df.to_csv(self.direccion + "\p2c.csv", index = False, header=True, sep='|')
        return p2c.df
    
    def cruce_ivr_conexion(self):
        ivr_conexion = self.cargaDatos.ivr_conexion()
        ivr_conexion.make_DF()
        print("Creando cruce cartera e ivr")
        ivr_conexion.df = pd.merge(ivr_conexion.df, self.cartera, how='inner', right_on='CedulaCliente', left_on='cedula')
        ivr_conexion.df.to_csv(self.direccion + "\ivr_conexion.csv", index = False, header=True, sep='|')
        return ivr_conexion.df
        
contro = controlador()
cc_unifica = contro.cruce_cc_unifica()
ah_unifica = contro.cruce_ah_unifica()
p2c = contro.cruce_p2c()
pf = contro.cruce_pf_unifica()
ivr_conexion = contro.cruce_ivr_conexion()