import pandas as pd
from cargaDatos import cargaDatos
from cross_selling import cross_selling

class controlador:
    
    __cargaDatos = cargaDatos()
    __crossSelling = cross_selling()
    
    def __init__(self):
        pass
    
    #def buscar_rif(self, df, rif):
        
    def cruce_CSClientes_p2c(self):
        p2c = self.__cargaDatos.P2C()
        csClientes = self.__crossSelling.CSCliente
        
        df['Comedy_Score'].where(df['Rating_Score'] < 50)
        
    def crear_Excel(self):
        self.__crossSelling.make_Excel()
        
contro = controlador()
contro.cruce_CSClientes_p2c()
contro.crear_Excel()