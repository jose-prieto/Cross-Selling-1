import pandas as pd

class custodia_load:
    
    #Constructor
    def __init__(self, ruta, cartera, fecha):
        print("Creando cash")
        self.crear_excel(ruta)
        self.ruta = ruta
        input("Vacíe la información necesaria en el archivo de excel llamado 'custodia_llenar.xlsx' recién creado en la ruta:\n\n" + ruta + "\n\nluego presione Enter")
        self.df = pd.read_excel(self.ruta + '\custodia_llenar.xlsx', usecols = 'A:D', header=0, sheet_name = "custodia", index_col=False, keep_default_na=True, dtype=str)
        self.df = pd.merge(self.df, cartera, how='inner', right_on='MisCliente', left_on='mis')
        self.df['montoDolar'] = self.df['montoDolar'].astype(float)
        self.df['montoEuro'] = self.df['montoEuro'].astype(float)
        self.dfDolar = self.df.groupby(['mis'], as_index=False).agg({'montoDolar': sum})
        self.dfDolar = self.dfDolar.rename(columns={'montoDolar': 'monto'})
        self.dfDolar = self.dfDolar.assign(fecha = fecha)
        self.dfDolar['monto'] = self.dfDolar['monto'].astype(str)
        for i in range(len(self.dfDolar['monto'])):
            self.dfDolar['monto'][i]=self.dfDolar['monto'][i].replace('.',',')
        self.dfEuro = self.df = self.df.groupby(['mis'], as_index=False).agg({'montoEuro': sum})
        self.dfEuro = self.dfEuro.rename(columns={'montoEuro': 'monto'})
        self.dfEuro = self.dfEuro.assign(fecha = fecha)
        self.dfEuro['monto'] = self.dfEuro['monto'].astype(str)
        for i in range(len(self.dfEuro['monto'])):
            self.dfEuro['monto'][i]=self.dfEuro['monto'][i].replace('.',',')
        
    def crear_excel(self, ruta):
        writer = pd.ExcelWriter(ruta + '\custodia_llenar.xlsx')
        df = pd.DataFrame(columns = ['mis', 'cliente', 'montoDolar', 'montoEuro'])
        df.to_excel(writer, sheet_name="custodia", index=False)
        writer.save()
    
    def to_csv(self):
        self.dfDolar.to_csv(self.ruta + '\\rchivos csv\custodiaDolar.csv', index = False, header=True, sep='|')
        self.dfEuro.to_csv(self.ruta + '\\rchivos csv\custodiaEuro.csv', index = False, header=True, sep='|')
        
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
    
#todo = custodia_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Febrero').df
#ccBs = todo.cc_unifica.dfBs
#ahBs = todo.ah_unifica.dfBs
#Bs = todo.dfBs