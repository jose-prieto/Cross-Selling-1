from cargaDatos import cargaDatos
from cross_selling import cross_selling

class controlador:
    
    
    def __init__(self):
        self.cargaDatos = cargaDatos()
        self.cartera = self.cargaDatos.cartera_cliente()
        self.crossSelling = cross_selling()
        self.objetCartera = ''
        
    def crear_DF(self, fila):
        new_row = {'MIS': self.objetCartera["MisCliente"].item(), 
                    'RIF': self.objetCartera["CedulaCliente"].item(), 
                    'NOMBRE DEL CLIENTE': self.objetCartera["NombreCliente"].item(),
                    'P2C (Mensual)': fila["Monto de la operacion"]}
        self.crossSelling.MontosCliente = self.crossSelling.MontosCliente.append(new_row, ignore_index=True)
        new_row = {'MIS': self.objetCartera["MisCliente"].item(), 
                    'RIF': self.objetCartera["CedulaCliente"].item(), 
                    'NOMBRE DEL CLIENTE': self.objetCartera["NombreCliente"].item(),
                    'P2C (Mensual)': 1}
        self.crossSelling.CSCliente = self.crossSelling.CSCliente.append(new_row, ignore_index=True)
        
    def cruce_p2c(self):
        p2c = self.cargaDatos.P2C()
        print("Creando cruce cartera y p2c")
        
        for indice_fila, fila in p2c.iterrows():
            if fila["RIF"] in list(self.cartera['CedulaCliente']):
                self.objetCartera = self.cartera.loc[self.cartera['CedulaCliente'] == fila["RIF"]]
                if (len(self.objetCartera) == 1):
                    self.crear_DF(fila)
                else:
                    print(len(self.objetCartera))
                    print(fila["RIF"])
                    
    def cruce_ah_cc_unifica(self):
        pass
        
contro = controlador()
contro.cruce_p2c()