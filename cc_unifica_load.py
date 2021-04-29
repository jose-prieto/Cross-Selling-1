import pandas as pd

class cc_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\cc_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        print("Creando cc_unifica")
        df = pd.read_csv(self.ruta + self.nombre_archivo + '2901.txt', delimiter='|', dtype=str, encoding='latin-1')
        df = df[(df[" Tipo Persona "] == "PERSONA JURIDICA") & ((df[" Estatus de la Operacion "] == "ACTIVA") | (df[" Estatus de la Operacion "] == "INACTIVA"))]
        df = df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto Contable ': sum})
        return df