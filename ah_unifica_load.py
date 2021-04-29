import pandas as pd

class ah_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\\ah_unifica_'
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
    
    def make_DF(self):
        print("Creando ah_unifica")
        df = pd.read_csv(self.ruta + self.nombre_archivo + '2901.txt', delimiter='|', index_col=False, dtype=str, encoding='latin-1')
        df[' Monto Contable '] = df[' Monto Contable '].astype(float)
        df = df[(df[" Tipo Persona "] == "PERSONA JURIDICA")]
        df = df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto Contable ': sum})
        return df