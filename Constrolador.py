import pandas as pd
from cargaDatos import cargaDatos
from cross_selling import cross_selling

class controlador:
    
    def __init__(self):
        self.cargaDatos = cargaDatos()
        self.cartera = self.cargaDatos.cartera_cliente()
        self.crossSelling = cross_selling()
    
    #def buscar_rif(self, df, rif):
        
    def cruce_CSClientes_p2c(self):
        p2c = self.cargaDatos.P2C()
        csClientes = self.crossSelling.CSCliente
        new_row = {'MIS': 1234, 'NOMBRE DEL CLIENTE': 'Jose Prieto'}
        self.crossSelling.CSCliente = self.crossSelling.CSCliente.append(new_row, ignore_index=True)
        self.crossSelling.make_Excel()
        #df['Comedy_Score'].where(df['Rating_Score'] < 50)
        
    def crear_Excel(self):
        self.crossSelling.make_Excel()
        
contro = controlador()
contro.cruce_CSClientes_p2c()