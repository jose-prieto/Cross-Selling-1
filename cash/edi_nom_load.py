import pandas as pd

class edi_nom_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando EDI NOM")
        self.rutaOrigin = ruta
        self.df = pd.read_excel(ruta + '\cash_llena.xlsx', usecols = 'A,B', sheet_name = 'EDINOM', dtype=str, header=0, index_col=False, keep_default_na=True)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df['monto'] = self.df['monto'].astype(float)
        self.df = self.df.groupby(['mis'], as_index=False).agg({'monto': sum})