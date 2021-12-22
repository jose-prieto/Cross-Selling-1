import pandas as pd
import glob as gb
import numpy as np
import csv

class cc_unifica_load:
    
    #Constructor
    def __init__(self, ruta, cartera):
        self.nombre_archivo = '\cc_unifica'
        self.ruta = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        columnas = ["Cedula/RIF ", " MIS ", " Nombre del Cliente ", " Tipo Persona ", " Monto Contable ", " Oficina Contable ", " Categoria ", " Estatus de la Operacion ", " Producto ", " Segmento "]
        self.df = pd.read_csv(self.ruta, usecols=(columnas), engine='python', sep="|", index_col=False, encoding='latin-1', quoting=csv.QUOTE_NONE, dtype=str)
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype(float)
        self.df[' Monto Contable '] = self.df[' Monto Contable '].astype(float)
        self.df = self.df[(self.df[" Oficina Contable "] <= 699) & 
                          (self.df[" Categoria "] != "B") & 
                          (self.df[" Categoria "] != "F") & 
                          (self.df[" Categoria "] != "H") & 
                          (self.df[" Categoria "] != "J") & 
                          (self.df[" Categoria "] != "K") & 
                          (self.df[" Categoria "] != "V")]
        #self.df = self.df.groupby([' Producto ']).agg({' Oficina Contable ': 'first'})
        self.df = self.df.rename(columns={'Cedula/RIF ': 'CedulaCliente', 
                                          ' MIS ': 'mis', 
                                          ' Nombre del Cliente ': 'Nombre del cliente', 
                                          ' Tipo Persona ': 'Tipo de Cliente', 
                                          ' Segmento ': 'Segmento', 
                                          ' Producto ': 'Producto', 
                                          ' Monto Contable ': 'monto', 
                                          ' Estatus de la Operacion ': 'estatus'})
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.sobregiro = self.df[(self.df["monto"] < 0)]
        self.sobregiro["monto"] *= -1
        #self.sobregiro = self.df[(self.df["monto"] < 0)].multiply(-1)
        print("Sobregiro: ", self.sobregiro['monto'].sum())
        self.df['monto'] = np.where(self.df['monto'] < 0, 0, self.df['monto'])
        self.df["Tipo de Cliente"].replace({"PERSONA NATURAL": "Natural", 
                                            "PERSONA JURIDICA": "Jurídica"}, inplace=True)
        
        self.dfBs = self.df[(self.df["Producto"] != "Corriente - CUENTA CORRIENTE MON. EXT DOLAR") & 
                          (self.df["Producto"] != "Corriente - CUENTA CORRIENTE ME EN EUROS")]
        print("\n---\ncc_unifica bolívares: ", self.dfBs['monto'].sum())
        
        self.nombre_archivo = '\\cuent'
        self.ruta = ""
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        columnas = ["CEDULA", "MIS", "NOMBRE", "SALDO_REAL", "SEGMENTO", "ESTADO"]
        self.dfO = pd.read_csv(self.ruta, usecols=(columnas), engine='python', sep="|", index_col=False, encoding='latin-1', quoting=csv.QUOTE_NONE, dtype=str)
        self.dfO = self.dfO.assign(tipo = "Jurídica")
        self.dfO = self.dfO.rename(columns={'CEDULA': 'CedulaCliente', 
                                              'MIS': 'mis', 
                                              'NOMBRE': 'Nombre del cliente', 
                                              'SALDO_REAL': 'monto', 
                                              'SEGMENTO': 'Segmento', 
                                              'tipo': 'Tipo de Cliente'})
        self.dfO['monto'] = self.dfO['monto'].astype(float)
        self.dfO['monto'] = np.where(self.dfO['monto'] < 0, 0, self.dfO['monto'])
        self.dfO['CedulaCliente'] = self.dfO['CedulaCliente'].str.strip()
        self.dfO['Segmento'] = self.dfO['Segmento'].str.strip()
        self.dfO["Segmento"].replace({"CI": "INSTITUCIONAL", 
                                      "CP": "CORPORATIVO", 
                                      "CR": "PYME", 
                                      "CS": "EMPRESA"}, inplace=True)
        self.dfBs = pd.concat([self.dfBs, self.dfO]).groupby(['mis'], as_index=False).agg({'monto': sum})
        print("cc_unifica Bolívares con cuenta O: ", self.dfBs['monto'].sum())
        
        self.dfDolar = self.df[(self.df["Producto"] == "Corriente - CUENTA CORRIENTE MON. EXT DOLAR") | 
                               (self.df["Producto"] == "Corriente - MI CUENTA EN DIVISAS DIGITAL EN DOLARES") ]
        self.dfDolar = self.dfDolar.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("cc_unifica Dólares: ", self.dfDolar['monto'].sum())
        
        self.dfEuro = self.df[(self.df["Producto"] == "Corriente - CUENTA CORRIENTE ME EN EUROS")]
        self.dfEuro = self.dfEuro.groupby(['mis'], as_index=False).agg({'monto': sum})
        print("cc_unifica Euros: ", self.dfEuro['monto'].sum())
        """self.nombre_archivo = '\cc_unifica'
        self.rutaOrigin = ruta
        for file in gb.glob(ruta + self.nombre_archivo + '*.txt'):
            self.ruta = file
        self.df = pd.read_csv(self.ruta, delimiter='|', index_col=False, decimal=",", dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.df[' Monto Contable '] = self.df[' Monto Contable '].astype('float')
        #print(self.df[self.df[' Oficina Contable '].isnull()])
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype('int')
        self.df = self.df[(self.df[" Oficina Contable "] < 700) &
                          (self.df[" Categoria "] != "B") & 
                          (self.df[" Categoria "] != "F") & 
                          (self.df[" Categoria "] != "H") & 
                          (self.df[" Categoria "] != "J") & 
                          (self.df[" Categoria "] != "K") & 
                          (self.df[" Categoria "] != "V") &
                          (self.df[" Estatus de la Operacion "] != "CANCELADA")]
        print("cc_unifica monto total: ", self.df[' Monto Contable '].sum())
        
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on=' MIS ')
        self.dfBs = self.df[(self.df[" Producto "] != "Corriente - CUENTA CORRIENTE MON. EXT DOLAR") & 
                          (self.df[" Producto "] != "Corriente - CUENTA CORRIENTE ME EN EUROS")]
        self.dfBs = self.dfBs.groupby([' MIS '], as_index=False).agg({' Monto Contable ': sum})
        self.dfBs = self.dfBs.rename(columns={' MIS ': 'mis', ' Monto Contable ': 'monto'})
        print("cc_unifica bolívares monto total: ", self.dfBs['monto'].sum())
        
        self.dfDolar = self.df[(self.df[" Producto "] == "Corriente - CUENTA CORRIENTE MON. EXT DOLAR")]
        self.dfDolar = self.dfDolar.groupby([' MIS '], as_index=False).agg({' Monto Contable ': sum})
        self.dfDolar = self.dfDolar[(self.dfDolar[" Monto Contable "] > 0)]
        self.dfDolar = self.dfDolar.rename(columns={' MIS ': 'mis', ' Monto Contable ': 'monto'})
        print("cc_unifica dólares monto total: ", self.dfDolar['monto'].sum())
        
        self.dfEuro = self.df[(self.df[" Producto "] == "Corriente - CUENTA CORRIENTE ME EN EUROS")]
        self.dfEuro = self.dfEuro.groupby([' MIS '], as_index=False).agg({' Monto Contable ': sum})
        self.dfEuro = self.dfEuro[(self.dfEuro[" Monto Contable "] > 0)]
        self.dfEuro = self.dfEuro.rename(columns={' MIS ': 'mis', ' Monto Contable ': 'monto'})
        print("cc_unifica Euros monto total: ", self.dfEuro['monto'].sum())"""
    
    def to_csv(self):
        self.dfBs.to_csv(self.rutaOrigin + '\\rchivos csv\cc_unifica_BS.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfDolar.to_csv(self.rutaOrigin + '\\rchivos csv\cc_unifica_Dolar.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
        self.dfEuro.to_csv(self.rutaOrigin + '\\rchivos csv\cc_unifica_Euro.csv', index = False, header=True, sep='|', encoding='latin-1', quoting=csv.QUOTE_NONE)
    
#todo = cc_unifica_load(r'C:\Users\bc221066\Documents\José Prieto\Cross Selling\Insumos\2021\Noviembre')
#Bs = todo.df
#Dolar = todo.dfDolar
#Euro = todo.dfEuro