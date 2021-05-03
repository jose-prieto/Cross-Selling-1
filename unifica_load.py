import pandas as pd
from ahorro_corriente.cc_unifica_load import cc_unifica_load
from ahorro_corriente.ah_unifica_load import ah_unifica_load

class unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera):
        self.ruta = ruta
        self.cc_unifica = cc_unifica_load(ruta, cartera)
        self.ah_unifica = ah_unifica_load(ruta, cartera)
        print("Uniendo los unificas")
        self.dfBs = pd.concat([self.cc_unifica.dfBs, self.ah_unifica.dfBs]).groupby(['mis']).sum().reset_index()
        self.dfDolar = pd.concat([self.cc_unifica.dfDolar, self.ah_unifica.dfDolar]).groupby(['mis']).sum().reset_index()
        self.dfEuro = self.cc_unifica.dfEuro
    
    def to_csv(self):
        self.dfBs.to_csv(self.ruta + '\\rchivos csv\corriente_ahorro.csv', index = False, header=True, sep='|')
        self.dfDolar.to_csv(self.ruta + '\\rchivos csv\convenio20_convenio1.csv', index = False, header=True, sep='|')
        self.dfEuro.to_csv(self.ruta + '\\rchivos csv\cuenta_euro.csv', index = False, header=True, sep='|')
        
    """def insertDfAccess(self,df):
        try:
            cursor = self.conn.cursor()
            for indice_fila, fila in df.iterrows():
                print("hola")
                cursor.execute("INSERT INTO UNIFICA ([mis], [rif_cedula], [tipo_persona], [estatus_operacion], [producto], [categoria], [monto contable]) VALUES(?,?,?,?,?,?,?)", fila[" MIS "], fila["Cedula/RIF "], fila[" Tipo Persona "], fila[" Estatus de la Operacion "], fila[" Producto "], fila[" Categoria "], fila[" Monto Contable "])
        except Exception as inst:
            print(type(inst))
            print(inst.args)
            print(inst)
        finally:
            self.conn.commit()
            self.conn.close()"""
    
#todo = unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#ccBs = todo.cc_unifica.dfBs
#ahBs = todo.ah_unifica.dfBs
#Bs = todo.dfBs