import pandas as pd
import csv

class cc_unifica_load:
    
    #Atributos
    ruta = ''
    nombre_archivo = '\cc_unifica_'
    #conn = pdbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\José Prieto\Documents\Bancaribe\Enero\CrossSelling.accdb')
    
    #Constructor
    def __init__(self, ruta):
        self.ruta = ruta
        self.df = pd.read_csv(self.ruta + self.nombre_archivo + '2901.txt', delimiter='|', index_col=False, dtype=str, encoding='latin-1', quoting=csv.QUOTE_NONE)
        
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
    
    def make_DF(self):
        print("Creando cc_unifica")
        self.df[' Monto Contable '] = self.df[' Monto Contable '].astype(float)
        self.df[' Oficina Contable '] = self.df[' Oficina Contable '].astype(int)
        self.df = self.df[(self.df[" Oficina Contable "] <= 699) & (self.df[" Tipo Persona "] == "PERSONA JURIDICA") & 
                          ((self.df[" Estatus de la Operacion "] == "ACTIVA") | (self.df[" Estatus de la Operacion "] == "INACTIVA")) & 
                          ((self.df[" Producto "] != "Corriente - CUENTA CORRIENTE MON. EXT DOLAR") & (self.df[" Producto "] != "Corriente - CUENTA CORRIENTE ME EN EUROS")) &
                          (self.df[" Categoria "] != "B") & (self.df[" Categoria "] != "F") & (self.df[" Categoria "] != "H") & (self.df[" Categoria "] != "J") & (self.df[" Categoria "] != "K") & (self.df[" Categoria "] != "V")]
        self.df = self.df.groupby([' MIS '], as_index=False).agg({'Cedula/RIF ': 'first', ' Tipo Persona ': 'first', ' Estatus de la Operacion ': 'first', ' Producto ': 'first', ' Categoria ': 'first', ' Monto Contable ': sum})
        return self.df
    
#p = cc_unifica_load(r'C:\Users\bc221066\Documents\José Prieto\Insumos Cross Selling\Enero')
#cc = p.make_DF()