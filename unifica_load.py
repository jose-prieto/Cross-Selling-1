from ahorro_corriente.cc_unifica_load import cc_unifica_load
from ahorro_corriente.ah_unifica_load import ah_unifica_load
from psycopg2.errors import ForeignKeyViolation
import pandas as pd
import csv

class unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando unifica")
        self.ruta = ruta
        self.fecha = fecha
        self.cc_unifica = cc_unifica_load(ruta, cartera)
        self.ah_unifica = ah_unifica_load(ruta, cartera)
        #self.dfBs = pd.concat([self.cc_unifica.dfBs, self.ah_unifica.dfBs]).groupby(['mis']).sum().reset_index()
        #self.dfBs = self.dfBs.assign(fecha = self.fecha)
        
        self.ahorro = self.ah_unifica.dfBs
        self.ahorro = self.ahorro.assign(fecha = self.fecha)
        
        self.corriente = self.cc_unifica.dfBs
        self.corriente = self.corriente.assign(fecha = self.fecha)
        
        self.dfDolar = pd.concat([self.cc_unifica.dfDolar, 
                                  self.ah_unifica.dfDolar]).groupby(['mis']).sum().reset_index()
        self.dfDolar = self.dfDolar.assign(fecha = self.fecha)
        
        self.dfEuro = self.cc_unifica.dfEuro
        self.dfEuro = self.dfEuro.assign(fecha = self.fecha)
        
        self.dfEuro['monto'] = self.dfEuro['monto'].astype(float)
        self.dfDolar['monto'] = self.dfDolar['monto'].astype(float)
        self.corriente['monto'] = self.corriente['monto'].astype(float)
        self.ahorro['monto'] = self.ahorro['monto'].astype(float)
        #self.dfBs['monto'] = self.dfBs['monto'].astype(float)
        
        print("Total en cuentas de ahorro: ", self.ahorro['monto'].sum())
        print("Total en cuentas corriente: ", self.corriente['monto'].sum())
        print("convenio 20 / convenio 1 total: ", self.dfDolar['monto'].sum())
        print("Cuenta en Euros total: ", self.dfEuro['monto'].sum(), "\n")
        
    def get_monto(self):
        dfEuro = self.dfEuro
        dfEuro = dfEuro.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfEuro['monto'] = dfEuro['monto'].astype(str)
        
        dfDolar = self.dfDolar
        dfDolar = dfDolar.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfDolar['monto'] = dfDolar['monto'].astype(str)
        
        dfCorriente = self.corriente
        dfCorriente = dfCorriente.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfCorriente['monto'] = dfCorriente['monto'].astype(str)
        
        dfAhorro = self.ahorro
        dfAhorro = dfAhorro.groupby(['mis'], as_index=False).agg({'monto': sum})
        dfAhorro['monto'] = dfAhorro['monto'].astype(str)
        
        for i in range(len(dfCorriente['monto'])):
            dfCorriente['monto'][i]=dfCorriente['monto'][i].replace('.',',')
            
        for i in range(len(dfAhorro['monto'])):
            dfAhorro['monto'][i]=dfAhorro['monto'][i].replace('.',',')
        
        for i in range(len(dfDolar['monto'])):
            dfDolar['monto'][i]=dfDolar['monto'][i].replace('.',',')
            
        for i in range(len(dfEuro['monto'])):
            dfEuro['monto'][i]=dfEuro['monto'][i].replace('.',',')
            
        dfMonto = pd.merge(dfAhorro.rename(columns={'monto': 'Ahorro'}), 
                           dfCorriente.rename(columns={'monto': 'Corriente'}), 
                           how='outer', right_on='mis', left_on='mis')
        
        dfMonto = pd.merge(dfMonto, dfDolar.rename(columns={'monto': 'Convenio 20 / Convenio 1'}), 
                           how='outer', right_on='mis', left_on='mis')
        return pd.merge(dfMonto, dfEuro.rename(columns={'monto': 'Cuenta en Euros'}), 
                        how='outer', right_on='mis', left_on='mis')
    
    def get_usable(self):
        dfBs = pd.merge(self.ahorro.rename(columns={'monto': 'Ahorro'}), 
                           self.corriente.rename(columns={'monto': 'Corriente'}), 
                           how='outer', right_on='mis', left_on='mis')
        dfBs = dfBs.assign(uso = 1)
        dfBs = dfBs.rename(columns={'uso': 'Corriente/Ahorro'})
        dfBs = dfBs.groupby(['mis'], as_index=False).agg({'Corriente/Ahorro': 'first'})
        
        df = pd.merge(self.dfDolar, self.dfEuro, how='outer', right_on='mis', left_on='mis')
        df = df.assign(uso = 1)
        df = df.groupby(['mis'], as_index=False).agg({'uso': 'first'})
        
        return pd.merge(dfBs, df.rename(columns={'uso': 'Cuenta Moneda Extranjera (Dólar y Euro)'}), 
                        how='outer', right_on='mis', left_on='mis')
    
    def insertPg(self, conector):
        print("Insertando cuenta de ahorros")
        for indice_fila, fila in self.ahorro.iterrows():
            try:
                conector.cursor.execute("INSERT INTO AHORRO (ah_mis, ah_monto, ah_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except KeyError as e:
                print(type(e))
                print(e.args)
                print(e) 
                print("key")
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep) 
                print("ac_bs1")
            finally:
                conector.conn.commit()
        
        print("Insertando cuenta corriente")
        for indice_fila, fila in self.corriente.iterrows():
            try:
                conector.cursor.execute("INSERT INTO CORRIENTE (ah_mis, ah_monto, ah_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except KeyError as e:
                print(type(e))
                print(e.args)
                print(e) 
                print("key")
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep) 
                print("ac_bs4")
            finally:
                conector.conn.commit()
                
        print("Insertando cuenta_dolar")
        for indice_fila, fila in self.dfDolar.iterrows():
            try:
                conector.cursor.execute("INSERT INTO CONVENIO (conv_mis, conv_monto, conv_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("ac_bs2")
            finally:
                conector.conn.commit()
        
        print("Insertando cuenta_euro")
        for indice_fila, fila in self.dfEuro.iterrows():
            try:
                conector.cursor.execute("INSERT INTO CUENTA_EUROS (eur_mis, eur_monto, eur_fecha) VALUES(%s, %s, %s)", 
                               (fila["mis"], 
                               fila["monto"], 
                               fila["fecha"]))
            except ForeignKeyViolation:
                pass
            except Exception as excep:
                print(type(excep))
                print(excep.args)
                print(excep)
                print("ac_bs3")
            finally:
                conector.conn.commit()
    
    def to_csv(self, df):
        self.dfBs.to_csv(self.ruta + '\\rchivos csv\corriente_ahorro.csv', index = False, header=True, sep='|', 
                         encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        self.dfDolar.to_csv(self.ruta + '\\rchivos csv\convenio20_convenio1.csv', index = False, header=True, sep='|', 
                            encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
        self.dfEuro.to_csv(self.ruta + '\\rchivos csv\cuenta_euro.csv', index = False, header=True, sep='|', 
                           encoding='utf-8-sig', quoting=csv.QUOTE_NONE)
    
#todo = unifica_load(r'C:\Users\José Prieto\Documents\Bancaribe\Marzo')
#ccBs = todo.cc_unifica.dfBs
#ahBs = todo.ah_unifica.dfBs
#Bs = todo.dfBs