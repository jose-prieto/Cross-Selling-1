from cargaDatos import cargaDatos
from cross_selling import cross_selling

class controlador:
    
    
    def __init__(self):
        self.cargaDatos = cargaDatos()
        self.cartera = self.cargaDatos.cartera_cliente()
        self.crossSelling = cross_selling()
        self.objetCartera = ''
        
    def crear_fila_p2c(self, fila):
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
        
    def crear_fila_ccUnifica(self, fila):
        new_row = {'MIS': self.objetCartera["MisCliente"].item(), 
                    'RIF': self.objetCartera["CedulaCliente"].item(), 
                    'NOMBRE DEL CLIENTE': self.objetCartera["NombreCliente"].item(),
                    'Corriente/Ahorro': fila[" Monto Contable "]}
        self.crossSelling.MontosCliente = self.crossSelling.MontosCliente.append(new_row, ignore_index=True)
        new_row = {'MIS': self.objetCartera["MisCliente"].item(), 
                    'RIF': self.objetCartera["CedulaCliente"].item(), 
                    'NOMBRE DEL CLIENTE': self.objetCartera["NombreCliente"].item(),
                    'Corriente/Ahorro': 1}
        self.crossSelling.CSCliente = self.crossSelling.CSCliente.append(new_row, ignore_index=True)
        
    def cruce_p2c(self):
        p2c = self.cargaDatos.P2C()
        print("Creando cruce cartera y p2c")
        
        for indice_fila, fila in p2c.iterrows():
            if fila["RIF"] in list(self.cartera['CedulaCliente']):
                self.objetCartera = self.cartera.loc[self.cartera['CedulaCliente'] == fila["RIF"]]
                if (len(self.objetCartera) == 1):
                    self.crear_fila_p2c(fila)
                else:
                    print(len(self.objetCartera))
                    print(fila["RIF"])
                    
    def cruce_cc_unifica(self):
        cc_unifica = self.cargaDatos.cc_unifica()
        print("Creando cruce cartera y ccUnifica")
        
        for indice_fila, fila in cc_unifica.iterrows():
            if fila[" MIS "] in list(self.cartera['MisCliente']):
                self.objetCartera = self.cartera.loc[self.cartera['MisCliente'] == fila[" MIS "]]
                if fila[" MIS "] not in list(self.crossSelling.MontosCliente['MIS']):
                    if (len(self.objetCartera) == 1):
                        self.crear_fila_ccUnifica(fila)
                    else:
                        print(len(self.objetCartera))
                        print(fila[" MIS "])
        self.crossSelling.make_Excel()
        
contro = controlador()
contro.cruce_cc_unifica()