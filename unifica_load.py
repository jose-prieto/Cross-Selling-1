import pandas as pd
import csv
from ahorro_corriente.cc_unifica_load import cc_unifica_load
from ahorro_corriente.ah_unifica_load import ah_unifica_load

class unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando unifica")
        self.ruta = ruta
        self.fecha = fecha
        self.cc_unifica = cc_unifica_load(ruta, cartera)
        self.ah_unifica = ah_unifica_load(ruta, cartera)
        self.dfBs = pd.concat([self.cc_unifica.dfBs, self.ah_unifica.dfBs]).groupby(['mis']).sum().reset_index()
        self.dfBs['monto'] = self.dfBs['monto'].astype(str)
        for i in range(len(self.dfBs['monto'])):
            self.dfBs['monto'][i]=self.dfBs['monto'][i].replace('.',',')
            
        self.dfDolar = pd.concat([self.cc_unifica.dfDolar, self.ah_unifica.dfDolar]).groupby(['mis']).sum().reset_index()
        self.dfDolar['monto'] = self.dfDolar['monto'].astype(str)
        for i in range(len(self.dfDolar['monto'])):
            self.dfDolar['monto'][i]=self.dfDolar['monto'][i].replace('.',',')
            
        self.dfEuro = self.cc_unifica.dfEuro
        self.dfEuro['monto'] = self.dfEuro['monto'].astype(str)
        for i in range(len(self.dfEuro['monto'])):
            self.dfEuro['monto'][i]=self.dfEuro['monto'][i].replace('.',',')
            
        self.dfMonto = pd.merge(self.dfBs.rename(columns={'monto': 'Corriente/Ahorro'}), self.dfDolar.rename(columns={'monto': 'Convenio 20 / Convenio 1'}), how='outer', right_on='mis', left_on='mis')
        self.dfMonto = pd.merge(self.dfMonto, self.dfEuro.rename(columns={'monto': 'Cuenta en Euros'}), how='outer', right_on='mis', left_on='mis')
        
        self.dfBs = self.dfBs.assign(fecha = self.fecha)
        self.dfDolar = self.dfDolar.assign(fecha = self.fecha)
        self.dfEuro = self.dfEuro.assign(fecha = self.fecha)
    
    def to_csv(self):
        self.dfBs.to_csv(self.ruta + '\\rchivos csv\corriente_ahorro.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfDolar.to_csv(self.ruta + '\\rchivos csv\convenio20_convenio1.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfEuro.to_csv(self.ruta + '\\rchivos csv\cuenta_euro.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        
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